# Intelligent News Monitor — 5-Member Team Task Document

## Goal
Build and integrate five specialized AI agents into one LangGraph news-intelligence pipeline.

**Pipeline:**

`RSS/API articles → Discovery → Validation → Clustering → Importance → Summary → Rule Engine → DB/Alerts/Dashboard`

## Golden rule
Each member owns **one agent** and works on their own Git branch. Do not rewrite another member's agent. Shared contracts in `backend/app/schemas/` and `backend/app/graph/state.py` are controlled by the integration owner (Kamesh / team lead).

## Branches

| Member | Name | Branch | Agent | File |
|---|---|---|---|---|
| 1 | **Kamesh** | `feature/agent-discovery` | Semantic Discovery | `backend/app/agents/discovery.py` |
| 2 | **Kanish S** | `feature/agent-validation` | Context Validation | `backend/app/agents/validation.py` |
| 3 | **Ajay Krithick S V** | `feature/agent-clustering` | Story Clustering | `backend/app/agents/clustering.py` |
| 4 | **Dev M K** | `feature/agent-importance` | Importance Analysis | `backend/app/agents/importance.py` |
| 5 | **Kamesh** | `feature/agent-summary` | Summary | `backend/app/agents/summary.py` |

## Member 1 — Semantic Discovery Agent *(Kamesh)*

### Objective
Reduce a large incoming article set to articles that are semantically relevant to the user's monitored domain.

### Input
From `NewsState`:
- `raw_articles`
- `domain`
- `keywords`
- `geography`

### Output
Write:
- `relevant_articles`
- `embeddings` (when embeddings are available)

### Implementation plan
1. Read `backend/app/agents/discovery.py`.
2. Normalize domain and keywords.
3. Build a query text from domain + keywords.
4. Create embeddings using `backend/app/services/embeddings.py`.
5. Score articles using semantic similarity plus lightweight keyword evidence.
6. Keep the strongest candidates; do not call the LLM for every article.
7. Preserve the original `Article` object and never invent article data.
8. Handle an empty article list safely.

### Beginner explanation
An embedding converts text into numbers representing meaning. Similar texts have similar vectors. Your job is to compare the user's monitoring topic with each article and keep the articles that are closest.

### Done when
- `news_graph.invoke()` still runs.
- Empty input returns an empty list.
- Output contains only `Article` objects from the input.
- Add/update unit tests for relevant and irrelevant articles.

---

## Member 2 — Context Validation Agent *(Kanish S)*

### Objective
Check whether each discovered article is genuinely relevant, not merely matching a keyword.

### Input
- `relevant_articles`
- `domain`
- `keywords`
- `geography`

### Output
- `validated_articles`
- `validation` map keyed by article ID.

Each validation should contain:
- `relevant`
- `relevance_score` (0–1)
- `reason`
- `topics`
- `geography`

### Implementation plan
1. Read `backend/app/schemas/news.py` and the `ValidationResult` model.
2. For each article, prepare a short evidence prompt.
3. Use structured LLM output through `backend/app/agents/llm.py`.
4. Keep a deterministic mock/fallback so tests work without an API key.
5. Reject low-confidence or geographically invalid articles.
6. Never invent facts.

### Beginner explanation
A keyword can be misleading. For example, an article may contain "AI" but actually be about a football club named AI. Validation reads the context and decides whether the article really belongs to the monitored topic.

### Done when
- Every processed article gets a structured validation result.
- Scores are between 0 and 1.
- Tests cover a relevant and irrelevant example.

---

## Member 3 — Story Clustering Agent *(Ajay Krithick S V)*

### Objective
Group multiple articles reporting the same underlying event into one story.

### Input
- `validated_articles`

### Output
- `stories`

Each story should contain:
- `story_id`
- `headline`
- `articles`

### Implementation plan
1. Start with title/topic token similarity so the algorithm is easy to understand.
2. Compare each article with existing groups.
3. If similarity is above your threshold, add it to that group.
4. Otherwise create a new group.
5. Choose a representative headline from the strongest source.
6. Later, improve the similarity step using embeddings/pgvector.

### Beginner explanation
If 10 websites report the same OpenAI launch, the dashboard should show one story with 10 sources, not 10 duplicate cards.

### Done when
- Similar articles become one story.
- Clearly unrelated articles remain separate.
- A story with one article still works.
- Add tests for duplicate/similar headlines.

---

## Member 4 — Importance Analysis Agent *(Dev M K)*

### Objective
Estimate how important each story is. This agent provides signals; the central rule engine decides the final priority.

### Input
- `stories`
- topic information if available
- source reliability

### Output
- `impacts` map keyed by `story_id`
- final score fields consumed by the existing importance stage

### Scores
Each 0–10:
- `business_impact`
- `urgency`
- `market_impact`
- `novelty`

Plus:
- `confidence` 0–1
- `rationale`

### Implementation plan
1. Read `ImpactResult` in `backend/app/schemas/news.py`.
2. Give the model the story headline and source evidence.
3. Ask for structured JSON through `llm.structured()`.
4. Do not ask the model to decide `HIGH/LOW/CRITICAL` directly.
5. Keep the final formula in `backend/app/rules/engine.py`.
6. Keep a mock scoring path for offline tests.

### Beginner explanation
The model answers questions such as: "Could this affect businesses? Is it urgent? Is it new?" The rule engine later converts these numbers into LOW/MEDIUM/HIGH/CRITICAL.

### Done when
- All scores stay in valid ranges.
- Every story gets an impact result.
- Tests verify score ranges and output shape.

---

## Member 5 — Summary Agent *(Kamesh)*

### Objective
Turn a clustered, scored story into a concise factual intelligence report.

### Input
- `scored_stories`
- article content and sources

### Output
- `summaries`

Each summary contains:
- `headline`
- `summary`
- `key_points`
- `impact`
- `what_to_watch`

### Implementation plan
1. Read `StorySummary` in `backend/app/schemas/news.py`.
2. Give the LLM the story headline plus a limited number of source articles.
3. Tell it to use only supplied evidence.
4. Ask for structured output.
5. Keep summaries concise and factual.
6. Never invent statistics, people, dates or claims.
7. Keep mock output for tests.

### Beginner explanation
Instead of making the user read five articles, this agent reads the evidence and produces one short report: what happened, key points, why it matters, and what to watch next.

### Done when
- One summary is produced per scored story.
- The output matches `StorySummary`.
- Tests verify the fields exist.

---

# How every member should work

## 1. Get the project

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd intelligent-news-monitor-team
```

## 2. Checkout your branch

Example for Member 1:

```bash
git checkout feature/agent-discovery
```

If the branch does not exist on the remote yet:

```bash
git checkout -b feature/agent-discovery
```

## 3. Install/run

Use the root README for Docker setup. Keep `MOCK_LLM=true` while learning and testing.

## 4. Change only your agent + its tests/docs

Good:

```text
backend/app/agents/discovery.py
tests/test_discovery.py
team/member-1-discovery/README.md
```

Avoid changing:

```text
backend/app/graph/state.py
backend/app/graph/workflow.py
backend/app/schemas/news.py
backend/app/rules/engine.py
```

unless the team lead approves it.

## 5. Run tests

```bash
pytest -q
```

## 6. Commit

```bash
git add .
git commit -m "feat: implement semantic discovery agent"
```

## 7. Push

```bash
git push -u origin feature/agent-discovery
```

## 8. Open a Pull Request

PR title format:

`feat: implement <agent-name> agent`

Explain:
- what you changed
- how your agent works
- tests added
- any limitations

---

# Team lead integration checklist

After each PR:

1. Pull latest `main`.
2. Review the changed files.
3. Run `pytest -q`.
4. Run the pipeline in mock mode.
5. Check the agent's output against the shared Pydantic schema.
6. Merge only after the pipeline still works end-to-end.

The integration owner controls `workflow.py`, shared state, schemas, database integration, API integration, frontend and deployment.
