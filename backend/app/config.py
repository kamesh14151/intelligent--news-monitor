from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://news:news@localhost:5432/newsintel"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"
    openai_embedding_model: str = "text-embedding-3-small"
    mock_llm: bool = True
    embedding_dimension: int = 1536
    cors_origins: str = "http://localhost:3000"
    max_articles_per_feed: int = 100
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
