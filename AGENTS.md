# AGENTS

## Project context
- Goal: Build a two-node Proxmox + Kubernetes AI service mesh demo that is portable to AWS EKS.
- Hardware: 2x Optiplex (i5-8500T, 16GB RAM, 256GB SSD), CPU-only.
- Focus: traffic splitting, autoscaling, and observability for 2–3 FastAPI services.

## Preferences
- Use uv for Python package management when appropriate.
- Use git for version control
- Use the GitHub gh CLI for creating pull requests.
- Keep local changes minimal and incremental.

## Tooling
- Use ruff for linting and formatting.
- Use pre-commit for hook management.
- Use mypy or pyright for type checking when helpful.
- Use docker compose for local testing.
- Use terraform fmt and tflint for infrastructure code.

## Constraints
- Do not create or initialize a git repository.
- Never commit `plan.md` or the `instructions/` directory.
- Keep outputs concise; avoid large pasted files unless requested.
- Assume network access is restricted unless explicitly allowed.
