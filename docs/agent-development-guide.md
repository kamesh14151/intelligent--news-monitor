# Beginner Agent Development Guide

## What is an agent here?

An agent is a normal Python function that performs one specialized reasoning task and returns part of the shared `NewsState`.

```python
from app.graph.state import NewsState

def my_agent(state: NewsState) -> NewsState:
    # read input
    # do work
    # return output
    return {"some_field": result}
```

The five agents are deliberately **not** five separate servers. LangGraph orchestrates them in one controlled workflow.

## The shared flow

```text
raw_articles
    ↓
relevant_articles
    ↓
validated_articles
    ↓
stories
    ↓
impacts / scored_stories
    ↓
summaries
    ↓
alerts
```

## Structured output

Use Pydantic models from `backend/app/schemas/news.py`. Do not return free-form strings where a schema exists.

Example:

```python
result = llm.structured(
    "Return only the requested structured result.",
    evidence_text,
    ValidationResult,
    mock_result,
)
```

## LLM safety rules for this project

- Use only supplied evidence.
- Do not invent facts.
- Prefer structured output.
- Keep a mock path for tests.
- Never put API keys in source code.
- Keep prompts short and specific.

## How to test without an API key

`.env` should contain:

```env
MOCK_LLM=true
```

This allows the project tests to run with deterministic fallback outputs.

## What to learn first

1. Python functions and dictionaries
2. Pydantic models
3. Async basics (only where already used)
4. Embeddings and cosine similarity
5. Prompt + structured output
6. LangGraph state/node concepts
7. pytest
8. Git branches and Pull Requests

You do not need to understand the entire application before implementing your assigned agent.
