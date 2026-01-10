# Translation Test: Microservices Deployment Simulation
This document is a translation test document intended for internal training purposes. It is intentionally constructed with a mix of various styles and technical terms, unrelated to actual products.

In this scenario, we assume the following goals and environment:
- Goal: Deploy a training microservices bundle to a simulated server and observe its operation.
- Environment: The `orion-stack` image exists in the local repository, and a training control node is accessible at `192.168.10.77`.

> **Practice Notes**
> - The guided commands are examples; adjust for `sudo` and paths according to your team environment.
> - Assume all REST calls use a self-signed certificate and include the `-k` option.

## 1. Preparation Checklist
Before starting the deployment rehearsal, verify the following items:

1. Record the image version and hash.
2. Activate the test virtual environment in the shell.
3. Clear the log collection directory and prepare a new session.

```bash
$ source ~/virtualenvs/deploy-lab/bin/activate
$ docker images | grep orion-stack
$ rm -rf ~/lab-logs/*
```

## 2. Sandbox State Diagnostics
Before starting the services, check the status of containers, services, and storage.

### 2.1 Service Status
```bash
$ systemctl status lab-agent
$ systemctl status lab-api
```

### 2.2 Container List
```bash
$ docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

### 2.3 Storage Summary
```bash
$ df -h /var/lib/orion
```

## 3. Execution of Deployment Scenario
1. Upload the artifact and verify the signature.
2. Register configuration changes with `lab-api` using the REST API.
3. Start the actual containers in the `lab-agent` service.

```bash
$ curl -k -X POST \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{"stage": "upload", "bundle": "orion-stack:training"}' \
'https://192.168.10.77/api/v1/lab/deploy'
```

During deployment, collect messages with the command `journalctl -u lab-agent -f`, and immediately record any specific error codes in the practice notes.

## 4. Observation of State and Log Collection
The following table provides examples of key state items that learners should record.

| Category | Command | Expected Value |
|----------|---------|----------------|
| Service Response | `curl -k https://192.168.10.77/healthz` | `{"status":"ok"}` |
| Container Count | `docker ps -q | wc -l` | 6 |
| CPU Utilization | `mpstat 1 1` | Below 75% |

## 5. Cleanup and Recovery
After completing the practice, follow these steps to clean up resources.

```bash
$ systemctl stop lab-api
$ systemctl stop lab-agent
$ docker system prune -f
```

Save the termination logs to a file `~/lab-logs/shutdown-$(date +%Y%m%d).log`, and share a summary of the results with the team channel for the next practice.

[TRANSLATION_END]

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**