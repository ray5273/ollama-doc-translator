# Translation Test: NVMe-oF Connection Practice
This document describes a simulated NVMe-oF connection scenario for verifying translation quality. The target is the `orion-target` initiator.

## 1. Environment Summary
| Category | Information |
|---|---|
| Target NQN | `nqn.2024-01.test.orion` |
| Management IP | `172.40.1.5` |
| Data Port | `192.168.90.10` |
| Protocol | TCP |

## 2. Pre-Check
1. Verify existing connections using the `nvme list-subsys` command.
2. Verify that the `/etc/nvme/hostnqn` file is up-to-date.
3. Verify that port 4420 is open in the firewall.

## 3. Connection Command
```bash
$ sudo nvme connect \
-t tcp \
-n nqn.2024-01.test.orion \
-a 192.168.90.10 \
-s 4420
```

## 4. Status Check
```bash
$ sudo nvme list
$ sudo nvme netapp ontapdevices -o json
```

## 5. Session Termination
```bash
$ sudo nvme disconnect -n nqn.2024-01.test.orion
```

## 6. Troubleshooting
- **Connection Failure**: Check the kernel logs using `dmesg | tail` and, if necessary, add the `-l 3600` option to the `sudo nvme connect` command to increase the timeout.
- **Performance Degradation**: Check the latency and error counters using the `sudo nvme smart-log /dev/nvme1n1` command.
- **Security Policy**: The target uses a self-signed certificate, so if TLS connection is required, the `--tls` flag and the certificate path must be specified.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**