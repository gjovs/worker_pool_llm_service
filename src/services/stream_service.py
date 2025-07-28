import redis
import json


class RedisStreamService:
    def __init__(self, redis_client: redis.Redis, doc_id: str):
        self.redis = redis_client
        self.channel_name = f"doc_stream:{doc_id}"

    def publish_message(self, event: str, data: dict):
        payload = json.dumps({'event': event, **data})
        self.redis.publish(self.channel_name, payload)

    def publish_token(self, token: str):
        self.publish_message('TOKEN', {'token': token})

    def publish_end_of_stream(self):
        self.publish_message('STREAM_END', {})
        print(f"Fim do stream publicado para o canal {self.channel_name}")

    def publish_error(self, error_message: str):
        self.publish_message('ERROR', {'message': error_message})
