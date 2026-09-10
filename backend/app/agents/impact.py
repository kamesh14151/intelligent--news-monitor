from app.graph.state import NewsState
from app.schemas.news import ImpactResult
from app.agents.llm import llm

def impact_analysis(state: NewsState) -> NewsState:
    out = {}
    for story in state.get("stories", []):
        articles = story["articles"]
        n = len(articles)
        mock = ImpactResult(
            business_impact=min(10, 4 + n), urgency=min(10, 3 + n), market_impact=min(10, 4 + n * .5),
            novelty=min(10, 5 + n * .7), confidence=.75, rationale="Mock score based on source count; replace with model scoring in production."
        )
        result = llm.structured(
            "Assess business impact, urgency, market impact, novelty and confidence for this news story. Use only supplied evidence.",
            f"Headline: {story['headline']}\nSources: {[a.source for a in articles]}\nContent: " + "\n".join(a.content[:1600] for a in articles[:5]),
            ImpactResult, mock,
        )
        out[story["story_id"]] = result
    return {"impacts": out}
