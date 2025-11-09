# Volume and Volume Store: Basic Operations
이 문서에서는 기본적인 볼륨(volume)기능 관련 REST API를 설명하고, 각 API의 사용 예시를 제공합니다.

이 문서에서는 다음과 같은 내용을 다룹니다.
1. [Logical Volume Store](#logical-volume-store)  
   1.1. 생성  
   1.2. 조회  
   1.3. 삭제
2. [Logical Volume](#logical-volume)  
   2.1. 생성  
   2.2. 조회  
   2.3. 삭제
3. [Attach Volume via NVMe-oF](#expose-logical-volume-to-external-hosts-via-nvme-of)  

이 문서에서는 다음과 같은 목표와 환경을 가정합니다.
- 목표: REST API를 통해 PBSSD의 볼륨(volume)을 관리
- 환경:
  - PBSSD가 정상적으로 실행되고 박스 초기화가 완료되어 `Total` 상태가 `OK`인 상황
  - PBSSD는 IP 주소 `10.1.3.8`를 할당받은 상태
  - 사용 예시에서 참조하는 디바이스 정보는 아래 표와 같습니다:
    - ```bash
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
> **사용 예시 참고:**
> - REST API 요청
>   - 관리자 계정으로 `admin:admin`을 사용한다고 가정합니다.
>   - self-signed 인증서를 사용한다고 가정하여, `curl` 명령에 `-k` 옵션을 포함하여 명령어를 작성하였습니다.

## Logical Volume Store
LVS(Logical Volume Store)는 물리적 NVMe 장치 또는 LVol 위에 계층을 구성하여, 사용자가 필요에 따라 크기와 성능이 다른 볼륨을 동적으로 생성·삭제할 수 있도록 지원하는 추상화 계층입니다.

**1. 생성**   
REST API의 `POST /volumes/lvstore` 엔드포인트를 호출하여 LVS를 생성합니다.
> 이 API는 관리자 권한이 있는 계정으로만 호출할 수 있습니다.
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

아래는 요청 본문의 필드에 대한 설명입니다.
| 필드명                                | 타입               | 필수 여부 |                                   |
|--------------------------------------|------------------|---------|-----------------------------------|
| `alias`                              | `string`         | 필수     | LVS를 생성할 위치 (ex. bdev 또는 LVol) |
| `lvs_name`                           | `string`         | 필수     | 생성할 LVS 이름                      |
| `cluster_sz`                         | `uint32`         | 선택     | 클러스터 크기                         |
| `clear_method`                       | `string`         | 선택     | LVS 생성 전 저장 공간 초기화 방식        |
| `num_md_pages_per_cluster_ratio`     | `uint32`         | 선택     | 클러스터당 메타데이터 페이지 비율          |

**2. 조회**  
REST API의 `GET /volumes/lvstore` 엔드포인트를 호출하여 LVS를 조회합니다.
```bash
curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Accept: application/json' \
'https://<IP_ADDRESS>/api/v1/volumes/lvstore'
```

아래는 쿼리 파라미터에 대한 설명입니다.
| 필드명                                   | 타입               | 필수 여부 |             |
|-----------------------------------------|------------------|---------|-------------|
| `lvs_name`                              | `string`         | 선택     | LVStore 이름 |

**3. 삭제**  
REST API의 `DELETE /volumes/lvstore` 엔드포인트를 호출하여 LVS를 삭제합니다.
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

아래는 요청 본문의 필드에 대한 설명입니다.
| 필드명          | 타입              | 필수 여부 |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | 필수     | 삭제할 LVS 경로 |
| `uuid`        | `string`         | 선택     | uuid         |


**4. 명령어 사용 예시**  
`bdevName`이 `nvme9472n1`인 디바이스에 LVS를 생성하기 위해 아래 명령어를 사용합니다.
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

만들어진 LVS를 조회하기 위해 아래 명령어를 사용합니다.
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

LVS 이름이 `lvs9472_1st` LVS를 삭제하기 위해 아래 명령어를 사용합니다.
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
LVol(Logical Volume)은 물리적 저장 장치를 추상화하여 사용할 수 있는 가상의 디스크 파티션입니다.

**1. 생성**  
REST API의 `POST /volumes/lvol` 엔드포인트를 호출하여 LVol를 생성합니다.
> 이 API는 관리자 권한이 있는 계정으로만 호출할 수 있습니다.
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

아래는 요청 본문의 필드에 대한 설명입니다.
| 필드명               | 타입        | 필수 여부 |                          |
|--------------------|------------|---------|--------------------------|
| `alias`            | `string`   | 필수     | LVol이 생성될 위치의 LVS 이름 |
| `lvol_name`        | `string`   | 필수     | 생성할 LVol 이름            |
| `size_in_mib`      | `uint64`   | 필수     | 크기                      |
| `thin_provision`   | `boolean`  | 선택     | thin provision 유무       |
| `uuid`             | `string`   | 선택     | uuid                     |

**2. 조회**  
REST API의 `GET /volumes/lvol` 엔드포인트를 호출하여 생성된 LVol(Logical Volume)을 조회합니다.
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
https://<IP_ADDRESS>/api/v1/volumes/lvol
```

아래는 쿼리 파라미터에 대한 설명입니다.
| 필드명                                 | 타입              | 필수 여부 |             |
|--------------------------------------|------------------|---------|-------------|
| `alias`                              | `string`         | 선택     | LVol 경로    |

**3. 삭제**  
REST API의 `DELETE /volumes/lvol` 엔드포인트를 호출하여 LVS를 삭제합니다.
```bash
curl -k -X DELETE \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "alias": "<LVOL_NAME>",
}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol'
```

아래는 요청 본문의 필드에 대한 설명입니다.
| 필드명          | 타입              | 필수 여부 |              |
|---------------|------------------|---------|--------------|
| `alias`       | `string`         | 필수     | 삭제할 LVol 경로 |

**4. 명령어 사용 예시**  
`lvs9472_1st`라는 이름의 LVS에 `lvol9472_1st`라는 이름의 LVol 생성하기 위해 아래 명령어를 사용합니다.
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

만들어진 LVol 조회하기 위해 아래 명령어를 사용합니다.
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

`lvs9472_1st/lvol9472_1st` 경로의 LVol를 삭제하기 위해 아래 명령어를 사용합니다.
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
NVMe-oF(NVMe over Fabrics)를 통해 이니시에이터(initiator)에서 PBSSD의 볼륨에 접근하려면, 먼저 해당 볼륨을 `attach`해야 합니다.
`attach`된 볼륨은 이니시에이터에서 정상적으로 NVMe-oF 연결을 통해 블록 장치로 인식되며, 파일 I/O 작업이 가능해집니다. [이니시에이터에서 PBSSD에 연결하는 과정은 NVMe-oF 페이지에서 다룹니다.](0300-nvmeof-connection.md)

**1. 명령어**  
REST API의 `POST /volumes/lvol/attach` 엔드포인트를 호출하여 LVol을 `attach` 합니다.
> 이 API는 관리자 권한이 있는 계정으로만 호출할 수 있습니다.
```bash
curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "<LVOL_PATH>"}' \
'https://<IP_ADDRESS>/api/v1/volumes/lvol/attach'
```

**2. 명령어 사용 예시**  
`lvs9472_1st`이름의 LVS안의 `lvol9472_1st` 이름의 LVol을 `attach` 하기위해 아래 명령어를 사용합니다.
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