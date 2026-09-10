from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float, JSON, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from app.config import settings

class Base(DeclarativeBase): pass

class SourceRow(Base):
    __tablename__ = "sources"
    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    reliability: Mapped[float] = mapped_column(Float, default=.75)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

class ArticleRow(Base):
    __tablename__ = "articles"
    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(255), index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    topics: Mapped[list] = mapped_column(JSON, default=list)
    geography: Mapped[str] = mapped_column(String(100), default="Global")
    reliability: Mapped[float] = mapped_column(Float, default=.75)
    embedding: Mapped[list | None] = mapped_column(Vector(settings.embedding_dimension), nullable=True)

class StoryRow(Base):
    __tablename__ = "stories"
    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    headline: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(20), index=True)
    score: Mapped[float] = mapped_column(Float)
    source_reliability: Mapped[float] = mapped_column(Float)
    summary: Mapped[str] = mapped_column(Text, default="")
    key_points: Mapped[list] = mapped_column(JSON, default=list)
    impact: Mapped[str] = mapped_column(Text, default="")
    what_to_watch: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class StoryArticleRow(Base):
    __tablename__ = "story_articles"
    story_id: Mapped[str] = mapped_column(String(128), ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True)
    article_id: Mapped[str] = mapped_column(String(128), ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)

class AgentRunRow(Base):
    __tablename__ = "agent_runs"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30))
    latency_ms: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class AlertRow(Base):
    __tablename__ = "alerts"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    story_id: Mapped[str] = mapped_column(String(128), index=True)
    priority: Mapped[str] = mapped_column(String(20))
    headline: Mapped[str] = mapped_column(Text)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class MonitoringRuleRow(Base):
    __tablename__ = "monitoring_rules"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    domain: Mapped[str] = mapped_column(String(255), index=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
