# Agent: Importance Analysis | Owner: Dev M K (Member 4)
from app.graph.state import NewsState

def importance_analysis(state: NewsState) -> NewsState:
    scored = []
    for story in state.get("stories", []):
        result = state["impacts"][story["story_id"]]
        reliability = max((a.reliability for a in story["articles"]), default=.5)
        raw = (result.business_impact*.30 + result.urgency*.25 + result.market_impact*.20 + result.novelty*.15 + result.confidence*10*.10)
        score = round(raw * (.7 + .3*reliability), 2)
        scored.append({**story, "impact": result, "score": score, "source_reliability": round(reliability, 2)})
    return {"scored_stories": scored}
