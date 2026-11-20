---
name: conversational-chatbot
description: Conversational AI and chatbot development for production apps. Covers dialog state machines, intent detection, empathetic tone, quick-reply chips, and prompt injection defense.
---

# Conversational Chatbot Skill

## 1. Chatbot Architecture
- **Multi-Turn State Tracking**: Maintain session history (user/assistant turns) while trimming oldest turns to preserve the context window.
- **Intent Disambiguation**: Categorize incoming queries into:
  - *Direct Scheme Inquiries* -> Trigger schema-grounded facts.
  - *Eligibility Screening* -> Guide student through profile parameters.
  - *Process / Documentation* -> Return checklists and portal URLs.
  - *Out-of-Scope* -> Politely redirect to core welfare mission.
- **Interactive Quick-Reply Chips**: Accompany every response with 3-4 contextual suggestions to keep the conversation flowing.

## 2. Jailbreak & Prompt Injection Defense
- Never concatenate unvalidated user text into raw instruction strings.
- Enforce strict system instructions and use boundary delimiters (`"""..."""` or XML tags `<user_query>...</user_query>`).
