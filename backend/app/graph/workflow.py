from langgraph.graph import StateGraph, START, END
from app.graph.state import NewsState
from app.agents.discovery import semantic_discovery
from app.agents.validation import context_validation
from app.agents.clustering import story_clustering
from app.agents.topic import topic_analysis
from app.agents.impact import impact_analysis
from app.agents.importance import importance_analysis
from app.agents.summary import summary_agent
from app.rules.engine import rule_engine
from app.services.audit import agent_audit

def _audited(name, fn):
    def wrapped(state: NewsState) -> NewsState:
        with agent_audit(state.get("run_id", "unknown"), name):
            return fn(state)
    return wrapped

def build_graph():
    g = StateGraph(NewsState)
    g.add_node("discover", _audited("semantic_discovery", semantic_discovery))
    g.add_node("validate", _audited("context_validation", context_validation))
    g.add_node("cluster", _audited("story_clustering", story_clustering))
    g.add_node("topics", _audited("topic_analysis", topic_analysis))
    g.add_node("impact", _audited("impact_analysis", impact_analysis))
    g.add_node("importance", _audited("importance_analysis", importance_analysis))
    g.add_node("summary", _audited("summary_agent", summary_agent))
    g.add_node("rules", _audited("rule_engine", rule_engine))
    g.add_edge(START, "discover")
    g.add_edge("discover", "validate")
    g.add_edge("validate", "cluster")
    g.add_edge("cluster", "topics")
    g.add_edge("cluster", "impact")
    g.add_edge(["topics", "impact"], "importance")
    g.add_edge("importance", "summary")
    g.add_edge("summary", "rules")
    g.add_edge("rules", END)
    return g.compile()

news_graph = build_graph()
