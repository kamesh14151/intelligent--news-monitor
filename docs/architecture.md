# Agent Architecture

```text
                 RSS / APIs / Websites
                          |
                          v
                   Data Ingestion
                          |
                          v
               +----------------------+
               | Member 1             |
               | Semantic Discovery   |
               +----------+-----------+
                          |
                          v
               +----------------------+
               | Member 2             |
               | Context Validation   |
               +----------+-----------+
                          |
                          v
               +----------------------+
               | Member 3             |
               | Story Clustering     |
               +----------+-----------+
                          |
                          v
               +----------------------+
               | Member 4             |
               | Importance Analysis  |
               +----------+-----------+
                          |
                          v
               +----------------------+
               | Member 5             |
               | Summary Agent        |
               +----------+-----------+
                          |
                          v
                    Rule Engine
                          |
                    +-----+-----+
                    |           |
                    v           v
                Database      Alerts
                    |
                    v
                Dashboard
```

The current codebase may contain helper functions for topic/impact analysis. Treat the five member-owned agents above as the five team boundaries. Member 4 owns the importance decision and may call helpers internally.
