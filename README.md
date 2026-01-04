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
- docs/ : diagrams, demo script, and screenshots

## Status
- Base Helm chart and values are in place.
- Services + gateway are implemented with real ML endpoints.
- Demo flow is documented and testable.

## Testing
Local and Docker-based testing options are documented in `docs/testing.md`.

## Linkerd
Local setup and verification steps are in `docs/linkerd-setup.md`.
Smoke test for namespace injection is in `docs/linkerd-injection-smoke.md`.
Traffic split (canary) demo is in `docs/linkerd-traffic-split.md`.
Viz dashboard screenshot steps are in `docs/linkerd-viz-dashboard.md`.

## Autoscaling
HPA demo steps are in `docs/hpa-demo.md`.

## Architecture
Architecture overview is in `docs/architecture.md`.

## Storage
Local-path storage notes are in `docs/storage.md`.

## Observability
Prometheus + Grafana setup steps are in `docs/observability-setup.md`.

## Networking + Resource Isolation
The demo uses Linkerd mTLS and NetworkPolicy for service-level isolation, plus ResourceQuota and
LimitRange to enforce namespace resource budgets. See `charts/ai-service-mesh/README.md` for
configuration details and `docs/testing.md` for verification steps.

## Demo Script
The demo flow is in `docs/demo-script.md`.

## Demo Workflows
Suggested end-to-end workflows are in `docs/workflows.md`.

## EKS Porting
Minimal values diff and EKS notes are in `docs/eks-porting.md`.

## Project Plan
The detailed plan is in `plan.md`.
