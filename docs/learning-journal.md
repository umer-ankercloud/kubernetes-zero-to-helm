# Learning Journal

## Module 1: Architecture (2026-11-02)
- Learned: control plane vs node components; reconciliation loop.
- Commands: get nodes/pods -o wide, explain, api-resources, describe, minikube ssh.
- Issue: checked node 28s after start, saw NotReady. It was CNI still starting; `kubectl wait` fixed it.
- Revisit: RBAC flags (M7), probes (M5).

## Module 2: Pods, ReplicaSets, Deployments (2026-11-02)
- Learned: Deployment -> ReplicaSet -> Pods; self-healing; rolling update; rollback.
- Commands: apply, get deploy,rs,pods, set image, rollout status/history/undo, describe pod, port-forward.
- Problem: image tag nginx:doesnotexist -> ErrImagePull -> ImagePullBackOff. Rollout stalled, old Pods kept serving. Fixed with rollout undo.
- Takeaway: imperative changes (set image, undo) cause drift from the YAML; edit the file and apply instead.
- Revisit: rollout history shows CHANGE-CAUSE <none>.
- Problem: selector/template label mismatch is rejected by the API (selector is immutable). Saved as labs/02-deployments/selector-mismatch.yaml.
