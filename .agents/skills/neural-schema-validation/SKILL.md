---
name: neural-schema-validation
description: Deterministic runtime data validation using Pydantic, Zod, and JSON Schema. Enforces strict type boundaries, serialization, and structured LLM tool outputs.
---

# Neural Schema Validation Skill

## 1. Runtime Schema Enforcers
- Validate all incoming payloads at API boundaries using strict types.
- Ensure type coercion is explicit rather than implicit.
- Provide descriptive validation error messages identifying the exact invalid field and violation rule.

## 2. LLM Structured Outputs
- When requesting JSON from LLMs, pass a JSON Schema definition (`response_format: { type: "json_object" }`) and validate the output against a Pydantic/Zod model before consuming it in business logic.
