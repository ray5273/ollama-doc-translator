# Translation Test: Virtual Box Initialization Procedure
This document describes a fictional box initialization scenario created by the QA team for checking translation quality.

## 1. Initial Inspection
- Lab Equipment Name: `orion-mini`
- Management IP: `172.30.11.20`
- Status Query Command:
```bash
$ curl -k https://172.30.11.20/api/v1/lab/status
```

## 2. Preparation Steps
| Step | Description |
|------|-------------|
| 1    | Verify Test Image |
| 2    | Backup Configuration |
| 3    | Clean Log Directory |

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
After initialization, verify the following items:
1. Is a new session folder created inside `/var/log/lab-reset`?
2. Is `systemctl status lab-core` in `active (running)` state?
3. Confirm that the `phase` value in the REST response is `READY`.

## 6. Post-Initialization Tasks
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"command": "seed-data"}' \
'https://172.30.11.20/api/v1/lab/tasks'
```

## 7. Report Writing
- The practitioner records the results in the `docs/reports/box-init-template.md` file.
- If issues arise, attach logs to an email to `lab-support@example.com` for inquiry.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**