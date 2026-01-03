# Proxmox Base Setup (Two Nodes)

This document keeps the Proxmox steps reproducible and minimal for a two-node demo.

## 1) Install Proxmox
- Use the Proxmox VE ISO on both Optiplex nodes.
- Assign static IPs or reserved DHCP leases.

## 2) Network Bridge
- Configure a Linux bridge (e.g., `vmbr0`) on each host.
- Attach both VMs to the same bridge for L2 connectivity.

## 3) Storage Layout (MVP)
- Keep defaults for a simple local install.
- Allocate enough space for a 120GB VM disk on each host.

## 4) Create VMs
- Create one VM per host:
  - `k8s-cp-1` (control-plane)
  - `k8s-w-1` (worker)
- Sizing: 4 vCPU, 12GB RAM, 120GB disk.
- OS: Ubuntu 22.04 LTS.

## 5) Record VM IPs
- Record the IPs of each VM for kubeadm bootstrap.

## Validation Checklist
- Both VMs can ping each other.
- Both VMs can reach the Internet for package installs.
