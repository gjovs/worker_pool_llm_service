from neo4j import GraphDatabase

from ..config import config

from openai import OpenAI


class Neo4jCacheService:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self.open_client = OpenAI(api_key=config.OPENAI_API_KEY)

    def close(self):
        self._driver.close()
        if self.open_client.is_closed() is False:
            self.open_client.close()


    def _get_text_embedding(self, text: str) -> list[float]:
        """Gera um vetor de embedding usando a nova sintaxe da API."""
        text = text.replace("\n", " ")
        response = self.open_client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"  # Modelo de embedding mais recente e eficiente
        )
        return response.data[0].embedding

    def find_similar_insight(self, text_content: str, threshold: float = 0.95):
        """Busca por um insight similar no grafo e o retorna se a similaridade for alta."""
        embedding_vector = self._get_text_embedding(text_content)

        query = """
        CALL db.index.vector.queryNodes('document_embeddings', 10, $embedding) YIELD node, score
        WHERE score >= $threshold
        RETURN node.insight AS insight, score
        ORDER BY score DESC
        LIMIT 1
        """
        with self._driver.session() as session:
            result = session.run(
                query, embedding=embedding_vector, threshold=threshold)
            record = result.single()
            return record['insight'] if record else None

    def save_embedding_and_insight(self, doc_id: str, text_content: str, insight_text: str):
        """Salva o embedding e o insight gerado no Neo4j."""
        embedding_vector = self._get_text_embedding(text_content)
        query = """
        CREATE (e:DocumentEmbedding {doc_id: $doc_id, embedding: $embedding, insight: $insight})
        """
        with self._driver.session() as session:
            session.run(query, doc_id=doc_id,
                        embedding=embedding_vector, insight=insight_text)
        print(f"Embedding para doc_id {doc_id} salvo no Neo4j.")

    def ensure_vector_index(self):
        """Garante que o índice vetorial exista no Neo4j para buscas rápidas."""
        # Esta função deve ser rodada uma vez na inicialização
        query = """
        CREATE VECTOR INDEX document_embeddings IF NOT EXISTS
        FOR (n:DocumentEmbedding) ON (n.embedding)
        OPTIONS { indexConfig: {
            `vector.dimensions`: 1536,
            `vector.similarity_function`: 'cosine'
        }}
        """
        with self._driver.session() as session:
            session.run(query)
        print("Índice vetorial do Neo4j verificado/criado com sucesso.")
