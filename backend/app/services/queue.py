import json
import uuid
from redis import Redis
from app.config import settings

QUEUE = "news:pipeline"

def enqueue(payload: dict) -> str:
    job_id = uuid.uuid4().hex
    client = Redis.from_url(settings.redis_url, decode_responses=True)
    client.rpush(QUEUE, json.dumps({"job_id": job_id, **payload}))
    return job_id
