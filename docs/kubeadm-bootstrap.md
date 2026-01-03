# Kubernetes Bootstrap (kubeadm)

This document captures a minimal kubeadm bootstrap flow for the two-node demo.

## 1) Base Packages (Both VMs)
- Install containerd and kubeadm/kubelet/kubectl.
- Disable swap and apply sysctl settings for bridging.

## 2) Initialize Control Plane (k8s-cp-1)
- Run kubeadm init with a Pod CIDR (Calico-friendly):
  - `--pod-network-cidr=192.168.0.0/16`
- Configure kubeconfig for kubectl access.

## 3) Join Worker (k8s-w-1)
- Use the kubeadm join command from the control plane.

## 4) Install CNI (Calico)
- Apply the Calico manifest.

## Validation Checklist
- `kubectl get nodes` shows both nodes Ready.
- `kubectl get pods -A` shows CNI pods running.

## Notes
- Keep the kubeadm init/join command output in a secure location for repeatable builds.
