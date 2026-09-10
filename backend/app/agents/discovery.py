# Agent: Semantic Discovery | Owner: Kamesh (Member 1)
from app.graph.state import NewsState
from app.services.embeddings import embed_texts


def semantic_discovery(state: NewsState) -> NewsState:
    keywords = [k.lower().strip() for k in state.get("keywords", []) if k.strip()]
    domain = state.get("domain", "").lower().strip()
    articles = state.get("raw_articles", [])
    query = " ".join([domain, *keywords])
    query_vec = embed_texts([query])[0] if query else None
    vectors = embed_texts([f"{a.title}\n{a.content[:2000]}" for a in articles]) if articles else []
    scored = []
    for article, vec in zip(articles, vectors):
        text = f"{article.title} {article.content}".lower()
        hits = sum(1 for k in keywords if k in text)
        domain_hit = 2 if domain and domain in text else 0
        if query_vec:
            dot = sum(x*y for x,y in zip(query_vec, vec))
        else:
            dot = 0
        score = hits + domain_hit + max(0, dot) * 2
        article.embedding = vec
        scored.append((score, article))
    scored.sort(key=lambda x: x[0], reverse=True)
    return {"relevant_articles": [a for score, a in scored if score > 0.15][:100], "embeddings": {a.id: a.embedding for _, a in scored if a.embedding}}
