# PBSSD Box Initialization Guide
Box Initialization is the process of setting up NVMe-oF (NVMe over Fabrics) target PBSSD. While initialization can occur internally within PBSSD, this document guides the procedure for initializing PBSSD through an NVMe-oF initiator.

This document assumes the following goals and environment:
- Goal: Initialize Box in `volume`, `nvmeof`, `tcp` modes via REST API for PBSSD
- Environment:
  - PBSSD firmware installation, execution (orc_run), and network configuration are completed.
  - PBSSD has been assigned the IP address `10.1.3.8`.

> **Example Usage Note:**
> - REST API Request
>   - It is assumed that the administrator account uses `admin:admin`.
>   - Assuming a self-signed certificate is used, the `curl` command includes the `-k` option as written.

## PBSSD Status Check Before Box Initialization
A status response for each command has been prepared prior to box initialization.

**1. PBSSD Status Check via REST API**  
Invoke the `GET /firmware/status` endpoint of the REST API to verify the integrated firmware status and module-specific statuses and versions of PBSSD. `pos-essential-orchestrator` requires box initialization, while `pos-essential-ioworker` is in a `Not Running` state due to incomplete initialization.

```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://10.1.3.8/api/v1/firmware/status'
```

```bash
{
  "FirmwareServices": [
    {
      "name": "Total",
      "status": "Failed"
    },
    {
      "name": "pos-essential-orchestrator",
      "status": "Need Initialize",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-ioworker0",
      "status": "Not Running"
    },
    {
      "name": "pos-essential-ssd-anomaly-detector",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-management-ui",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-opentelemetry-collector (Third Party)",
      "status": "Running",
      "version": "0.77.0 (2.6.0)"
    },
    {
      "name": "pos-essential-node-exporter (Third Party)",
      "status": "Running",
      "version": "2.6.0 (v1.6.0)"
    },
    {
      "name": "pos-essential-prometheus (Third Party)",
      "status": "Running",
      "version": "2.6.0 (v2.47.0)"
    },
    {
      "name": "pos-essential-ipmi-exporter (Third Party)",
      "status": "Running",
      "version": "1.6.1"
    }
  ],
  "common": {
    "message": "Firmware status retrieved successfully",
    "relatedJobs": null
  }
}
```

**2. Network Configuration Verification**  
Invoke the `GET /settings/network` endpoint of the REST API to verify the PBSSD network settings.

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
  ]
}
```

## PBSSD Box Initialization
Initiate PBSSD box initialization by calling the `POST /settings/init` endpoint of the REST API.
> This API can only be invoked by accounts with administrative privileges.
```bash
$ curl -k -X POST \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "backing":"volume",
  "protocol":"nvmeof",
  "transport":"tcp"
}' \
'https://10.1.3.8/api/v1/settings/init'
```
```bash
{"message":"PBSSD initialized successfully","relatedJobs":null}
```

## PBSSD Status Check After Box Initialization
After successfully completing box initialization, responses for each command have been documented.

**1. PBSSD Status Check via REST API**  
Invoke the `GET /firmware/status` endpoint of the REST API to verify the integrated firmware status, module-specific statuses, and versions of PBSSD. If box initialization was successful, `pos-essential-orchestrator` and `pos-essential-ioworker` should be in `Running` state, with `Total` status indicating `OK`.

```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://10.1.3.8/api/v1/firmware/status'
```

```bash
{
  "FirmwareServices": [
    {
      "name": "Total",
      "status": "OK"
    },
    {
      "name": "pos-essential-orchestrator",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-ioworker0",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-ssd-anomaly-detector",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-management-ui",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-opentelemetry-collector (Third Party)",
      "status": "Running",
      "version": "0.77.0 (2.6.0)"
    },
    {
      "name": "pos-essential-node-exporter (Third Party)",
      "status": "Running",
      "version": "2.6.0 (v1.6.0)"
    },
    {
      "name": "pos-essential-prometheus (Third Party)",
      "status": "Running",
      "version": "2.6.0 (v2.47.0)"
    },
    {
      "name": "pos-essential-ipmi-exporter (Third Party)",
      "status": "Running",
      "version": "1.6.1"
    }
  ],
  "common": {
    "message": "Firmware status retrieved successfully",
    "relatedJobs": null
  }
}
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**