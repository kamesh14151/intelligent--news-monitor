from app.graph.state import NewsState
ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

def classify(score: float) -> str:
    if score >= 9: return "CRITICAL"
    if score >= 7.5: return "HIGH"
    if score >= 5: return "MEDIUM"
    return "LOW"

def rule_engine(state: NewsState) -> NewsState:
    rules = state.get("rules")
    summary_map = {s.headline: s for s in state.get("summaries", [])}
    scored, alerts = [], []
    for story in state.get("scored_stories", []):
        priority = classify(story["score"])
        topics = set((state.get("topics", {}).get(story["story_id"]).topics if story["story_id"] in state.get("topics", {}) else []))
        sources = {a.source for a in story["articles"]}
        allowed = not rules.allowed_sources or bool(sources & set(rules.allowed_sources))
        excluded_source = bool(sources & set(rules.excluded_sources))
        required_ok = not rules.required_topics or bool(topics & set(rules.required_topics))
        excluded_topic = bool(topics & set(rules.excluded_topics))
        if not allowed or excluded_source or not required_ok or excluded_topic:
            continue
        enriched = {**story, "priority": priority, "summary": summary_map.get(story["headline"])}
        scored.append(enriched)
        if rules.alert_enabled and ORDER[priority] >= ORDER.get(rules.min_priority, 3):
            alerts.append({"story_id": story["story_id"], "priority": priority, "headline": story["headline"]})
    return {"scored_stories": scored, "alerts": alerts}
