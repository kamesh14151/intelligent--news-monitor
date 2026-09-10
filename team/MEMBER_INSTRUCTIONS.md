# Team Member Instructions — Intelligent News Monitor

This document contains instructions for every team member.
Read your section carefully before starting.

---

## Golden Rule

**Never push directly to `main`.**

Every member works on their own branch:

| Member | Name | Branch |
|--------|------|--------|
| 1 | Kamesh | `feature/agent-discovery` |
| 2 | Kanish S | `feature/agent-validation` |
| 3 | Ajay Krithick S V | `feature/agent-clustering` |
| 4 | Dev M K | `feature/agent-importance` |
| 5 | Kamesh | `feature/agent-summary` |

After you push your branch, open a Pull Request. The team lead will review and merge it into `main`.

---

## MEMBER 1 — Semantic Discovery Agent

**Owner:** Kamesh  
**Branch:** `feature/agent-discovery`  
**Pipeline:** `raw_articles -> relevant_articles`  
**Main file:** `backend/app/agents/discovery.py`

### Responsibility

Your agent should:
- Receive raw news articles
- Understand the configured topic/domain
- Decide whether each article is relevant
- Remove irrelevant articles
- Return structured output using the shared schemas
- Do NOT modify other members' agent logic

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/kamesh14151/intelligent--news-monitor.git
```

**2. Enter the project**

```bash
cd intelligent--news-monitor
```

**3. Create or switch to your branch**

```bash
git checkout feature/agent-discovery
```

If the branch does not exist yet on the remote:

```bash
git checkout -b feature/agent-discovery
```

**4. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**5. Open and edit your main file**

```
backend/app/agents/discovery.py
```

**6. Test your work**

```bash
python -m pytest tests/test_agent_contracts.py
```

**7. Check your changes**

```bash
git status
```

**8. Commit**

```bash
git add .
git commit -m "Implement semantic discovery agent"
```

**9. Push ONLY your branch**

```bash
git push -u origin feature/agent-discovery
```

**10. Open a Pull Request on GitHub**

Go to the repository on GitHub and open a Pull Request from `feature/agent-discovery` into `main`.

---

## MEMBER 2 — Context Validation Agent

**Owner:** Kanish S  
**Branch:** `feature/agent-validation`  
**Pipeline:** `relevant_articles -> validated_articles`  
**Main file:** `backend/app/agents/validation.py`

### Responsibility

Your agent should:
- Check whether discovered articles have enough context
- Detect weak, duplicate, or misleading information
- Evaluate source reliability and context
- Validate important claims where possible
- Return structured validated article data
- Do NOT modify other members' agent logic

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/kamesh14151/intelligent--news-monitor.git
```

**2. Enter the project**

```bash
cd intelligent--news-monitor
```

**3. Create or switch to your branch**

```bash
git checkout feature/agent-validation
```

If the branch does not exist yet on the remote:

```bash
git checkout -b feature/agent-validation
```

**4. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**5. Open and edit your main file**

```
backend/app/agents/validation.py
```

**6. Test your work**

```bash
python -m pytest tests/test_agent_contracts.py
```

**7. Check your changes**

```bash
git status
```

**8. Commit**

```bash
git add .
git commit -m "Implement context validation agent"
```

**9. Push ONLY your branch**

```bash
git push -u origin feature/agent-validation
```

**10. Open a Pull Request on GitHub**

Go to the repository on GitHub and open a Pull Request from `feature/agent-validation` into `main`.

---

## MEMBER 3 — Story Clustering Agent

**Owner:** Ajay Krithick S V  
**Branch:** `feature/agent-clustering`  
**Pipeline:** `validated_articles -> stories`  
**Main file:** `backend/app/agents/clustering.py`

### Responsibility

Your agent should:
- Group articles that cover the same event or story
- Detect semantic similarity between articles
- Create story clusters
- Avoid treating every article as a separate story
- Return structured story objects
- Preserve article and source information within each cluster
- Do NOT modify other members' agent logic

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/kamesh14151/intelligent--news-monitor.git
```

**2. Enter the project**

```bash
cd intelligent--news-monitor
```

**3. Create or switch to your branch**

```bash
git checkout feature/agent-clustering
```

If the branch does not exist yet on the remote:

```bash
git checkout -b feature/agent-clustering
```

**4. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**5. Open and edit your main file**

```
backend/app/agents/clustering.py
```

**6. Test your work**

```bash
python -m pytest tests/test_agent_contracts.py
```

**7. Check your changes**

```bash
git status
```

**8. Commit**

```bash
git add .
git commit -m "Implement story clustering agent"
```

**9. Push ONLY your branch**

```bash
git push -u origin feature/agent-clustering
```

**10. Open a Pull Request on GitHub**

Go to the repository on GitHub and open a Pull Request from `feature/agent-clustering` into `main`.

---

## MEMBER 4 — Importance Analysis Agent

**Owner:** Dev M K  
**Branch:** `feature/agent-importance`  
**Pipeline:** `stories -> scored_stories`  
**Main file:** `backend/app/agents/importance.py`

### Responsibility

Your agent should:
- Analyze how important each story is
- Consider factors such as impact, urgency, credibility, and relevance
- Generate impact signals (scores)
- Produce an importance and priority score
- Classify stories appropriately (LOW / MEDIUM / HIGH / CRITICAL)
- Return structured scored story data
- Do NOT modify other members' agent logic

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/kamesh14151/intelligent--news-monitor.git
```

**2. Enter the project**

```bash
cd intelligent--news-monitor
```

**3. Create or switch to your branch**

```bash
git checkout feature/agent-importance
```

If the branch does not exist yet on the remote:

```bash
git checkout -b feature/agent-importance
```

**4. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**5. Open and edit your main file**

```
backend/app/agents/importance.py
```

**6. Test your work**

```bash
python -m pytest tests/test_agent_contracts.py
```

**7. Check your changes**

```bash
git status
```

**8. Commit**

```bash
git add .
git commit -m "Implement importance analysis agent"
```

**9. Push ONLY your branch**

```bash
git push -u origin feature/agent-importance
```

**10. Open a Pull Request on GitHub**

Go to the repository on GitHub and open a Pull Request from `feature/agent-importance` into `main`.

---

## MEMBER 5 — Summary Agent

**Owner:** Kamesh  
**Branch:** `feature/agent-summary`  
**Pipeline:** `scored_stories -> summaries`  
**Main file:** `backend/app/agents/summary.py`

### Responsibility

Your agent should:
- Read each scored story
- Generate a concise and useful summary
- Include the most important facts
- Avoid unnecessary repetition
- Keep the summary grounded in the provided articles (no invented facts)
- Produce structured summary output matching the shared schema
- Do NOT modify other members' agent logic

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/kamesh14151/intelligent--news-monitor.git
```

**2. Enter the project**

```bash
cd intelligent--news-monitor
```

**3. Create or switch to your branch**

```bash
git checkout feature/agent-summary
```

If the branch does not exist yet on the remote:

```bash
git checkout -b feature/agent-summary
```

**4. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**5. Open and edit your main file**

```
backend/app/agents/summary.py
```

**6. Test your work**

```bash
python -m pytest tests/test_agent_contracts.py
```

**7. Check your changes**

```bash
git status
```

**8. Commit**

```bash
git add .
git commit -m "Implement summary agent"
```

**9. Push ONLY your branch**

```bash
git push -u origin feature/agent-summary
```

**10. Open a Pull Request on GitHub**

Go to the repository on GitHub and open a Pull Request from `feature/agent-summary` into `main`.

---

## Files You Must NOT Modify

The following files are controlled by the team lead (Kamesh). Do not edit them unless explicitly approved:

```
backend/app/graph/state.py
backend/app/graph/workflow.py
backend/app/schemas/news.py
backend/app/rules/engine.py
docker-compose.yml
```

---

## Quick Reference — Git Commands

| Action | Command |
|--------|---------|
| Check current branch | `git branch` |
| Check what changed | `git status` |
| Stage all changes | `git add .` |
| Commit with message | `git commit -m "your message"` |
| Push your branch | `git push -u origin <your-branch>` |
| Pull latest from main | `git pull origin main` |
| See recent commits | `git log --oneline -10` |

---

## Pull Request Checklist

Before opening a Pull Request, confirm:

- [ ] Your agent file is edited and saved
- [ ] Tests pass: `python -m pytest tests/test_agent_contracts.py`
- [ ] You have committed your changes
- [ ] You pushed to your own branch, not `main`
- [ ] PR title follows the format: `feat: implement <agent-name> agent`
- [ ] PR description explains what you changed and how it works

---

*Team Lead: Kamesh — controls main branch, schemas, workflow, and deployment.*
