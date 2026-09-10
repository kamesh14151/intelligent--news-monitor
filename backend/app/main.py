from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.pipeline import router
from app.db.session import init_db

app = FastAPI(title="Intelligent News Monitoring API", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.on_event("startup")
def startup(): init_db()

@app.get("/health")
def health(): return {"status":"ok", "service":"news-intelligence", "version":"0.3.0"}
