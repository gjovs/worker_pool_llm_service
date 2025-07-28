from .worker import start_worker
from .services import Neo4jCacheService
from .config import config

if __name__ == "__main__":
    try:
        cacher = Neo4jCacheService(
            config.NEO4J_URI, config.NEO4J_USER, config.NEO4J_PASSWORD)
        cacher.ensure_vector_index()
        cacher.close()
    except Exception as e:
        print(
            f"AVISO: Não foi possível verificar/criar o índice do Neo4j. {e}")
        print("O serviço continuará, mas a busca por similaridade pode falhar.")

    start_worker()
