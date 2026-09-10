import hashlib
from datetime import datetime, timezone
import feedparser
from app.config import settings
from app.schemas.news import Article

SOURCE_RELIABILITY = {
    "reuters": .95, "bbc": .92, "associated press": .95, "ap news": .95,
    "official": .95, "openai": .90, "microsoft": .90, "google": .90,
}

def reliability_for(source: str) -> float:
    s = source.lower()
    for key, value in SOURCE_RELIABILITY.items():
        if key in s: return value
    return .75

def fetch_rss(url: str) -> list[Article]:
    feed = feedparser.parse(url)
    articles = []
    source = feed.feed.get("title", url)
    reliability = reliability_for(source)
    for entry in feed.entries[:settings.max_articles_per_feed]:
        title = entry.get("title", "Untitled")
        content = entry.get("summary", entry.get("description", "")) or ""
        link = entry.get("link", "")
        raw_id = entry.get("id") or link or title
        digest = hashlib.sha256(raw_id.encode()).hexdigest()[:32]
        published = None
        if entry.get("published_parsed"):
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        articles.append(Article(id=digest, title=title, content=content, url=link, source=source, published_at=published, reliability=reliability))
    return articles
