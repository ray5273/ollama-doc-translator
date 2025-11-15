# Translation Test: NVMe-oF Connection Practice
This document is a hypothetical NVMe-oF connection scenario constructed for verifying translation quality. The target practice device is the `orion-target` initiator.

## 1. Environment Summary
| Category | Information |
|----------|-------------|
| Target NQN | `nqn.2024-01.test.orion` |
| Management IP | `172.40.1.5` |
| Data Port | `192.168.90.10` |
| Protocol | TCP |

## 2. Pre-Check
1. Verify existing connections using the `nvme list-subsys` command.
2. Ensure the `/etc/nvme/hostnqn` file is up-to-date.
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

## 5. Session Disconnection
```bash
$ sudo nvme disconnect -n nqn.2024-01.test.orion
```

## 6. Troubleshooting
- **Connection Failure**: Check kernel logs with `dmesg | tail`, and if necessary, add the `-l 3600` option to the `sudo nvme connect` command to extend the timeout.
- **Performance Degradation**: Use `sudo nvme smart-log /dev/nvme1n1` to check latency and error counters.
- **Security Policy**: Since the test target uses a self-signed certificate, specify the `--tls` flag along with the certificate path if TLS connection is required.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**