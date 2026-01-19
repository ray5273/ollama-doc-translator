# Translation Test: Microservice Deployment Practice
This document is used as an internal training material. It is unrelated to actual products and intentionally includes various writing styles and technical terms.

In this scenario, the following goals and environment are assumed.
- Goal: Deploy and observe the operation of a training microservice bundle on a simulation server.
- Environment: The `orion-stack` image exists in the local registry, and the learning control node is accessible at the address `192.168.10.77`.

> **Practice Notes**
> - The provided commands are examples, and you should modify them to match your team's environment, including whether to use `sudo` and the path.
> - All REST calls assume the use of self-signed certificates, including the `-k` option.

## 1. Preparation Checklist
Before starting the deployment practice, verify the following items.

1. Record the image version and hash.
2. Activate the test virtual environment in the shell.
3. Clear the log collection directory and prepare a new session.

```bash
$ source ~/virtualenvs/deploy-lab/bin/activate
$ docker images | grep orion-stack
$ rm -rf ~/lab-logs/*
```

## 2. Sandbox Status Check
Before starting the service, check the status of the container, service, and storage.

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
1. Upload and verify the signing value.
2. Register configuration changes in `lab-api` using the REST API.
3. Start the actual container in the `lab-agent` service.

```bash
$ curl -k -X POST \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{"stage": "upload", "bundle": "orion-stack:training"}' \
'https://192.168.10.77/api/v1/lab/deploy'
```

During deployment, collect messages using the `journalctl -u lab-agent -f` command, and immediately record any specific error codes in the practice notes.

## 4. Status Observation and Log Collection
The following table shows examples of key status items that learners should record.

| Category | Check Command | Expected Value |
|---|---|---|
| Service Response | `curl -k https://192.168.10.77/healthz` | `{"status":"ok"}` |
| Container Count | `docker ps -q | wc -l` | 6 |
| CPU Usage | `mpstat 1 1` | 75% or less |

## 5. Shutdown and Recovery
After the practice, clean up the resources using the following procedure.

```bash
$ systemctl stop lab-api
$ systemctl stop lab-agent
$ docker system prune -f
```

The shutdown logs are saved in the `~/lab-logs/shutdown-$(date +%Y%m%d).log` file, and the results are shared with the team channel for the next practice.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**