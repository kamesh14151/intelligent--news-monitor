from app.graph.state import NewsState
from app.schemas.news import TopicResult
from app.agents.llm import llm

def topic_analysis(state: NewsState) -> NewsState:
    out = {}
    for story in state.get("stories", []):
        articles = story["articles"]
        words = []
        for a in articles:
            words.extend(a.topics)
        mock = TopicResult(topics=list(dict.fromkeys(words))[:10], entities=[], sentiment="neutral")
        result = llm.structured(
            "Extract the main topics, named entities and overall sentiment from the supplied news story. Do not invent facts.",
            f"Headline: {story['headline']}\n" + "\n".join(f"{a.source}: {a.content[:1500]}" for a in articles[:5]),
            TopicResult, mock,
        )
        out[story["story_id"]] = result
    return {"topics": out}
