# Translation Test: NVMe-oF Connection Practice
This document is a simulated NVMe-oF connection scenario designed to validate translation quality. The target is the `orion-target` initiator.

## 1. Environment Summary
| Category | Information |
|----------|-------------|
| Target NQN | `nqn.2024-01.test.orion` |
| Management IP | `172.40.1.5` |
| Data Port | `192.168.90.10` |
| Protocol | TCP |

## 2. Pre-Check
1. Check existing connections with the `nvme list-subsys` command.
2. Verify that the `/etc/nvme/hostnqn` file is up-to-date.
3. Check if firewall allows port 4420.

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

## 5. Session Disconnect
```bash
$ sudo nvme disconnect -n nqn.2024-01.test.orion
```

## 6. Troubleshooting
- **Connection Failure**: Check kernel logs with `dmesg | tail`, and if necessary, add the `-l 3600` option to the `sudo nvme connect` command to increase timeout.
- **Performance Degradation**: Use the `sudo nvme smart-log /dev/nvme1n1` command to check latency and error counters.
- **Security Policies**: The test target uses a self-signed certificate, so specify the `--tls` flag and certificate path if TLS connection is required.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**