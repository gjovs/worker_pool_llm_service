from sqlalchemy import create_engine, text
import json

class PersistenceService:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def update_insight_status(self, doc_id: str, status: str):
        """Atualiza o status de um insight no banco de dados."""
        query = text(
            "UPDATE infrastructure_documentinsight SET status = :status, updated_at = NOW() WHERE document_id = :doc_id")
        with self.engine.connect() as connection:
            connection.execute(query, {"status": status, "doc_id": doc_id})
            connection.commit()

    def save_final_insight(self, doc_id: str, insight_text: str):
        """Salva o conteúdo final do insight e marca como concluído."""
        query = text("""
            UPDATE infrastructure_documentinsight 
            SET content = :content, status = 'COMPLETED', updated_at = NOW() 
            WHERE document_id = :doc_id
        """)
        with self.engine.connect() as connection:
            content_json = {"summary": insight_text}  # Salva como JSON
            connection.execute(
                query, {"content": json.dumps(content_json), "doc_id": doc_id})
            connection.commit()
