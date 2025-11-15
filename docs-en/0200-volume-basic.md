# Volume and Volume Store: Basic Operations
This document explains basic REST API functionalities related to volumes and provides usage examples for each API.

This document covers the following topics:
1. [Logical Volume Store](#logical-volume-store)  
   1.1. Creation  
   1.2. Retrieval  
   1.3. Deletion
2. [Logical Volume](#logical-volume)  
   2.1. Creation  
   2.2. Retrieval  
   2.3. Deletion
3. [Exposing Logical Volume via NVMe-oF](#expose-logical-volume-to-external-hosts-via-nvme-of)  

This document assumes the following goals and environments:
- **Goal**: Manage volumes of PBSSD through REST APIs.
- **Environment**:
  - PBSSD is running normally with box initialization completed and `Total` status set to `OK`.
  - PBSSD has been assigned the IP address `10.1.3.8`.
  - The device information referenced in examples is as follows:
    ```bash
      {
        "devices": [
          {
            "address": "0000:25:00.0",
            "bdevName": "nvme9472n1",
            "capabilities": [],
            "firmware": {
              "name": "OPRATB57"
            },
            "modelNumber": "SAMSUNG MZWMO30THCLF-01AW7",
            "numa": -1,
            "serialNumber": "S871NG0Y200019",
            "size": 30720827326464,
            "slotId": 9472,
            "status": 1
          },
          ...
        ],
        "message": "Devices retrieved successfully",
        "relatedJobs": null
      }
      ```
> **Example usage reference:**
> - REST API Request
>   - Administrator Through the account `admin:admin` Using it Assume.
>   - self-signed Certificate Using it Assume, `curl` According to instructions `-k` Options Including command It was written..

## Logical Volume Store
LVS(Logical Volume Store) Physical NVMe Device Or LVol Above Hierarchy Composed, The user According to need Following Size and performance Other Volume Dynamically Creation·Delete Water so that it may be possible Supporting Abstraction It is a hierarchy..

**Creation**   
REST API's `POST /volumes/lvstore` endpoints Call upon LVS I create.
>  API Manager Authority Exists By account only To call Water It exists..
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "<BDEV_OR_LVOL_NAME>",
  "lvs_name": "<LVS_NAME>",
  "cluster_sz": <CLUSTER_SIZE>,
  "clear_method": "<CLEAR_METHOD>",
  "num_md_pages_per_cluster_ratio": "<PAGE_PER_CLUSTER>"
}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvstore'
```

Below is Request The main text In the field The Republic of Korea This is an explanation..
| Field Name                                | Type               | Essential Whether |                                   |
|--------------------------------------|------------------|---------|-----------------------------------|
| `alias`                              | `string`         | Essential     | LVS Create Location (ex. bdev Or LVol) |
| `lvs_name`                           | `string`         | Essential     | Create LVS Name                      |
| `cluster_sz`                         | `uint32`         | Selection     | Cluster Size                         |
| `clear_method`                       | `string`         | Selection     | LVS Creation Before Storage Space Initialization Method        |
| `num_md_pages_per_cluster_ratio`     | `uint32`         | Selection     | Per cluster Metadata Page Ratio          |

**2. Inquiry**  
REST API's `GET /volumes/lvstore` Endpoints Call upon LVS I am checking it..
```bash
curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Accept: application/json' \
'https://<IP_ADDRESS>/api/v1/volumes/lvstore'
```

Below is Query parameters to The Republic of Korea This is an explanation..
| Field Name                                   | Type               | Essential Whether |             |
|-----------------------------------------|------------------|---------|-------------|
| `lvs_name`                              | `string`         | Selection     | LVStore Name |

**Deletion**  
REST API's `DELETE /volumes/lvstore` Endpoints Call upon LVS Delete it..
```bash
curl -k -X DELETE \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "<LVS_NAME>",
  "uuid": "<UUID>"
}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvstore'
```

Below is Request The main text In the field The Republic of Korea This is an explanation..
| Field Name          | Type              | Essential Whether |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Essential     | Delete LVS Path |
| `uuid`        | `string`         | Selection     | uuid         |


**Examples of Command Usage**  
`bdevName` `nvme9472n1`인 On the device LVS Create For safety Below command I use it..
```bash
$ curl -k -X POST \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-d '{"alias": "nvme9472n1", "lvs_name": "lvs9472_1st"}' \
'https://10.1.3.8/api/v1/volumes/lvstore'
```
```bash
{"data":"559723cc-d39f-4adf-a402-c37b0f7a3691","message":"Successfully created lvstore"}
```

Created LVS Search For safety Below command I use it..
```bash
curl -k -X GET \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
'https://10.1.3.8/api/v1/volumes/lvstore'
```
```bash
{
  "data": [
    {
      "block_size": 512,
      "cluster_size": 4194304,
      "free_clusters": 7317262,
      "name": "lvs9472_1st",
      "total_data_clusters": 7317262,
      "uuid": "559723cc-d39f-4adf-a402-c37b0f7a3691"
    },
    ...
  ],
  "message": "Successfully retrieved lvstore list"
}
```

LVS names `lvs9472_1st` delete the LVS using the following commands:

```bash
curl -k -X DELETE \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{"alias": "lvs9472_1st"}' \
'https://10.1.3.8/api/v1/volumes/lvstore'
```

```bash
{"data":true,"message":"Successfully deleted lvstore"}
```

## Logical Volume
LVol (Logical Volume) is a virtual disk partition that abstracts physical storage devices for easier use.

**1. Creation**  
Create LVol by calling the `POST /volumes/lvol` endpoint of the REST API.
> This API can only be invoked with an account that has administrative privileges.
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "<BASE_LVS_NAME>",
  "lvol_name": "<LVOL_NAME>",
  "size_in_mib": <SIZE>,
  "thin_provision": <IS_THIN_PROVISION>,
  "uuid": "<UUID>"
}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol'
```

Here is a description of the fields in the request body:
| Field Name               | Type        | Required |                          |
|--------------------|------------|---------|--------------------------|
| `alias`            | `string`   | Yes     | LVS name where LVol will be created |
| `lvol_name`        | `string`   | Yes     | Name of the LVol to be created |
| `size_in_mib`      | `uint64`   | Yes     | Size                      |
| `thin_provision`   | `boolean`  | No      | Thin provision availability |
| `uuid`             | `string`   | No      | UUID                      |

**2. Retrieval**  
Retrieve the created LVol (Logical Volume) by calling the `GET /volumes/lvol` endpoint of the REST API.
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
https://<IP_ADDRESS>/api/v1/volumes/lvol
```

Here is a description of the query parameters:
| Field Name                                 | Type              | Required |             |
|--------------------------------------|------------------|---------|-------------|
| `alias`                              | `string`         | No      | LVol path   |

**3. Deletion**  
Delete the LVS by calling the `DELETE /volumes/lvol` endpoint of the REST API.
```bash
curl -k -X DELETE \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "<LVOL_NAME>",
}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol'
```

Here is a description of the fields in the request body:
| Field Name          | Type              | Required |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Yes     | Path of LVol to delete |

**4. Command Examples**  
Use the following command to create an LVol named `lvol9472_1st` under an LVS named `lvs9472_1st`:
```bash
$ curl -k -X POST \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "lvs9472_1st",
  "lvol_name": "lvol9472_1st",
  "size_in_mib": 28500000
}' \
'https://10.1.3.8/api/v1/volumes/lvol'
```
```bash
{"data":"bcf5b9ad-7697-4615-b093-7b675f2e9c0f","message":"Successfully created lvol"}
```

To retrieve the created LVol, use the following command:
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
'https://10.1.3.8/api/v1/volumes/lvol'
```
```bash
{
  "data": [
    {
      "alias": "lvs9472_1st/lvol9472_1st",
      "block_size": 512,
      "is_clone": false,
      "is_degraded": false,
      "is_esnap_clone": false,
      "is_snapshot": false,
      "is_thin_provisioned": false,
      "lvs": {
        "name": "lvs9472_1st",
        "uuid": "559723cc-d39f-4adf-a402-c37b0f7a3691"
      },
      "name": "lvol9472_1st",
      "num_blocks": 58368000000,
      "uuid": "bcf5b9ad-7697-4615-b093-7b675f2e9c0f"
    },
    ...
  ],
  "message": "Successfully retrieved lvol list"
}
```

To delete the LVol at the path `lvs9472_1st/lvol9472_1st`, use the following command:
```bash
curl -k -X DELETE \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{"alias": "lvs9472_1st/lvol9472_1st"}' \
'https://10.1.3.8/api/v1/volumes/lvol'
```
```bash
{"data":true,"message":"Successfully deleted lvol"}
```

## Expose Logical Volume to External Hosts via NVMe-oF
To access the volume of PBSSD through an initiator using NVMe-oF (NVMe over Fabrics), you must first `attach` the volume.
Once `attached`, the volume is recognized as a block device by the initiator through a normal NVMe-oF connection, enabling file I/O operations. [The process of connecting the initiator to PBSSD via NVMe-oF is covered in the NVMe-oF page](0300-nvmeof-connection.md).

**1. Command**  
Call the `POST /volumes/lvol/attach` endpoint of the REST API to `attach` the LVol.
> This API can only be invoked by an account with administrative privileges.
```bash
curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "<LVOL_PATH>"}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol/attach'
```

**2. Command Example Usage**  
Use the following command to `attach` the `lvol9472_1st` named LVol within the `lvs9472_1st` LVS.
```bash
curl -k -X POST \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-d '{"alias": "lvs9472_1st/lvol9472_1st"}' \
'https://10.1.3.8/api/v1/volumes/lvol/attach'
```
```bash
{"data":"lvs9472_1st/lvol9472_1st","message":"Successfully attached lvol"}
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**