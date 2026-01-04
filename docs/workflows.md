# Demo Workflows

Use these flows to tell a coherent story during demos or interviews.

## 1) RAG-Lite Answering
1. `/rag-lite` on the gateway with a user question.
2. Embedding + retrieval against a local corpus.
3. LLM answers using only the top-K snippets.

Talking points:
- Local data stays local.
- Deterministic retrieval + generative answer.
- Portability to EKS with minimal changes.

## 2) Document Similarity + Summary
1. `/compare` with two text inputs.
2. Cosine similarity on embeddings.
3. LLM returns a summary (style/format configurable) with highlights.

Talking points:
- Embedding-based similarity.
- Simple explainable score + narrative.

## 3) Image Caption (CNN + LLM)
1. `/caption` with a base64 image.
2. CNN returns top-K labels.
3. LLM composes a caption from labels (style/length configurable).

Talking points:
- Pretrained CNN, no training required.
- Multimodal pipeline on CPU-only hardware.

## 4) Semantic Routing
1. `/route` with a user query.
2. Embeddings pick the best route (overview, observability, or EKS porting).
3. LLM answers using route-specific context.

Talking points:
- Embedding-driven routing.
- Modular answers with scoped context.
