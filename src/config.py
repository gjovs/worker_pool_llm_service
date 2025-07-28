import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    TASK_QUEUE_NAME = 'tasks_queue'

    # PostgreSQL
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Neo4j
    NEO4J_URI = f"bolt://{os.getenv('NEO4J_HOST', 'localhost')}:7687"
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    
    DOCUMENT_THRESHOLD_SIMILARITY = float(os.getenv('DOCUMENT_THRESHOLD_SIMILARITY', 0.95))

config = Config()
