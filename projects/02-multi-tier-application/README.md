# Projects 2 and 3: Multi-Tier App, Production-Style Deployment

## Overview and use case
A small "shop visits" app: browser -> Ingress -> nginx frontend -> Flask API -> Postgres.
It models the classic three-tier web app you would migrate to Kubernetes: stateless tiers behind Services, one stateful database on a persistent volume, and config/credentials kept out of images.
Covers Project 2 (multi-tier) and Project 3 (probes, limits, namespace, Ingress).

## Architecture
~~~mermaid
flowchart LR
  C[Client] --> I[Ingress shop.local]
  I --> F[frontend x2 - nginx-unprivileged]
  F -->|/api| B[backend x2 - Flask + gunicorn]
  B --> D[(postgres-0 - StatefulSet + 1Gi PVC)]
~~~

## Tools
Minikube (Docker driver), kubectl, Docker, Flask/gunicorn/psycopg, Postgres 16, nginx-unprivileged, ingress-nginx addon.

## Kubernetes concepts
Namespace, StatefulSet + volumeClaimTemplates, headless Service, ConfigMap (env and files), Secret, liveness vs readiness probes, requests/limits, Ingress, rolling updates.

## Prerequisites
Running Minikube with the ingress addon (`minikube addons enable ingress`) and Docker.

## Structure
    backend/      Flask API source + Dockerfile
    frontend/     index.html and nginx default.conf (source for the ConfigMap)
    manifests/    00 namespace, 10 postgres, 20 backend, 30-31 frontend, 40 ingress
    screenshots/  captured cluster output

## Deploy (run from this directory)
    kubectl apply -f manifests/00-namespace.yaml
    kubectl -n shop create secret generic postgres-secret --from-literal=POSTGRES_PASSWORD="$(openssl rand -hex 16)"
    docker build -t shop-api:1.0 backend/ && minikube image load shop-api:1.0
    kubectl apply -f manifests/
    kubectl -n shop rollout status statefulset/postgres
    kubectl -n shop rollout status deploy/backend
    kubectl -n shop rollout status deploy/frontend

To change the frontend files, regenerate the ConfigMap and restart (subPath mounts do not live-update):

    kubectl -n shop create configmap frontend-config --from-file=frontend/index.html --from-file=frontend/default.conf --dry-run=client -o yaml > manifests/30-frontend-config.yaml
    kubectl -n shop rollout restart deploy/frontend

## Test
    kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8082:80 &
    curl -s -H 'Host: shop.local' localhost:8082/api/visits

Expected: JSON like {"pod":"backend-...","visits":N}; N keeps increasing and the pod name varies.

## Configuration notes
- Postgres: StatefulSet with a headless Service (DNS returns the Pod IP) and a 1Gi PVC per replica.
- Backend: DB host/name/user from a ConfigMap; password from the Secret. Liveness /healthz (no DB), readiness /ready (checks DB).
- Frontend: nginx-unprivileged on 8080, config and page mounted from a ConfigMap; proxies /api/ to the backend Service by DNS name.
- Every container has requests and limits.

## Troubleshooting and lessons (observed)
- Deleting postgres-0 and scaling the StatefulSet to 0 kept the data (PVC survives).
- DB down: backends went 0/1 with 0 restarts (readiness checks the DB, liveness does not). With zero DB Pods, the headless Service has no DNS records.
- Rotated the Secret without updating the DB: new Pods stayed 0/1, the rollout stalled, old Pods kept serving. The Postgres image applies POSTGRES_PASSWORD only on first init. The error was visible only in the /ready body, so log errors in the app. Safe rotation: add the new credential to the DB first, then the Secret, then roll, then revoke the old one.
- kubectl port-forward bypasses readiness; subPath mounts do not auto-update.

## Security considerations
Done: password generated at deploy time and never in Git; backend runs as uid 10001 and the frontend uses an unprivileged image; limits set.
Known gaps (addressed in Module 9): Secret is only base64; password passed as an env var; no NetworkPolicy; no TLS on the Ingress; no securityContext hardening; single DB replica and no backups; locally built image is not scanned.

## Evidence
screenshots/shop-resources.txt is the real `kubectl get` output from the cluster.

## Cleanup
    kubectl delete namespace shop     # also deletes the PVC and its data
    kubectl config set-context --current --namespace=default
