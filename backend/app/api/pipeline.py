import uuid
from fastapi import APIRouter, HTTPException
from app.graph.workflow import news_graph
from app.schemas.news import PipelineRequest, RSSRequest, QueueRequest
from app.ingestion.rss import fetch_rss
from app.db.session import save_pipeline
from app.services.queue import enqueue

router = APIRouter(prefix="/api", tags=["news"])

def execute(request: PipelineRequest):
    run_id = uuid.uuid4().hex
    result = news_graph.invoke({"domain": request.domain, "keywords": request.keywords, "geography": request.geography, "rules": request.rules, "raw_articles": request.articles, "run_id": run_id})
    result["run_id"] = run_id
    if request.persist:
        try: save_pipeline(result)
        except Exception as exc: raise HTTPException(500, f"Persistence failed: {exc}")
    return {
        "run_id": run_id, "stories": result.get("scored_stories", []), "summaries": result.get("summaries", []), "alerts": result.get("alerts", []),
        "stats": {"received": len(request.articles), "relevant": len(result.get("relevant_articles", [])), "validated": len(result.get("validated_articles", [])), "stories": len(result.get("stories", [])), "alerts": len(result.get("alerts", []))}
    }

@router.post("/pipeline/run")
def run_pipeline(request: PipelineRequest): return execute(request)

@router.post("/rss/run")
def run_rss(request: RSSRequest):
    articles = [a for url in request.feed_urls for a in fetch_rss(str(url))]
    return execute(PipelineRequest(domain=request.domain, keywords=request.keywords, geography=request.geography, articles=articles, rules=request.rules, persist=request.persist, notify=request.notify))

@router.post("/jobs/rss")
def queue_rss(request: QueueRequest):
    job_id = enqueue(request.model_dump(mode="json"))
    return {"job_id": job_id, "status": "queued"}
