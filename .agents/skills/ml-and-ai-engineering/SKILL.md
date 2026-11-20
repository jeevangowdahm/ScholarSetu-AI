---
name: ml-and-ai-engineering
description: Machine learning and modern LLM application engineering. Retrieval-Augmented Generation (RAG), vector embeddings, semantic search, prompt conditioning, and hallucination reduction.
---

# ML & AI Engineering Skill

## 1. Retrieval-Augmented Generation (RAG) Architecture
1. **Document Chunking**: Split domain knowledge into semantic chunks with 10-15% token overlap.
2. **Dense Retrieval**: Embed queries using vector models (e.g., text-embedding-004) and match with cosine similarity.
3. **Re-Ranking**: Use cross-encoders or keyword filters to re-score candidates before injecting them into the LLM context.
4. **Context Injection**: Constrain LLM responses strictly to the grounded retrieved documents to eliminate false generation.

## 2. Prompt Conditioning Strategies
- **System Role Anchoring**: Clearly specify identity, tone, domain boundaries, and prohibited behaviors.
- **Few-Shot In-Context Learning**: Provide 2-3 input-output exemplar pairs illustrating desired markdown structure and tone.
- **Guardrails**: Instruct the model to gracefully output a predefined disclaimer when queried outside its grounded domain.
