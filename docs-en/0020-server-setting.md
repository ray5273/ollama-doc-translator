# Translation Test: Experimental Network Configuration Guide
This document describes the process of configuring the network interface of a virtual device `Nebula Node` used in a lab environment. Do not apply this to actual hardware.

### Assumptions for the Environment
- **Objective**: Assign a static IP through the management interface of the training control node to a high-speed data port.
- **Environment**:
  - `nebula-orchestrator` service is running, and the management interface is accessible at `172.20.0.8`.
  - The data port does not have an IP yet and requires manual configuration for RDMA testing.

> **Lab Note**
> - Adjust commands requiring `sudo` according to your environment.
> - Always use the `-k` flag for REST calls assuming a self-signed certificate.

## 1. Finding DHCP Addresses
### 1.1 mDNS Discovery
```bash
$ avahi-browse -alr | grep nebula
```

### 1.2 Check ARP Table
```bash
$ arp -a | grep nebula
```

## 2. Checking Current Network Status
### 2.1 Example REST Request
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
| `networkPortSettings` | `array` | List of port configurations |
| `portNum` | `int` | Target port number |
| `ip`      | `string` | IP to be assigned |
| `cidr`    | `int` | Subnet |
| `gateway` | `string` | Gateway |

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

## 4. Verification
1. Use `curl -k -X GET ...` to check if the IP has been applied to `portNum` 3.
2. Test gateway reachability with the command `ping 192.168.40.1 -c 2`.
3. Record fabric wait times with the command `rdma-statistic collect`.

## 5. Troubleshooting Scenarios
- **Response Delay**: If the REST call is delayed by more than 5 seconds, check the `journalctl -u nebula-orchestrator` logs.
- **MTU Mismatch**: The experimental network requires `mtuBytes 9000`, so add this field to the PUT request if necessary.
- **Incorrect Credentials**: If a `401` response occurs, retry with a newly issued lab account.

[TRANSLATION_END]

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**