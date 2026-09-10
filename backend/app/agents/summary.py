from app.graph.state import NewsState
from app.schemas.news import StorySummary
from app.agents.llm import llm

def summary_agent(state: NewsState) -> NewsState:
    summaries = []
    for story in state.get("scored_stories", []):
        articles = story["articles"]
        mock = StorySummary(
            headline=story["headline"],
            summary=f"{story['headline']} was reported across {len(articles)} source(s).",
            key_points=[a.title for a in articles[:3]],
            impact="Potential relevance to the monitored domain; verify against primary sources.",
            what_to_watch=["Official follow-up", "Business or market impact"],
        )
        result = llm.structured(
            "Write a concise factual intelligence summary from the supplied sources. Do not invent facts. Return structured output only.",
            f"Story: {story['headline']}\nArticles:\n" + "\n".join(f"- {a.source}: {a.title}\n{a.content[:2000]}" for a in articles[:5]),
            StorySummary, mock,
        )
        summaries.append(result)
    return {"summaries": summaries}
