import hashlib
import math
from app.config import settings
from app.agents.llm import llm


def _mock_embedding(text: str, dim: int = 1536) -> list[float]:
    # Deterministic local fallback so the demo works without an API key.
    values = []
    seed = text.encode("utf-8")
    counter = 0
    while len(values) < dim:
        digest = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
        values.extend(((b / 127.5) - 1.0) for b in digest)
        counter += 1
    values = values[:dim]
    norm = math.sqrt(sum(x*x for x in values)) or 1.0
    return [x / norm for x in values]


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    if not llm.client:
        return [_mock_embedding(t, settings.embedding_dimension) for t in texts]
    response = llm.client.embeddings.create(model=settings.openai_embedding_model, input=texts)
    return [item.embedding for item in response.data]
