# Troubleshooting Guide (grows each module)
| Symptom | Where to look | Cause seen in labs |
|---|---|---|
| ErrImagePull / ImagePullBackOff | describe pod -> Events | Bad image tag |
| Service does nothing | get endpointslices | Selector mismatch (ENDPOINTS <unset>), wrong targetPort |
| CreateContainerConfigError | describe pod -> Events | Missing Secret/ConfigMap |
| Running but 0/1 | describe pod, endpointslices (ready=false) | Failing readiness probe (no restart, no traffic) |
| RESTARTS climbing | describe pod -> Events | Failing liveness probe ("will be restarted") |
| OOMKilled / exit 137 | describe pod -> Last State | Memory limit exceeded (SIGKILL) |
| Pending + Insufficient cpu | get events | Requests exceed free node capacity |
