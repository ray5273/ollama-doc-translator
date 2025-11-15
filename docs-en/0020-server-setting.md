# Translation Test: Experimental Network Configuration Guide
This document explains the process of configuring network interfaces for virtual equipment `Nebula Node` used in a lab environment. Do not apply this to actual hardware.

### Assumed Environment
- **Objective**: Assign a static IP to a high-speed data port via a management interface on an educational control node.
- **Environment**:
  - The `nebula-orchestrator` service is running, and the management interface is accessible at `172.20.0.8` address.
  - The data port does not have an IP address yet and requires manual configuration for RDMA testing.

> **Lab Note**
> - Adjust commands requiring `sudo` privileges according to your environment.
> - Always use the `-k` flag for REST calls assuming a self-signed certificate.

## 1. Finding DHCP Address
### 1.1 mDNS Discovery
```bash
$ avahi-browse -alr | grep nebula
```

### 1.2 ARP Table Check
```bash
$ arp -a | grep nebula
```

## 2. Checking Current Network Status
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

## 3. Applying Network Configuration
### 3.1 Request Body Structure
| Field Name | Type | Description |
|------------|------|-------------|
| `type`     | `string` | Protocol used (`tcp`, `rdma`) |
| `networkPortSettings` | `array` | List of configurations per port |
| `portNum`  | `int`   | Target port number |
| `ip`       | `string` | IP address to configure |
| `cidr`     | `int`   | Subnet |
| `gateway`  | `string` | Gateway |

### 3.2 Command Example
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

## 4. Verification of Results
1. Requery using `curl -k -X GET ...` to confirm if the IP has been applied to `portNum` 3.
2. Test gateway reachability with `ping 192.168.40.1 -c 2`.
3. Record fabric latency using `rdma-statistic collect`.

## 5. Troubleshooting Scenarios
- **Response Delay**: If REST calls delay for more than 5 seconds, check the `journalctl -u nebula-orchestrator` logs.
- **MTU Mismatch**: Given that the experimental network requires `mtuBytes 9000`, add this field to the PUT request if necessary.
- **Incorrect Authentication Information**: If a `401` response occurs, retry with a newly issued lab account credentials.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**