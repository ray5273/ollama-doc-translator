# PBSSD Network Configuration (Before Box Initialization)
Network configuration can be set within PBSSD but this document guides you through configuring and managing PBSSD's network interface from an NVMe-oF initiator before initialization.

It is recommended to perform network configuration only in the phase before box initialization.

This document assumes the following goals and environments:
- **Goal:** Manually configure a static IP address on PBSSD's 100Gbps NVMe-oF interface via a 1Gbps management interface from the initiator
- **Environment:**
  - Firmware is properly installed on PBSSD, and the `orc_run` service is running
  - PBSSD has been assigned an IP address `10.1.3.8` via DHCP through a 1Gbps management interface and communicates stably with the initiator
  - PBSSD's 100Gbps NVMe-oF interface currently lacks an assigned IP address and requires manual configuration

> **Example Usage Note:**
> - Some commands may require `sudo` privileges depending on the environment.
> - REST API Requests
>   - Assuming the use of an admin account `admin:admin`.
>   - Assuming a self-signed certificate is used, commands are written with the `-k` option included for `curl`.

## Finding DHCP IP
Use the following command to check the IP address automatically assigned via DHCP:

The command execution result confirms that the IP address of the target PBSSD is `10.1.3.8`. _(Note: Hostname may vary depending on the device.)_

**1. mDNS Discovery**  
Using the command `avahi-browse -alr`, you can check the hostname, IP address, and service information broadcasted via mDNS (Multicast DNS) on the local network.
```bash
$ apt install avahi-utils
$ avahi-browse -alr
```
```bash
...
= ens17f0np0 IPv6 spdk0_10.1.3.8_1153    _nvme-disc._tcp    local
   hostname = [pbssd.local]
   address = [10.1.3.8]
   port = [1153]
   txt = ["nqn=nqn.2014-08.org.nvmexpress.discovery" "p=tcp"]
...
```

**2. IP ↔ MAC Mapping Verification**  
If there has been communication between the initiator and the device, you can verify the IP address ↔ MAC address mapping stored in the local ARP table using the `arp -a` command.
```bash
$ arp -a
```
```bash
... 
pbssd.local (10.1.3.8) at 7c:c2:55:9f:fd:d0 [ether] on enp9s0f0
...
```

## PBSSD Firmware Network Check
Assuming a scenario where a 100Gbps network interface does not have an assigned IP address, a REST API request is issued through a 1Gbps management port to verify the network settings of the target PBSSD device. The `portNum` value for the 100Gbps network interface is confirmed through the REST API response.

**1. Command**  
Invoke the `GET /settings/network` endpoint of the REST API to check network information.
```bash
$ curl -X GET \
-u '<USERNAME>:<PASSWORD>' \
-H 'Accept: application/json'\
'https://<IP_ADDRESS>/api/v1/settings/network'
```

**2. Command Usage Example**  
In the example below, `"portNum": 2` represents the port number where the 100Gbps network interface is located.
```bash
$ curl -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://10.1.3.8/api/v1/settings/network'
```
```bash
{
  "common": {
    "message": "API Server successfully get the network settings.",
    "relatedJobs": null
  },
  "networkPortSettings": [
    ...
    {
      "cidr": 64,
      "ip": "fe80::7ec2:54ef:ff43:ae80",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 2,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
    },
    ...
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "gateway": "10.1.5.22",
      "ip": "10.1.3.8",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 4,
      "displayName": "Intel Corporation I350 Gigabit Network Connection",
      "health": "UP",
    }
    ...
  ]
}
```

## Network Setting
Before performing Box Initialization, network settings are required. Refer to the `3. Command Usage Examples` section to manually configure a static IP address on a 100Gbps network interface.

**1. Command**  
To configure the network settings for the target PBSSD via REST API, call the `PUT /settings/network` endpoint of the REST API. When requesting network settings through the REST API and specifying the `type` field, the `pos-essential-ioworker` service on the target PBSSD automatically starts. In environments without a DHCP server or when a static IP address is permanently used by PBSSD, issue a `PUT /settings/network` request including the `networkPortSettings` object to explicitly configure IP address, DHCP settings, DNS, gateway, etc.
> This API can only be invoked with an account that has administrative privileges.
```bash
{
  "common": {
    "message": "API Server successfully get the network settings.",
    "relatedJobs": null
  },
  "networkPortSettings": [
    ...
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "gateway": "10.1.5.22",
      "ip": "10.1.3.8",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 4,
      "displayName": "Intel Corporation I350 Gigabit Network Connection",
      "health": "UP",
      "type": "tcp"
    },
    ...
    {
      "cidr": 64,
      "ip": "fe80::7ec2:54ef:ff43:ae80",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 2,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
      "type": "tcp"
    },
    ...
  ]
}
```
Below is a description of the fields in the request body:

| Field Name                  | Type              | Required | Description                                              |
|----------------------------|------------------|---------|--------------------------------------------------|
| `type`                      | `string`          | Required | Network transmission protocol (e.g., `TCP`, `RDMA`)             |
| `networkPortSettings`       | `array`           | Optional | List of network port settings                          |
| `isDhcpEnabled`             | `boolean`         | Required | Whether DHCP is enabled (`true`: automatic assignment, `false`: static IP) |
| `ip`                        | `string`          | Optional | Static IP address (e.g., `192.168.1.100`)                  |
| `cidr`                      | `int`             | Optional | Subnet mask length (e.g., `24`)                         |
| `gateway`                   | `string`          | Optional | Gateway address (e.g., `192.168.1.1`)                   |
| `dnsPrimaryAddress`         | `string`          | Optional | Primary DNS server (e.g., `8.8.8.8`)                       |
| `dnsSecondaryAddress`       | `string`          | Optional | Secondary DNS server (e.g., `8.8.4.4`)                       |
| `mtuBytes`                  | `int`             | Optional | MTU size (default `1500`)                              |
| `portNum`                   | `int`             | Required | Network port number (e.g., `1`, `2`)                     |


**2. Command Usage Example: Changing Network Protocol & Verifying Changes**  
This REST API request changes the network connected to target PBSSD (`10.1.3.8`) to `"type": "tcp"`.
```bash
$ curl -k -X PUT \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{ "type": "tcp"}' \
'https://10.1.3.8:443/api/v1/settings/network'
```
```bash
{"message":"API server successfully set the network settings","relatedJobs":null}
```
To verify the changes, retrieve network information.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://10.1.3.8/api/v1/settings/network'
```
```bash
{
  "common": {
    "message": "API Server successfully get the network settings.",
    "relatedJobs": null
  },
  "networkPortSettings": [
    ...
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "gateway": "10.1.5.22",
      "ip": "10.1.3.8",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 4,
      "displayName": "Intel Corporation I350 Gigabit Network Connection",
      "health": "UP",
      "type": "tcp"
    },
    ...
    {
      "cidr": 64,
      "ip": "fe80::7ec2:54ef:ff43:ae80",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 2,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
      "type": "tcp"
    },
    ...
  ]
}
```
**3. Command Usage Example: Changing Network Protocol & Configuring Single Port Settings & Verifying Changes**  
This REST API request changes the network on target PBSSD (`10.1.3.8`) to `"type": "tcp"` and modifies network settings for `"portNum": 2`. Refer to the commands below to configure the network settings for a 100Gbps network interface as intended in this document.
```bash
$ curl -k -X PUT \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{ "type": "tcp", "networkPortSettings": [{"isDhcpEnabled": false,"ip":"10.100.3.8", "cidr": 16, "gateway": "10.1.5.22", "dnsPrimaryAddress": "10.1.1.13", "dnsSecondaryAddress": "12.26.3.228", "mtuBytes": 9000, "portNum": 2}]}' \
'https://10.1.3.8:443/api/v1/settings/network'
```

```
Change Result Please confirm. For Network Information Checking.
```
Check the change results by querying network information.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json'
'https://10.1.3.8/api/v1/settings/network'
```
```bash
{
  "common": {
    "message": "API Server successfully retrieved the network settings.",
    "relatedJobs": null
  },
  "networkPortSettings": [
    ...
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "gateway": "10.1.5.22",
      "ip": "10.1.3.8",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 4,
      "displayName": "Intel Corporation I350 Gigabit Network Connection",
      "health": "UP",
      "type": "tcp"
    },
    ...
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "ip": "10.100.3.8",
      "isDhcpEnabled": false,
      "mtuBytes": 9000,
      "portNum": 2,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
      "type": "tcp"
    },
    ...
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "ip": "10.100.3.9",
      "isDhcpEnabled": false,
      "mtuBytes": 9000,
      "portNum": 3,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
      "type": "tcp"
    },
    ...
  ]
}
```
**Example Usage: Changing Network Protocol and Updating Multiple Port Settings (ports: 2, 3) & Verification**  
The following example demonstrates a REST API request to modify network settings on the target PBSSD (`10.1.3.8`) to `"type": "tcp"` and simultaneously update network information for multiple ports (`"portNum": 2` and `3`).
```bash
$ curl -k -X PUT \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{ "type": "tcp", "networkPortSettings": [{"isDhcpEnabled": false,"ip":"10.100.3.8", "cidr": 16, "gateway": "10.1.5.22", "dnsPrimaryAddress": "10.1.1.13", "dnsSecondaryAddress": "12.26.3.228", "mtuBytes": 9000, "portNum": 2},{"isDhcpEnabled": false,"ip":"10.100.3.9", "cidr": 16, "gateway": "10.1.5.22", "dnsPrimaryAddress": "10.1.1.13", "dnsSecondaryAddress": "12.26.3.228", "mtuBytes": 9000, "portNum": 3}]}'\
'https://10.1.3.8:443/api/v1/settings/network'
```
```bash
{"message":"API server successfully set the network settings","relatedJobs":null}
```
Check the change results by querying network information.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json'
'https://10.1.3.8/api/v1/settings/network'
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**