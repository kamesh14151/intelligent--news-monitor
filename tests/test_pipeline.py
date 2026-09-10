import sys
sys.path.insert(0, "backend")
from app.graph.workflow import news_graph
from app.schemas.news import Article, MonitoringRule

def test_pipeline_mock():
    result = news_graph.invoke({
        "domain":"Artificial Intelligence", "keywords":["LLM","AI agents"], "geography":["Global"],
        "rules": MonitoringRule(min_priority="LOW"),
        "raw_articles":[
            Article(id="1",title="AI agents launch",content="New AI agents and LLM tools are announced.",url="https://example.com/1",source="OpenAI",reliability=.9),
            Article(id="2",title="Football results",content="A team won a match.",url="https://example.com/2",source="Demo",reliability=.7)
        ], "run_id":"test"
    })
    assert len(result["validated_articles"]) == 1
    assert result["scored_stories"]
    assert result["summaries"]
    assert result["scored_stories"][0]["priority"] in {"LOW","MEDIUM","HIGH","CRITICAL"}
    assert result["topics"]
    assert result["impacts"]
