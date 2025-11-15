# Translation Test: Microservices Deployment Rehearsal
This document is a translation test document intended for internal training purposes. It is unrelated to actual products and intentionally includes a mix of various styles and technical terms.

This scenario assumes the following goals and environments:
- **Goal**: Simulate deploying a training microservices bundle to a simulated server and observe its operation.
- **Environment**: The `orion-stack` image exists in the local repository, and a training control node is accessible at the address `192.168.10.77`.

> **Practice Notes**
> - Guided commands are examples; adjust `sudo` usage and paths according to your team environment.
> - Assume all REST calls use a self-signed certificate and include the `-k` option accordingly.

## 1. Preparation Checklist
Before starting the deployment rehearsal, verify the following items:

1. Record the image version and hash.
2. Activate a test virtual environment in the shell.
3. Clear the log collection directory and prepare for a new session.

```bash
$ source ~/virtualenvs/deploy-lab/bin/activate
$ docker images | grep orion-stack
$ rm -rf ~/lab-logs/*
```

## 2. Sandbox Status Diagnosis
Inspect the container, service, and storage statuses before initiating services.

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

## 3. Deployment Scenario Execution
1. Upload artifacts and verify signatures.
2. Register configuration changes via the `lab-api` REST API.
3. Start actual containers using the `lab-agent` service.

```bash
$ curl -k -X POST \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{"stage": "upload", "bundle": "orion-stack:training"}' \
'https://192.168.10.77/api/v1/lab/deploy'
```

During deployment, collect messages using the `journalctl -u lab-agent -f` command; immediately record specific error codes in the practice notes if they occur.

## 4. Status Observation and Log Collection
The following table provides examples of key status items that learners should record:

| Category       | Verification Command         | Expected Value         |
|----------------|------------------------------|------------------------|
| Service Response | `curl -k https://192.168.10.77/healthz` | `{"status":"ok"}`     |
| Number of Containers | `docker ps -q | wc -l` | 6                      |
| CPU Utilization | `mpstat 1 1`                | ≤ 75%                  |

## 5. Cleanup and Recovery
After completing the practice, follow these steps to clean up resources:

```bash
$ systemctl stop lab-api
$ systemctl stop lab-agent
$ docker system prune -f
```

Shutdown logs are saved in the file `~/lab-logs/shutdown-$(date +%Y%m%d).log`, and summarize results for sharing with the team channel for the next session.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**