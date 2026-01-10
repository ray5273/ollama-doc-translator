# Translation Test: Virtual Box Initialization Procedure
This document describes a hypothetical scenario for initializing a virtual box created by the QA team to check translation quality.

## 1. Initial Check
- Lab Name: `orion-mini`
- Management IP: `172.30.11.20`
- Status Check Command:
```bash
$ curl -k https://172.30.11.20/api/v1/lab/status
```

## 2. Preparation Steps
| Step | Description |
|------|-------------|
| 1 | Validate Test Image |
| 2 | Backup Configuration |
| 3 | Clean Log Directories |

## 3. Initialization Command
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"mode": "training", "resetLogs": true}' \
'https://172.30.11.20/api/v1/lab/init'
```

## 4. Tracking Progress
- `watch -n2 "curl -ks https://172.30.11.20/api/v1/lab/progress"`
- `journalctl -u lab-reset -f`

## 5. Completion Verification
Once initialization is complete, check the following items:
1. Has a new session folder been created inside `/var/log/lab-reset`?
2. Is `systemctl status lab-core` in `active (running)` state?
3. Verify that the `phase` value in the REST response is `READY`.

## 6. Post-Initialization Tasks
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"command": "seed-data"}' \
'https://172.30.11.20/api/v1/lab/tasks'
```

## 7. Reporting
- The participant records the results in the `docs/reports/box-init-template.md` file.
- If any issues arise, attach logs to an inquiry at `lab-support@example.com`.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**