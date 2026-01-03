# AI Service Mesh Demo (Proxmox + EKS)

This repo hosts a two-node, CPU-only Kubernetes service mesh demo that runs on Proxmox and ports cleanly to AWS EKS. The goal is to showcase traffic splitting, autoscaling, and observability across 2–3 FastAPI services.

## Goals
- Portable Kubernetes stack: Proxmox now, EKS later
- Linkerd-based traffic splitting and mTLS
- HPA-driven autoscaling with observable metrics
- Minimal changes between local and cloud deployments

## Repository Layout
- charts/ : Helm chart(s) and environment-specific values
- services/ : FastAPI services and gateway
- infra/ : Terraform and supporting scripts
- docs/ : diagrams, demo script, and screenshots

## Next Steps
1. Define the base Helm chart scaffold and values structure.
2. Sketch service interfaces and resource budgets for the 2–3 APIs.
3. Draft the demo flow (traffic split + HPA + metrics).

## Testing
Local and Docker-based testing options are documented in `docs/testing.md`.

## Linkerd
Local setup and verification steps are in `docs/linkerd-setup.md`.
Smoke test for namespace injection is in `docs/linkerd-injection-smoke.md`.
Traffic split (canary) demo is in `docs/linkerd-traffic-split.md`.

## Project Plan
The detailed plan is in `plan.md`.
