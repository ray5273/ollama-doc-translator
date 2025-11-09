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
- **Goal:** Manage volumes of PBSSD through REST APIs
- **Environment:**
  - PBSSD is running normally with box initialization completed, with `Total` status set to `OK`.
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
>   - Manager Account `admin:admin`It seems like the provided text "을" is incomplete or lacks context for a meaningful translation. Could you please provide more text for translation? Used it Assume.
>   - self-signed Certificate Used it Assuming, `curl` According to instructions `-k` Options Including command I have written it..

## Logical Volume Store
LVS(Logical Volume Store)That Physical NVMe Device Or LVol Above Hierarchy Composed, The user According to need Following Size and performance Other Volume Dynamically Creation·Delete Water so that Supporting Abstraction It is a hierarchy..

**1. Creation**   
REST APIThe provided Korean text "의" translates to "of" or "for" in English, depending on the context. Without additional context, a direct translation cannot specify which usage is intended. Could you please provide more context or text for a precise translation? `POST /volumes/lvstore` Endpoint Call them LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? I create..
> This APIThat Manager Authority Exists By account only to call Water It exists..
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

Below is Request The text provided seems incomplete as "본문의" translates to "of the main text" or "of the passage," but lacks context for a full translation. Assuming you intended to provide more text for translation, please offer the complete Korean text for an accurate translation. Based solely on the given word:

"Of the main text" or "Of the passage Field Regarding This is an explanation..
| Field Name                                | Type               | Essential Whether |                                   |
|--------------------------------------|------------------|---------|-----------------------------------|
| `alias`                              | `string`         | Essential     | LVSIt seems there might be a typo or missing text in your request. Could you please provide the Korean text you would like translated to English? To create Location (ex. bdev Or LVol) |
| `lvs_name`                           | `string`         | Essential     | To create LVS Name                      |
| `cluster_sz`                         | `uint32`         | Choice     | Cluster Size                         |
| `clear_method`                       | `string`         | Choice     | LVS Creation The provided Korean text "전" translates to "before" in English. However, please note that context is crucial for accurate translation, and "전" can have different meanings depending on its usage in a sentence. Without additional context, this is the most straightforward translation. Storage Space Initialization Method        |
| `num_md_pages_per_cluster_ratio`     | `uint32`         | Choice     | Per cluster Metadata Page Ratio          |

**2. Inquiry**  
REST APIOf `GET /volumes/lvstore` Endpoint Call them LVSIt seems like your text might be incomplete. Could you please provide the full Korean text you would like translated? Checking.
```bash
curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Accept: application/json' \
'https://<IP_ADDRESS>/api/v1/volumes/lvstore'
```

Below is Query Parameters Regarding This is an explanation..
| Field name                                   | Type               | Essential Whether |             |
|-----------------------------------------|------------------|---------|-------------|
| `lvs_name`                              | `string`         | Choice     | LVStore Name |

**3. Delete**  
REST APIIt seems there might be a typo or incomplete text provided ("의" alone doesn't form a complete phrase or sentence in Korean). Could you please provide the full text you would like translated? `DELETE /volumes/lvstore` Endpoint Call them LVSIt seems there might be a typo or missing text in your request. Could you please provide the Korean text you would like translated to English? Deletes it.
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

Below is Request The main text In the field Regarding This is an explanation..
| Field Name          | Type              | Essential Whether |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Essential     | Delete LVS Path |
| `uuid`        | `string`         | Choice     | uuid         |


**4. Example Usage of Commands**  
`bdevName`This `nvme9472n1`In English, "인" by itself doesn't provide enough context for a meaningful translation as it can function as various parts of speech depending on context (e.g., a suffix, part of a name, etc.). Could you please provide more context or the full text? On the device LVSIt seems there might be a typo or missing text in your request. Could you please provide the Korean text you would like translated to English? Create For Below command I use it..
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

Created LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Search For Below command I use it..
```bash
curl -k -X GET \
...

```

`lvs9472_1st/lvol9472_1st` Pathway LVolIt seems there might be a typo or missing text in your request. Could you please provide the Korean text you would like translated to English? Delete For Below command I use it..
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

**Delete the LVS named `lvs9472_1st` using the following command:**
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
**Logical Volume (LVol)** is a virtual disk partition that abstracts physical storage devices for use.

**1. Creation**  
Call the `POST /volumes/lvol` endpoint of the REST API to create an LVol.
> This API can only be invoked by accounts with administrative privileges.
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

**Fields Description:**
| Field Name               | Type        | Required |                          |
|--------------------|------------|---------|--------------------------|
| `alias`            | `string`   | Yes     | LVol location alias      |
| `lvol_name`        | `string`   | Yes     | LVol name                |
| `size_in_mib`      | `uint64`   | Yes     | Size                      |
| `thin_provision`   | `boolean`  | Optional| Thin provisioning flag    |
| `uuid`             | `string`   | Optional| UUID                      |

**2. Retrieval**  
Call the `GET /volumes/lvol` endpoint of the REST API to retrieve the created LVol(Logical Volume).
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
https://<IP_ADDRESS>/api/v1/volumes/lvol
```

**Query Parameters Description:**
| Field Name                                 | Type              | Required |             |
|--------------------------------------|------------------|---------|-------------|
| `alias`                              | `string`         | Optional| LVol path   |

**3. Deletion**  
Call the `DELETE /volumes/lvol` endpoint of the REST API to delete the LVS.
```bash
curl -k -X DELETE \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "<LVOL_NAME>",
}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol'
```

**Request Body Fields Description:**
| Field Name          | Type              | Required |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Yes     | LVol path to delete |

**4. Command Example Usage**  
To create an LVol named `lvol9472_1st` under the LVS named `lvs9472_1st`, use the following command:
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
To access volumes on PBSSD via NVMe-oF from an initiator, first attach the relevant volume using NVMe-oF.
`Attached` volumes are recognized by the initiator through NVMe-oF connections as block devices, enabling file I/O operations. [Refer to the NVMe-oF connection process from the initiator to PBSSD in the NVMe-oF section](0300-nvmeof-connection.md).

**1. Command**  
Call the `POST /volumes/lvol/attach` endpoint of the REST API to attach an LVol.
> This API can only be invoked by accounts with administrative privileges.
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol/attach'
```

```bash
curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "<LVOL_PATH>"}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol/attach'
```

**2. Command Usage Example**  
To attach an `lvol` named `lvol9472_1st` within `LVS` named `lvs9472_1st`, use the following command:
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