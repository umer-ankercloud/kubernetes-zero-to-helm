# Learning Journal

## Module 1: Architecture (2026-11-02)
- Learned: control plane vs node components; reconciliation loop.
- Commands: get nodes/pods -o wide, explain, api-resources, describe, minikube ssh.
- Issue: checked node 28s after start, saw NotReady. It was CNI still starting; `kubectl wait` fixed it.
- Revisit: RBAC flags (M7), probes (M5).
