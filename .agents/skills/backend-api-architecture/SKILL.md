---
name: backend-api-architecture
description: RESTful API design, HTTP status codes, standard JSON envelopes, idempotency, JWT/session authentication, rate limiting, and CORS security.
---

# Backend API Architecture Skill

## 1. REST Standards
- **Envelopes**: Consistent API response envelopes:
  ```json
  { "success": true, "data": { ... }, "meta": { "count": 1, "page": 1 } }
  ```
  Error envelope:
  ```json
  { "success": false, "error": { "code": "INVALID_PARAMETER", "message": "..." } }
  ```
- **HTTP Verbs**: GET for read-only, POST for creation, PUT/PATCH for mutation, DELETE for removal.
- **Security Headers**: HSTS, CSP, X-Content-Type-Options, X-Frame-Options.
- **Brute-Force Rate Limiting**: Track client IP failure counts with exponential backoff and lockout thresholds.
