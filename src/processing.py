from .config import config
from .services.cache_service import Neo4jCacheService
from .services.llm_service import OpenAILLMService
from .services.stream_service import RedisStreamService
from .services.persistence_service import PersistenceService
from .utils import get_text_from_pdf_url
import redis
import time


def process_document_task(task: dict):
    doc_id = task.get('doc_id')
    file_url = task.get('file_url')  # Agora recebemos a URL

    if not doc_id or not file_url:
        print("Tarefa inválida, faltando 'doc_id' ou 'file_url'.")
        return

    streamer = RedisStreamService(redis.Redis(
        host=config.REDIS_HOST, port=config.REDIS_PORT), doc_id)

    persister = PersistenceService(config.DATABASE_URL)

    cacher = Neo4jCacheService(
        config.NEO4J_URI, config.NEO4J_USER, config.NEO4J_PASSWORD)

    llm = OpenAILLMService()

    print(
        f"Iniciando processamento para o documento: {doc_id} a partir de {file_url}")

    try:
        print(
            f"Iniciando processamento para o documento: {doc_id} a partir de {file_url}")
        persister.update_insight_status(doc_id, 'PROCESSING')

        document_text_content = get_text_from_pdf_url(file_url)

        if not document_text_content:
            raise ValueError("Não foi possível extrair conteúdo do PDF.")

        cached_insight = cacher.find_similar_insight(document_text_content, config.DOCUMENT_THRESHOLD_SIMILARITY)

        if cached_insight:
            print(f"Cache HIT para o documento {doc_id}.")
            
            for word in cached_insight.split():
                token_to_stream = word + " "
                streamer.publish_token(token_to_stream)
                time.sleep(0.02)
                
            persister.save_final_insight(doc_id, cached_insight)
            streamer.publish_end_of_stream()
            return

        print(f"Cache MISS para o documento {doc_id}. Chamando LLM.")
        full_response = []

        def token_callback(token: str):
            full_response.append(token)
            streamer.publish_token(token)

        llm.stream_completion(document_text_content, on_token=token_callback)

        # 4. Processos pós-stream
        final_text = "".join(full_response)
        persister.save_final_insight(doc_id, final_text)
        cacher.save_embedding_and_insight(
            doc_id, document_text_content, final_text)
        streamer.publish_end_of_stream()

    except Exception as e:
        print(f"ERRO CRÍTICO ao processar documento {doc_id}: {e}")
        persister.update_insight_status(doc_id, 'FAILED')
        streamer.publish_error(str(e))
    finally:
        cacher.close()

