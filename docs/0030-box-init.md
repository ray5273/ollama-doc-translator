# PBSSD Box Initialization Guide
박스 초기화(Box Initialization)는 NVMe-oF(NVMe over Fabrics) 타깃(target) PBSSD의 설정을 초기화하는 과정입니다. PBSSD 내부에서 초기화할 수도 있지만, 이 문서에서는 NVMe-oF 이니시에이터(initiator)를 통해 PBSSD를 초기화하는 절차를 안내합니다.

이 문서에서는 다음과 같은 목표와 환경을 가정합니다.
- 목표: REST API를 통한 `volume`, `nvmeof`, `tcp`모드로 PBSSD에 박스 초기화
- 환경:
  - PBSSD 펌웨어 설치, 실행(orc_run) 및 네트워크 설정이 완료한 상태
  - PBSSD는 IP 주소 `10.1.3.8`를 할당받은 상태

> **사용 예시 참고:**
> - REST API 요청
>   - 관리자 계정으로 `admin:admin`을 사용한다고 가정합니다.
>   - self-signed 인증서를 사용한다고 가정하여, `curl` 명령에 `-k` 옵션을 포함하여 명령어를 작성하였습니다.

## PBSSD Status Check Before Box Initialization
박스 초기화 전 상태에서 각 명령어에 대한 응답을 작성하였습니다.

**1. REST API로 PBSSD 상태 확인**  
REST API의 `GET /firmware/status` 엔드포인트를 호출하여 PBSSD 펌웨어 통합 상태와 모듈별 상태와 버전을 확인합니다. `pos-essential-orchestrator`는 박스 초기화가 필요하며, `pos-essential-ioworker`는 박스 초기화가 완료되지 않아 `Not Running` 상태 입니다.
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

**2. 네트워크 설정 확인**  
REST API의 `GET /settings/network` 엔드포인트를 호출하여 PBSSD 네트워크 설정을 확인합니다.

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
REST API의 `POST /settings/init` 엔드포인트를 호출하여 PBSSD 박스 초기화를 진행합니다.
> 이 API는 관리자 권한이 있는 계정으로만 호출할 수 있습니다.
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
박스 초기화가 정상적으로 완료된 상태에서 각 명령에 대한 응답을 작성하였습니다.

**1. REST API로 PBSSD 상태 확인**  
REST API의 `GET /firmware/status` 엔드포인트를 호출하여 PBSSD 펌웨어 통합 상태와 모듈별 상태와 버전을 확인합니다. 박스 초기화가 정상적으로 완료되었다면 `pos-essential-orchestrator`와 `pos-essential-ioworker`는 `Running` 상태이며, `Total`상태는 `OK`입니다.
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
