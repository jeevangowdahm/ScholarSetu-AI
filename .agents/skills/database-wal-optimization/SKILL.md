---
name: database-wal-optimization
description: High-performance SQLite and relational database optimization. Write-Ahead Logging (WAL), transaction concurrency, PRAGMA tuning, indexes, and zero-downtime backups.
---

# Database WAL Optimization Skill

## 1. SQLite High-Concurrency Configuration
For multi-threaded or multi-process web applications:
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
PRAGMA cache_size = -64000; -- 64MB memory cache
PRAGMA foreign_keys = ON;
```

## 2. Performance Query Profiling
- Run `EXPLAIN QUERY PLAN SELECT ...` to ensure all WHERE and ORDER BY clauses utilize indexes rather than full table scans (`SCAN TABLE`).
- Use composite indexes for multi-column filtering: `CREATE INDEX idx_name ON table(col1, col2);`.
- Automated online backup: use SQLite online backup API (`backup(dest_db)`) to snapshot state without locking readers.
