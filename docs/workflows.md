# Demo Workflows

Use these flows to tell a coherent story during demos or interviews.

## 1) Safety Triage (Text)
1. `/predict` on the gateway with a user text.
2. Embedding + classifier scores confidence.
3. Eval enforces a threshold for pass/fail.
4. `/generate` produces a short explanation or summary.

Talking points:
- CPU-only inference.
- Simple policy gating on model output.
- Clear API boundaries for auditability.

## 2) Multimodal Risk Check (Image + Text)
1. `/classify-image` with a base64 image.
2. Top-K labels returned from the CNN.
3. Operator or rule engine decides whether to proceed.
4. Optional `/generate` to create a human-readable note.

Talking points:
- Pretrained CNN without training.
- Lightweight, portable inference on Proxmox.
- Separation of perception and policy.

## 3) RAG-Lite Answering
1. `/embedding` for a user question.
2. Retrieve top-K snippets from a small local corpus.
3. `/generate` produces a short answer using the snippets.

Talking points:
- Private data stays local.
- Portability to EKS with minimal changes.
