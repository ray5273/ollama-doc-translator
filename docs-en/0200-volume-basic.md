# Translation Test: Data Volume Practice Scenario Guide
This document is a hypothetical data volume management guide created for verifying translation accuracy. Do not apply it to actual infrastructure.

This document covers the following items:
1. [Virtual Volume Store](#virtual-volume-store)
2. [Sandbox Volume](#sandbox-volume)
3. [NVMe-oF Exposure](#nvme-of-exposure)

## Virtual Volume Store
Training `LVS` can be configured on practice SSDs or existing LVol volumes. The following example uses the `atlas9472n1` device.

### 1. Creation
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{
  "alias": "atlas9472n1",
  "lvs_name": "training_store",
  "cluster_sz": 1048576,
  "clear_method": "none"
}' \
'https://<IP_ADDRESS>/api/v1/training/lvstore'
```

| Field         | Description           |
|---------------|-----------------------|
| `alias`       | Base Device Name      |
| `lvs_name`    | Name of the LVS to be Created |
| `cluster_sz`  | Cluster Size          |
| `clear_method`| Method of Space Initialization |

### 2. Query
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
'https://<IP_ADDRESS>/api/v1/training/lvstore'
```

### 3. Deletion
```bash
$ curl -k -X DELETE \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store"}' \
'https://<IP_ADDRESS>/api/v1/training/lvstore'
```

## Sandbox Volume
### 1. Creation
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{
  "alias": "training_store",
  "lvol_name": "demo_lvol",
  "size_in_mib": 51200,
  "thin_provision": true
}' \
'https://<IP_ADDRESS>/api/v1/training/lvol'
```

### 2. Query
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
'https://<IP_ADDRESS>/api/v1/training/lvol'
```

### 3. Deletion
```bash
$ curl -k -X DELETE \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol'
```

## NVMe-oF Exposure
### 1. Attach Request
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
```

### 2. Status Check
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
```

### 3. Detachment
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol", "action": "detach"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
```

## Reference Table
| Item           | Value                  |
|----------------|------------------------|
| Training Account | `trainee`             |
| API Endpoint    | `https://<IP_ADDRESS>/api/v1/training/*` |
| Default Context Length | 32 MiB |

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**