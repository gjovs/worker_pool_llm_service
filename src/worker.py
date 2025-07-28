import redis
import json
from .config import config
from .processing import process_document_task
import time

def start_worker():
    redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    print(f"Worker iniciado. Escutando a fila '{config.TASK_QUEUE_NAME}' no Redis...")
    
    while True:
        try:
            _, task_raw = redis_client.brpop(config.TASK_QUEUE_NAME)
            print(f"Tarefa recebida: {task_raw}")
            task = json.loads(task_raw)
            print(f"Tarefa recebida: {task}")
            process_document_task(task)
        except redis.exceptions.ConnectionError as e:
            print(f"Erro de conexão com o Redis, tentando reconectar... {e}")
            time.sleep(5)
        except json.JSONDecodeError:
            print(f"Erro ao decodificar a tarefa: {task_raw}")
        except Exception as e:
            print(f"Erro inesperado no worker: {e}")