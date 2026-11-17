# kubectl cheat sheet (commands I have actually used)

## Context and cluster
    kubectl config current-context
    kubectl config set-context --current --namespace=<ns>
    kubectl get nodes -o wide
    kubectl get pods -A
    kubectl api-resources
    kubectl explain pod.spec.containers

## Create and update (declarative first; the file in Git is the truth)
    kubectl apply -f file.yaml
    kubectl apply --dry-run=client -f file.yaml
    kubectl create deployment web --image=nginx --replicas=3 --dry-run=client -o yaml > deployment.yaml
    kubectl create secret generic NAME --from-literal=KEY="$(openssl rand -hex 16)"
    kubectl create configmap NAME --from-file=a --from-file=b --dry-run=client -o yaml
    kubectl delete -f file.yaml

## Rollouts and scaling
    kubectl rollout status deploy/NAME
    kubectl rollout history deploy/NAME
    kubectl rollout undo deploy/NAME
    kubectl rollout restart deploy/NAME
    kubectl scale deploy/NAME --replicas=N

## Inspect and debug
    kubectl get deploy,rs,pods -l app=NAME -o wide
    kubectl describe pod POD                  # read Events first
    kubectl get events --sort-by=.lastTimestamp
    kubectl logs POD --previous               # logs of the crashed container
    kubectl logs -l app=NAME
    kubectl exec -it POD -- sh
    kubectl get endpointslices -l kubernetes.io/service-name=SVC
    kubectl port-forward svc/NAME 8080:80
    kubectl run tmp --image=curlimages/curl:8.10.1 --restart=Never --rm -i -- curl -s http://SVC
    kubectl wait --for=condition=Ready pod/NAME --timeout=60s

## Symptom -> first command
| Symptom | First look |
|---|---|
| ErrImagePull / ImagePullBackOff | describe pod -> Events (bad tag or registry) |
| Service does nothing | get endpointslices (selector, targetPort) |
| Running but 0/1 | describe pod -> readiness probe failure |
| RESTARTS climbing | describe pod -> Events; logs --previous |
| Pending | describe pod (Insufficient cpu) or describe pvc (unbound claim) |
| OOMKilled / 137 | describe pod -> Last State |
| CreateContainerConfigError | describe pod (missing Secret/ConfigMap) |
| Ingress 404 / 503 | describe ingress; curl with Host header |
