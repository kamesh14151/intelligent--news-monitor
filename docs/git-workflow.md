# Git Workflow for the 5-Member Team

## Branch map

```text
main
├── feature/agent-discovery
├── feature/agent-validation
├── feature/agent-clustering
├── feature/agent-importance
└── feature/agent-summary
```

## Important clarification

`feature/agent-discovery` is a **Git branch name**, not a folder. Do not create five copies of the whole application. Every member branches from the same `main` codebase and owns one agent file.

## First-time setup

```bash
git clone <REPO_URL>
cd intelligent-news-monitor-team
git fetch --all
```

## Before coding

```bash
git checkout main
git pull origin main
git checkout feature/agent-discovery
```

Replace the branch name with your assigned branch.

## During coding

```bash
git status
git add .
git commit -m "feat: improve discovery relevance scoring"
git push
```

## Pull Request rule

Never merge directly into `main`. Open a PR and let the integration owner review it.

## If main changed while you were working

```bash
git checkout main
git pull origin main
git checkout feature/agent-discovery
git merge main
```

Resolve conflicts carefully. If the conflict is in shared state/schema/workflow files, ask the integration owner before changing the contract.
