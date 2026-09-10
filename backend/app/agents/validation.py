from app.graph.state import NewsState
from app.schemas.news import ValidationResult
from app.agents.llm import llm


def validate_one(article, state):
    text = f"{article.title} {article.content}".lower()
    keywords = [k.lower() for k in state.get("keywords", [])]
    hits = [k for k in keywords if k and k in text]
    mock = ValidationResult(
        relevant=bool(hits),
        relevance_score=min(1.0, 0.45 + 0.12 * len(hits)) if hits else 0.1,
        reason="Configured keyword/domain evidence supports relevance." if hits else "No configured keyword evidence found.",
        topics=hits[:8], geography=article.geography,
    )
    return llm.structured(
        "Validate article relevance to the monitored domain. Be conservative; do not invent facts. Return structured output only.",
        f"Domain: {state.get('domain')}\nKeywords: {state.get('keywords')}\nGeography: {state.get('geography')}\nTitle: {article.title}\nContent: {article.content[:5000]}",
        ValidationResult, mock,
    )


def context_validation(state: NewsState) -> NewsState:
    validated, results = [], {}
    allowed_geo = {g.lower() for g in state.get("geography", [])}
    for article in state.get("relevant_articles", []):
        result = validate_one(article, state)
        results[article.id] = result
        geo_ok = not allowed_geo or "global" in allowed_geo or result.geography.lower() in allowed_geo or article.geography.lower() in allowed_geo
        if result.relevant and result.relevance_score >= 0.5 and geo_ok:
            article.topics = result.topics
            validated.append(article)
    return {"validated_articles": validated, "validation": results}
