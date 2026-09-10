from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.db.models import Base, ArticleRow, StoryRow, StoryArticleRow, AlertRow, AgentRunRow

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_articles_embedding_hnsw ON articles USING hnsw (embedding vector_cosine_ops)"))

def save_pipeline(result: dict):
    db = SessionLocal()
    try:
        for article in result.get("validated_articles", []):
            db.merge(ArticleRow(id=article.id, title=article.title, content=article.content, url=str(article.url), source=article.source, published_at=article.published_at, topics=article.topics, geography=article.geography, reliability=article.reliability, embedding=article.embedding))
        summaries = {s.headline: s for s in result.get("summaries", [])}
        for story in result.get("scored_stories", []):
            s = summaries.get(story["headline"])
            db.merge(StoryRow(id=story["story_id"], headline=story["headline"], priority=story.get("priority","LOW"), score=story["score"], source_reliability=story.get("source_reliability",.5), summary=s.summary if s else "", key_points=s.key_points if s else [], impact=s.impact if s else "", what_to_watch=s.what_to_watch if s else []))
            for a in story["articles"]:
                db.merge(StoryArticleRow(story_id=story["story_id"], article_id=a.id))
        for alert in result.get("alerts", []):
            db.merge(AlertRow(id=f"{result.get('run_id','run')}_{alert['story_id']}", story_id=alert["story_id"], priority=alert["priority"], headline=alert["headline"], delivered=False))
        db.commit()
    finally:
        db.close()
