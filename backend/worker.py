import json, time, traceback
from redis import Redis
from app.config import settings
from app.ingestion.rss import fetch_rss
from app.graph.workflow import news_graph
from app.db.session import save_pipeline, init_db
from app.schemas.news import MonitoringRule

QUEUE = "news:pipeline"
client = Redis.from_url(settings.redis_url, decode_responses=True)
init_db()
print("news worker started")
while True:
    item = client.blpop(QUEUE, timeout=5)
    if not item:
        continue
    try:
        payload = json.loads(item[1])
        articles = []
        for url in payload["feed_urls"]:
            articles.extend(fetch_rss(url))
        result = news_graph.invoke({"domain": payload["domain"], "keywords": payload["keywords"], "geography": payload["geography"], "rules": MonitoringRule(**payload["rules"]), "raw_articles": articles, "run_id": payload["job_id"]})
        result["run_id"] = payload["job_id"]
        save_pipeline(result)
        print(f"completed {payload['job_id']}: {len(result.get('alerts', []))} alerts")
    except Exception:
        traceback.print_exc()
