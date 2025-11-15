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
- **Goal:** Manage volumes of PBSSD through REST APIs.
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
>   - Manager Account `admin:admin`The provided text "을" translates to "as" or depends on context, often functioning as a particle indicating the object of a verb in Korean sentences. Without additional context, a direct translation isn't fully illustrative, but generally:

"as" (in certain contexts) Used it Assume.
>   - self-signed Certificate Used it Assuming, `curl` According to instructions `-k` Options Including command I have written it..

## Logical Volume Store
LVS(Logical Volume Store)This Korean text "는" translates to "is" or "are" in English, depending on the context in which it is used. Without additional context, a direct translation cannot specify which form is most appropriate. Generally, it serves as a subject marker or verb ending in sentences. Physical NVMe Device Or LVol Above Hierarchy Composed, The user According to need Following Size and performance Other Volume Dynamically Creation·Delete Water To enable/make possible Supporting Abstraction It is a hierarchy..

**1. Creation**   
REST APIThe provided Korean text "의" translates to "of" or "a" in English, depending on the context. Without additional context, a direct translation cannot specify which usage is intended. Could you please provide more context or text for a precise translation? `POST /volumes/lvstore` Endpoint Call them LVSIt seems like your text might be incomplete. Could you please provide the full Korean text you would like translated? I create..
> This APIIs Manager Authority Exists By account only to call Water It exists..
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

Below is Request The main text Field Regarding This is an explanation..
| Field name                                | Type               | Essential Whether |                                   |
|--------------------------------------|------------------|---------|-----------------------------------|
| `alias`                              | `string`         | Essential     | LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? To create Location (ex. bdev Or LVol) |
| `lvs_name`                           | `string`         | Essential     | Creating LVS Name                      |
| `cluster_sz`                         | `uint32`         | Selection     | Cluster Size                         |
| `clear_method`                       | `string`         | Choice     | LVS Creation The provided Korean text "전" translates to "before" in English. However, please note that context is crucial for accurate translation, and "전" can have different meanings depending on its usage in a sentence. Without additional context, this is the most straightforward translation. Storage Space Initialization Method        |
| `num_md_pages_per_cluster_ratio`     | `uint32`         | Choice     | Per cluster Metadata Page Ratio          |

**2. Inquiry**  
REST APIThe provided Korean text "의" translates to "of" or "for" in English, depending on the context. Without additional context, a direct translation cannot specify which usage is intended. Please provide more context if a precise translation is needed. `GET /volumes/lvstore` Endpoint Call to LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Checking.
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
REST APIOf `DELETE /volumes/lvstore` Endpoint Call them LVSIt seems there might be a typo or missing text in your request. Could you please provide the Korean text you would like translated to English? Deletes it..
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

Below is Request The main text Field Regarding This is an explanation..
| Field name          | Type              | Essential Whether |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Essential     | Delete LVS Path |
| `uuid`        | `string`         | Choice     | uuid         |


**4. Example Usage of Commands**  
`bdevName`This `nvme9472n1`In English, "인" by itself doesn't provide enough context for translation as it can function differently depending on usage (e.g., as a suffix, part of a word, etc.). Could you please provide more context or the full text? Device LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Create For Below command I use it..
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
```
```

LVS Name `lvs9472_1st` LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Delete For Below command I use it..
```

**Delete the LVS named `lvs9472_1st` using the following command:**## Logical Volume
A Logical Volume (LVol) is a virtual disk partition that abstracts physical storage devices for easier management and use.**1. Creation**Create an LVol by calling the `POST /volumes/lvol` endpoint of the REST API.
> This API can only be invoked by accounts with administrative privileges.**Logical Volume (LVol)** is a virtual disk partition abstracted from physical storage devices for use.

**1. Creation**To create an LVol, invoke the REST API endpoint `POST /volumes/lvol`.
> This API can only be called by accounts with administrative privileges.

**Request Body Field Descriptions:**
| Field Name       | Type    | Required | Description                                      |
|------------------|---------|----------|--------------------------------------------------|
| `alias`          | `string`| Required | LVS name where the LVol will be created           |
| `lvol_name`      | `string`| Required | Name of the LVol to be created                    |
| `size_in_mib`    | `uint64`| Required | Size                                             |
| `thin_provision` | `boolean`| Optional | Indicates whether thin provisioning is used       |
| `uuid`           | `string`| Optional | UUID                                             |**2. Inquiry**Call the `GET /volumes/lvol` endpoint of the REST API to retrieve the created Logical Volume (LVol).**Fields Description** in the request body:
| Field Name               | Type        | Required |                          |
|--------------------|------------|---------|--------------------------|
| `alias`            | `string`   | Yes     | LVol location alias      |
| `lvol_name`        | `string`   | Yes     | LVol name to create      |
| `size_in_mib`      | `uint64`   | Yes     | Size                      |
| `thin_provision`   | `boolean`  | Optional| Thin provisioning status  |
| `uuid`             | `string`   | Optional| UUID                      |

**2. Retrieval**To retrieve created Logical Volumes (LVols), invoke the REST API endpoint `GET /volumes/lvol`.

Here is an explanation of the query parameters:

| Field Name       | Type    | Required | Description                  |
|------------------|---------|----------|------------------------------|
| `alias`          | `string`| Optional | LVol path                    |**3. Delete**Delete the LVS by calling the `DELETE /volumes/lvol` endpoint of the REST API.**Query Parameters Description**:
| Field Name                                 | Type              | Required |             |
|--------------------------------------|------------------|---------|-------------|
| `alias`                              | `string`         | Optional| LVol path   |

**3. Deletion**To delete an LVS, invoke the REST API endpoint `DELETE /volumes/lvol`.

**Request Body Field Descriptions:**
| Field Name | Type    | Required | Description                               |
|------------|---------|----------|-------------------------------------------|
| `alias`    | `string`| Required | Path of the LVOL to be deleted             |**4. Example Usage of Commands**Use the following command to create an LV (Logical Volume) named `lvol9472_1st` under an LVS (Logical Volume Server) named `lvs9472_1st`: 

```
sudo lvconvert --yes --lv /path/to/lvs9472_1st/lvol9472_1st
``` 

(Note: Replace `/path/to/lvs9472_1st` with the actual path to your LVS.)**Fields Description** in the request body:
| Field Name          | Type              | Required |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Yes     | LVol path to delete |

**4. Command Example Usage**To create an LVol named `lvol9472_1st` under LVS named `lvs9472_1st`, use the following command:

```
# Command placeholder for actual LV creation syntax
```

To retrieve the created LVol, use the following command:

```
lvdisplay /dev/<VG_NAME>/lvol9472_1st
```

To delete the LVol located at the path `lvs9472_1st/lvol9472_1st`, use the following command:

```
lvremove /dev/<VG_NAME>/lvol9472_1st
```

## Expose Logical Volume to External Hosts via NVMe-oF
To access volumes in PBSSD via NVMe-oF from an initiator, first attach the corresponding volume.
Once attached, the volume will be recognized as a block device through a normal NVMe-oF connection from the initiator, enabling file I/O operations. [For the process of connecting an initiator to PBSSD via NVMe-oF, refer to the NVMe-oF documentation page.] (0300-nvmeof-connection.md)**1. Command**Attach an LVol using the `POST /volumes/lvol/attach` endpoint of the REST API.
> This API can only be invoked by accounts with administrative privileges.**1. Command**  
Invoke the REST API endpoint `POST /volumes/lvol/attach` to attach an LVol.
> This API requires administrative privileges.
```bash
[TRANSLATION_END]

```

**2. Example Usage of Commands**  
`lvs9472_1st`Name's LVSInside `lvol9472_1st` Name's LVolThe provided text "을" translates to "as" or depends on context, often functioning as a particle indicating the object of a verb in Korean sentences. Without additional context, a direct translation isn't fully illustrative, but generally:

**"as"** (in comparative contexts) or **"object marker"** (functionally). `attach` To do so Below command I use it..
```

**2. Command Example Usage**  
Use the following command to attach an `lvol` named `lvol9472_1st` within LVS named `lvs9472_1st`.
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