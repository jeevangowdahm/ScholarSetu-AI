---
name: data-pipeline-etl
description: Building resilient data ingestion and ETL pipelines. Covers stream and batch processing, data normalization, deduplication, backpressure, and fault-tolerant retry loops.
---

# Data Pipeline ETL Skill

## 1. Pipeline Phases
1. **Extract**: Ingest structured and unstructured data from heterogeneous sources (APIs, CSV, databases, PDF scrapers).
2. **Transform**: Normalize strings, strip trailing spaces, convert currencies to integers, enforce standardized ISO dates.
3. **Deduplicate**: Compute SHA-256 hashes of composite key attributes to discard duplicate ingestion records.
4. **Load**: Execute batch inserts inside an atomic database transaction.

## 2. Fault Tolerance
- Implement exponential backoff retry loops (`delay = base * 2^attempt`) for transient network calls.
- Write failed records to a Dead Letter Queue (DLQ) with timestamp and error reason for auditing.
