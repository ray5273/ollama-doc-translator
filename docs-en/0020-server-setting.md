# Translation Test: Experimental Network Configuration Guide
This document describes the process of configuring the network interface of the virtual device `Nebula Node` used in the lab. Do not apply this to actual devices.

The environment assumed in this scenario is as follows:
- Goal: Assign a static IP address to a training node via the management interface.
- Environment:
  - The `nebula-orchestrator` service is running, and the management interface is accessible at the address `172.20.0.8`
  - The data port is currently without an IP address, and manual configuration is required for RDMA testing.

> **Lab Notes**
> - Adjust the commands requiring `sudo` permissions to match the environment.
> - REST calls assume self-signed certificates, so always use the `-k` flag.

## 1. Find DHCP Address
### 1.1 mDNS Browse
```bash
$ avahi-browse -alr | grep nebula
```

### 1.2 Check ARP Table
```bash
$ arp -a | grep nebula
```

## 2. Check Current Network Status
### 2.1 REST Request Example
```bash
$ curl -k -X GET \
-u 'trainer:trainer' \
-H 'Accept: application/json' \
'https://172.20.0.8/api/v1/training/network'
```

### 2.2 Expected Response
```bash
{
  "ports": [
    {"portNum": 1, "displayName": "Intel X710", "ip": "172.20.0.8"},
    {"portNum": 3, "displayName": "Mellanox CX6", "ip": null}
  ],
  "message": "training snapshot"
}
```

## 3. Apply Network Settings
### 3.1 Request Body Structure
| Field Name | Type | Description |
|---|---|---|
| `type` | `string` | Protocol to use (`tcp`, `rdma`) |
| `networkPortSettings` | `array` | List of configurations for each port |
| `portNum` | `int` | Target port number |
| `ip` | `string` | IP to set |
| `cidr` | `int` | Subnet |
| `gateway` | `string` | Gateway |

### 3.2 Example Command
```bash
$ curl -k -X PUT \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{
  "type": "rdma",
  "networkPortSettings": [
    {
      "portNum": 3,
      "ip": "192.168.40.10",
      "cidr": 24,
      "gateway": "192.168.40.1",
      "dnsPrimaryAddress": "1.1.1.1",
      "dnsSecondaryAddress": "8.8.8.8",
      "isDhcpEnabled": false
    }
  ]
}' \
'https://172.20.0.8/api/v1/training/network'
```

## 4. Verify Results
1. Use `curl -k -X GET ...` again to verify that `portNum` 3 has been assigned an IP address.
2. Use the command `ping 192.168.40.1 -c 2` to test reachability to the gateway.
3. Use the command `rdma-statistic collect` to record fabric latency.

## 5. Troubleshooting Scenarios
- **Delayed Response**: If REST calls are delayed for more than 5 seconds, check the `journalctl -u nebula-orchestrator` logs.
- **MTU Mismatch**: The experimental network requires an `mtuBytes 9000`, so if necessary, add this field to the PUT request.
- **Incorrect Authentication Information**: If a `401` response occurs, retry with the newly issued training account.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**