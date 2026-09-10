from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, field_validator

class Article(BaseModel):
    id: str
    title: str
    content: str = ""
    url: HttpUrl | str
    source: str
    published_at: datetime | None = None
    topics: list[str] = Field(default_factory=list)
    geography: str = "Global"
    reliability: float = Field(default=0.75, ge=0, le=1)
    embedding: list[float] | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()

class ValidationResult(BaseModel):
    relevant: bool
    relevance_score: float = Field(ge=0, le=1)
    reason: str
    topics: list[str] = Field(default_factory=list)
    geography: str = "Global"

class TopicResult(BaseModel):
    topics: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    sentiment: str = "neutral"

class ImpactResult(BaseModel):
    business_impact: float = Field(ge=0, le=10)
    urgency: float = Field(ge=0, le=10)
    market_impact: float = Field(ge=0, le=10)
    novelty: float = Field(ge=0, le=10)
    confidence: float = Field(ge=0, le=1)
    rationale: str = ""

class StorySummary(BaseModel):
    headline: str
    summary: str
    key_points: list[str] = Field(default_factory=list)
    impact: str
    what_to_watch: list[str] = Field(default_factory=list)

class MonitoringRule(BaseModel):
    min_priority: str = "HIGH"
    required_topics: list[str] = Field(default_factory=list)
    excluded_topics: list[str] = Field(default_factory=list)
    allowed_sources: list[str] = Field(default_factory=list)
    excluded_sources: list[str] = Field(default_factory=list)
    alert_enabled: bool = True

class PipelineRequest(BaseModel):
    domain: str
    keywords: list[str] = Field(default_factory=list)
    geography: list[str] = Field(default_factory=lambda: ["Global"])
    articles: list[Article]
    rules: MonitoringRule = Field(default_factory=MonitoringRule)
    persist: bool = True
    notify: bool = False

class RSSRequest(BaseModel):
    feed_urls: list[HttpUrl | str]
    domain: str
    keywords: list[str] = Field(default_factory=list)
    geography: list[str] = Field(default_factory=lambda: ["Global"])
    rules: MonitoringRule = Field(default_factory=MonitoringRule)
    persist: bool = True
    notify: bool = False

class QueueRequest(RSSRequest):
    pass
