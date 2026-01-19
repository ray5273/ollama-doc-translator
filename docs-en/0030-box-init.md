# Translation Test: Virtual Box Initialization Procedure
This document describes a hypothetical virtual box initialization scenario created by the QA team to check translation quality.

## 1. Initial Check
- Lab equipment name: `orion-mini`
- Management IP: `172.30.11.20`
- Status query command:
```bash
$ curl -k https://172.30.11.20/api/v1/lab/status
```

## 2. Preparation
| Step | Description |
|------|------|
| 1 | Test image verification |
| 2 | Configuration backup |
| 3 | Log directory cleanup |

## 3. Initialization Command
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"mode": "training", "resetLogs": true}' \
'https://172.30.11.20/api/v1/lab/init'
```

## 4. Progress Tracking
- `watch -n2 "curl -ks https://172.30.11.20/api/v1/lab/progress"`
- `journalctl -u lab-reset -f`

## 5. Completion Verification
After initialization is complete, verify the following items:
1. Is a new session folder created in `/var/log/lab-reset`?
2. Is `systemctl status lab-core` in `active (running)` state?
3. Verify that the `phase` value in the REST response is `READY`.

## 6. Follow-up Tasks
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"command": "seed-data"}' \
'https://172.30.11.20/api/v1/lab/tasks'
```

## 7. Report Writing
- The lab technician records the results in the `docs/reports/box-init-template.md` file.
- If a problem occurs, attach the logs and contact `lab-support@example.com`.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**