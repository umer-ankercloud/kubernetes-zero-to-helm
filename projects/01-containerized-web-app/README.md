# Project 1: Containerized Web App

Deploy nginx with a bare Pod, then a Deployment: scaling, rolling update, failure, rollback.

~~~mermaid
flowchart LR
  D[Deployment web] --> RS[ReplicaSet] --> P1[Pod] & P2[Pod] & P3[Pod]
~~~

## Concepts
Pod, ReplicaSet, Deployment, desired state, rolling update, rollback, ImagePullBackOff.

## Run it (from this directory)
    kubectl apply -f manifests/pod.yaml
    kubectl apply -f manifests/deployment.yaml
    kubectl get deploy,rs,pods -l app=web

## Lessons
- Bare Pods are not recreated; Deployments self-heal.
- A bad image stalls the rollout without taking down healthy Pods.
- `kubectl set image` drifts from the YAML; keep the file as the source of truth.
- Deployment selector must match template labels, and is immutable.

## Cleanup
    kubectl delete -f manifests/deployment.yaml
