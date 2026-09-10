import re
from app.graph.state import NewsState
STOP = {"the","a","an","and","to","of","in","for","on","with","new","is","are","from","by","as","this","that"}

def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2}

def story_clustering(state: NewsState) -> NewsState:
    groups = []
    for article in state.get("validated_articles", []):
        at = tokens(article.title + " " + " ".join(article.topics))
        best, best_sim = None, 0
        for group in groups:
            sim = len(at & group["tokens"]) / max(1, len(at | group["tokens"]))
            if sim > best_sim:
                best_sim, best = sim, group
        if best is not None and best_sim >= 0.30:
            best["articles"].append(article)
            best["tokens"] |= at
        else:
            groups.append({"tokens": set(at), "articles": [article]})
    stories = []
    for i, group in enumerate(groups, 1):
        articles = group["articles"]
        stories.append({"story_id": f"story_{i}", "headline": max(articles, key=lambda a: (a.reliability, len(a.title))).title, "articles": articles})
    return {"stories": stories}
