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
>   - Manager Account `admin:admin`The provided text "을" translates to "as" or depends on context, often functioning as a particle indicating the object of a verb in Korean sentences. Without additional context, a direct translation isn't fully illustrative, but generally:

**"as"** (in comparative contexts) or **"object marker"** (functionally). 

Please provide more context if a specific translation is needed. Used it Assume.
>   - self-signed Certificate Used it Assuming, `curl` According to instructions `-k` Options Including command I have written it..

## Logical Volume Store
LVS(Logical Volume Store)It seems there might be a typo or incomplete text provided ("는"). Could you please provide the full Korean text you would like translated? Physical NVMe Device Or LVol Above Hierarchy Composed, The user According to need Following Size and performance Other Volume Dynamically Creation·Delete Water To enable/make possible Supporting Abstraction It is a hierarchy..

**1. Creation**   
REST APIIt seems there might be a typo or incomplete text provided ("의" alone doesn't form a complete phrase). Could you please provide the full Korean text you would like translated? `POST /volumes/lvstore` Endpoint Call to LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? I create..
> This APIIs Manager Authority Exists By account only To call Water It exists..
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
| `alias`                              | `string`         | Essential     | LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Creating Location (ex. bdev Or LVol) |
| `lvs_name`                           | `string`         | Essential     | To create LVS Name                      |
| `cluster_sz`                         | `uint32`         | Choice     | Cluster Size                         |
| `clear_method`                       | `string`         | Selection     | LVS Creation The provided Korean text "전" translates to "before" in English. However, please note that context is crucial for accurate translation, and "전" can have different meanings depending on its usage in a sentence. Without additional context, this is the most straightforward translation. Storage Space Initialization Method        |
| `num_md_pages_per_cluster_ratio`     | `uint32`         | Choice     | Per cluster Metadata Page Ratio          |

**2. Inquiry**  
REST APIIt seems there might be a typo or incomplete text provided ("의" alone doesn't form a complete phrase). Could you please provide the full Korean text you would like translated? `GET /volumes/lvstore` Endpoint Call to LVSPlease provide the Korean text you would like translated. Checking.
```bash
curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Accept: application/json' \
'https://<IP_ADDRESS>/api/v1/volumes/lvstore'
```

Below is Query parameters to Regarding This is an explanation..
| Field name                                   | Type               | Essential Whether |             |
|-----------------------------------------|------------------|---------|-------------|
| `lvs_name`                              | `string`         | Choice     | LVStore Name |

**3. Delete**  
REST APIThe provided Korean text "의" translates to "of" or "for" in English, depending on the context. Without additional context, a direct translation cannot specify which usage is intended. Could you please provide more context or text for a precise translation? `DELETE /volumes/lvstore` Endpoint Call them LVSPlease provide the Korean text you would like translated. Deletes it..
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

| Field name          | Type              | Essential Whether |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Essential     | Delete LVS Path |
| `uuid`        | `string`         | Choice     | uuid         |


**4. Example Usage of Commands**  
`bdevName`This `nvme9472n1`In English, the provided Korean text "인" translates to "Person" or could be part of a larger context needing more text for accurate translation. Given only "인", it commonly refers to "person" in many contexts. Device LVSIt seems there might be a typo or missing text in your request. Could you please provide the Korean text you would like translated to English? Create For Below command I use it..
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

Created LVSIt seems like your text might be incomplete. Could you please provide the full Korean text you would like translated? Search For Below command I use it..
```bash
curl -k -X GET \
[TRANSLATION_END]

```
```
```

LVS Name is `lvs9472_1st` LVSIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Delete For Below command I use it..
```

**Delete the LVS named `lvs9472_1st` using the following command:**## Logical Volume
A Logical Volume (LVol) is a virtual disk partition that abstracts physical storage devices, making them usable in a more organized manner.**1. Creation**Create an LVol by calling the `POST /volumes/lvol` endpoint of the REST API.
> This API can only be invoked by accounts with administrative privileges.**Logical Volume (LVol)** is a virtual disk partition that abstracts physical storage devices for use.

**1. Creation**To create an LVol, call the `POST /volumes/lvol` endpoint of the REST API.
> This API can only be invoked by accounts with administrative privileges.

Here is a description of the fields in the request body:

| Field Name       | Type    | Required | Description                                      |
|------------------|---------|----------|--------------------------------------------------|
| `alias`          | `string`| Required | LVS name where the LVol will be created           |
| `lvol_name`      | `string`| Required | Name of the LVol to be created                    |
| `size_in_mib`    | `uint64`| Required | Size                                             |
| `thin_provision` | `boolean`| Optional | Indicates whether thin provisioning is used       |
| `uuid`           | `string`| Optional | UUID                                             |**2. Inquiry**Call the `GET /volumes/lvol` endpoint of the REST API to retrieve the created Logical Volume (LVol).**Fields Description:**

| Field Name               | Type        | Required |                          |
|--------------------|------------|---------|--------------------------|
| `alias`            | `string`   | Yes     | LVol location alias      |
| `lvol_name`        | `string`   | Yes     | LVol name                |
| `size_in_mib`      | `uint64`   | Yes     | Size                      |
| `thin_provision`   | `boolean`  | Optional| Thin provision flag       |
| `uuid`             | `string`   | Optional| UUID                      |

**2. Retrieval**To retrieve the created LVol (Logical Volume), call the `GET /volumes/lvol` endpoint of the REST API.

Here is an explanation of the query parameters:

| Field Name       | Type    | Required | Description                  |
|------------------|---------|----------|------------------------------|
| `alias`          | `string`| Optional | LVol path                    |**3. Delete**Delete the LVS by calling the `DELETE /volumes/lvol` endpoint of the REST API.**Query Parameters Description:**

| Field Name                                 | Type              | Required |             |
|--------------------------------------|------------------|---------|-------------|
| `alias`                              | `string`         | Optional| LVol path   |

**3. Deletion**To delete the LVS, call the `DELETE /volumes/lvol` endpoint of the REST API.

**Fields Description for Request Body:**

| Field Name | Type    | Required | Description                  |
|------------|---------|----------|------------------------------|
| `alias`    | `string`| Yes      | Path of the LVol to be deleted |**4. Example Usage of Commands**Use the following command to create an LV (Logical Volume) named `lvol9472_1st` under an LVS (Logical Volume Server) named `lvs9472_1st`: 

```
sudo lvconvert --yes --lv /path/to/lvs9472_1st/lvol9472_1st
``` 

(Note: Replace `/path/to/lvs9472_1st` with the actual path to your LVS.)**Request Body Fields Description:**

| Field Name          | Type              | Required |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | Yes     | LVol path to delete |

**4. Command Example Usage**To create an LVol named `lvol9472_1st` under the LVS named `lvs9472_1st`, use the following command:
```
lvcreate -l <size> -n lvol9472_1st lvs9472_1st
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
To access volumes in PBSSD from an initiator via NVMe-oF (NVMe over Fabrics), first attach the corresponding volume. Once attached, the volume will be recognized as a block device through a normal NVMe-oF connection from the initiator, enabling file I/O operations. [The process of connecting an initiator to PBSSD via NVMe-oF is covered in the NVMe-oF section](0300-nvmeof-connection.md).**1. Command**Attach an LVol using the `POST /volumes/lvol/attach` endpoint of the REST API.
> This API can only be invoked by accounts with administrative privileges.**1. Command**  
Call the `POST /volumes/lvol/attach` endpoint of the REST API to attach an LVol.
> This API can only be invoked by accounts with administrative privileges.
```bash
[TRANSLATION_END]```

```

**2. Example Usage of Commands**  
`lvs9472_1st`Name's LVSInside `lvol9472_1st` Name's LVolThe provided text "을" translates to "as" or depends on context, often functioning as a particle indicating the object of a verb in Korean sentences. Without additional context, a direct translation isn't fully illustrative, but generally:

**"as"** (in comparative contexts) or **"object marker"** (functionally). `attach` To do so Below command I use it..
```

**2. Command Usage Example**  
To attach an `lvol` named `lvol9472_1st` within LVS named `lvs9472_1st`, use the following command:
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