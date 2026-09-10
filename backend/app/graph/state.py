import operator
from typing import Annotated, TypedDict
from app.schemas.news import Article, ImpactResult, MonitoringRule, StorySummary, TopicResult, ValidationResult

class NewsState(TypedDict, total=False):
    raw_articles: list[Article]
    relevant_articles: list[Article]
    validated_articles: list[Article]
    stories: list[dict]
    scored_stories: list[dict]
    summaries: list[StorySummary]
    alerts: list[dict]
    domain: str
    keywords: list[str]
    geography: list[str]
    rules: MonitoringRule
    validation: dict[str, ValidationResult]
    topics: dict[str, TopicResult]
    impacts: dict[str, ImpactResult]
    embeddings: dict[str, list[float]]
    run_id: str
