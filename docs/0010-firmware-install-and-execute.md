# PBSSD Firmware Installation & Execution Guide
이 문서에서는 PBSSD 펌웨어 설치(PBSSD Firmware Installation) 및 실행(PBSSD Firmware Execution) 절차를 안내합니다.

이 문서에서는 다음과 같은 목표와 환경을 가정합니다.
- 목표: PBSSD 펌웨어 설치 및 실행을 제어
- 환경: PBSSD 펌웨어 데비안 패키지가 준비된 상태

> **사용 예시 참고:**
> - 환경에 따라 일부 명령은 `sudo` 권한이 필요할 수 있습니다.
> - REST API 요청
>   - 관리자 계정으로 `admin:admin`을 사용한다고 가정합니다.
>   - self-signed 인증서를 사용한다고 가정하여, `curl` 명령에 `-k` 옵션을 포함하여 명령어를 작성하였습니다.

## PBSSD Firmware Installation
PBSSD 펌웨어 설치 절차입니다.

**1. 펌웨어 패키지 설치**  
아래 명령어를 사용하여 펌웨어를 설치합니다.  
_주의: PBSSD 펌웨어 데비안 패키지는 설치 전 반드시 `/tmp` 디렉토리에 위치해야 합니다._
```bash
$ apt install /tmp/pos-essential_2.6.0_arm64.deb
```
```bash
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
...
```

**2. 펌웨어 설치 확인**  
PBSSD 펌웨어 설치가 완료되면, `docker images` 명령어를 실행하여 PBSSD 관련 컨테이너 이미지가 정상적으로 로드되었는지 확인합니다.
```bash
$ docker images
```
```bash
REPOSITORY                         TAG                  IMAGE ID       CREATED         SIZE
anomaly_detector                   2.6.0                5bc6c9128795   5 hours ago     93.3MB
anomaly_detector                   latest               5bc6c9128795   5 hours ago     93.3MB
iow_bin                            2.6.0                32e2bc79fc17   5 hours ago     2.73GB
iow_bin                            latest               32e2bc79fc17   5 hours ago     2.73GB
pos-essential-management-ui        2.6.0                44b51bd6950d   5 hours ago     202MB
pos-essential-management-ui        latest               44b51bd6950d   5 hours ago     202MB
fluent/fluent-bit                  2.2.0                f2a704f310c2   24 months ago   81.5MB
fluent/fluent-bit                  2.6.0                f2a704f310c2   24 months ago   81.5MB
jaegertracing/all-in-one           1.50                 06ec8144ca8c   2 years ago     57.4MB
jaegertracing/all-in-one           2.6.0                06ec8144ca8c   2 years ago     57.4MB
grafana/loki                       2.6.0                33a5847e7daf   2 years ago     72.4MB
grafana/loki                       2.9.0                33a5847e7daf   2 years ago     72.4MB
prom/prometheus                    2.6.0                eb8939d5c174   2 years ago     240MB
prom/prometheus                    v2.47.0              eb8939d5c174   2 years ago     240MB
quay.io/prometheus/node-exporter   2.6.0                6a33998eca8a   2 years ago     21.9MB
quay.io/prometheus/node-exporter   v1.6.0               6a33998eca8a   2 years ago     21.9MB
otel/opentelemetry-collector       0.77.0               afb19f2adefc   2 years ago     90.7MB
otel/opentelemetry-collector       2.6.0                afb19f2adefc   2 years ago     90.7MB
```

## PBSSD Status Check Before Starting PBSSD Firmware
PBSSD 펌웨어가 실행되기 전 상태에서 각 명령어에 대한 응답을 작성하였습니다.

**1. 서비스 상태 확인**  
설치된 PBSSD 펌웨어는 여러 서비스로 구성되어 있으며, 서비스 상태는 아래 명령어로 확인합니다. 현재 PBSSD 펌웨어 서비스가 실행되지 않은 상태이므로, PBSSD 서비스 상태는 `inactive`입니다.
```bash
$ systemctl status orc_init
```
```bash
○ orc_init.service - Daemon for running a script for pre-settings required before executing Pos Essential Orchestrator
     Loaded: loaded (/etc/systemd/system/orc_init.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Tue 2025-10-30 04:23:34 UTC; 26min ago
     ...
```
```bash
$ systemctl status orc_run
```
```bash
○ orc_run.service - pos-essential-orchestrator
     Loaded: loaded (/etc/systemd/system/orc_run.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Tue 2025-10-30 04:23:34 UTC; 26min ago
     ...
```

**2. 컨테이너 상태 확인**  
설치된 PBSSD 펌웨어는 컨테이너 형태로 동작하며, 컨테이너 실행 상태는 아래 명령어로 확인합니다. 현재 PBSSD 펌웨어 서비스가 실행되지 않은 상태이므로, 관련 컨테이너는 실행 중이지 않습니다.
```bash
$ docker ps
```
```bash
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

**3. 스토리지 상태 확인**  
스토리지 상태는 아래 명령어로 확인합니다. `nvme list`명령어를 사용하여 운영체제에 등록된 NVMe 장치를 확인할 수 있습니다.  
_참고: PBSSD 펌웨어가 실행된 후에는 NVMe 장치가 펌웨어에 의해 관리되므로, PBSSD가 관리하는 NVMe 장치는 위 명령어를 통해 더 이상 노출되지 않습니다._
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme0n1          /dev/ng0n1            S871NG0Y200017       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme10n1         /dev/ng10n1           Y3P200LXNSJ4         KBG40ZPZ128G TOSHIBA MEMORY              0x1        128.04  GB / 128.04  GB    512   B +  0 B   AEGA0103
/dev/nvme11n1         /dev/ng11n1           S871NG0Y200018       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme12n1         /dev/ng12n1           S871NG0Y200015       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
/dev/nvme1n1          /dev/ng1n1            S871NG0Y200022       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme2n1          /dev/ng2n1            S871NG0Y200019       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme3n1          /dev/ng3n1            S871NG0Y200014       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme4n1          /dev/ng4n1            S871NG0Y200016       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme5n1          /dev/ng5n1            S871NG0Y200023       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00  GB /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme6n1          /dev/ng6n1            S871NG0Y200069       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme7n1          /dev/ng7n1            S871NG0Y200070       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
/dev/nvme8n1          /dev/ng8n1            S871NG0Y200074       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
/dev/nvme9n1          /dev/ng9n1            S871NG0Y200071       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
```

## Starting PBSSD Firmware
`orc_run` 서비스를 시작하여 PBSSD 펌웨어를 실행합니다.
```bash
$ systemctl start orc_run
```
## PBSSD Status Check After Starting PBSSD Firmware
PBSSD 펌웨어가 실행 중인 상태에서 각 명령어에 대한 응답을 아래에 작성하였습니다.

**1. 서비스 상태 확인**  
`orc_init`과 `orc_run`서비스의 상태는 아래 명령어로 확인합니다. `Active: active` 상태여야 하며, `orc_run`은 `running` 상태여야 합니다.
```bash
$ systemctl status orc_init
```
```bash
● orc_init.service - Daemon for running a script for pre-settings required before executing Pos Essential Orchestrator
     Loaded: loaded (/etc/systemd/system/orc_init.service; enabled; vendor preset: enabled)
     Active: active (exited) since Tue 2025-10-30 04:51:17 UTC; 3s ago
     ...
```
```bash
$ systemctl status orc_run
```
```bash
● orc_run.service - pos-essential-orchestrator
     Loaded: loaded (/etc/systemd/system/orc_run.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2025-10-30 04:51:17 UTC; 3s ago
     ...
```
**2. 컨테이너 상태 확인**  
컨테이너 실행 상태는 아래 명령어로 확인합니다. PBSSD 펌웨어 서비스가 정상적으로 실행되었다면, 다음 다섯 개의 컨테이너가 중일 것입니다. `ui`, `prometheus`, `node-exporter`, `opentelemetry-collector`, `anomaly_detector`
```bash
$ docker ps
```
```bash
CONTAINER ID   IMAGE                                     COMMAND                  CREATED          CONTAINER ID   IMAGE                                     COMMAND                  CREATED        STATUS        PORTS     NAMES
38458f7fbb0b   quay.io/prometheus/node-exporter:v1.6.0   "/bin/node_exporter …"   1 second ago   Up 1 second             pos-essential-node-exporter
f5aca9be9211   prom/prometheus:v2.47.0                   "/bin/prometheus --w…"   1 second ago   Up 1 second             pos-essential-prometheus
f1137a330130   pos-essential-management-ui:latest        "python3 rest/app.py"    1 second ago   Up 1 second             pos-essential-management-ui
2070f50fa42b   anomaly_detector:latest                   "/bin/sh -c ./main"      1 second ago   Up 1 second             pos-essential-ssd-anomaly-detector
6877e9285056   otel/opentelemetry-collector:0.77.0       "/otelcol --config /…"   1 second ago   Up 1 second             pos-essential-opentelemetry-collector
```

**3. 스토리지 상태 확인**  
`orc_run` 서비스를 통해 PBSSD 펌웨어를 실행하면, PBSSD 펌웨어가 NVMe 장치를 운영체제에서 가져와 직접 제어합니다. 따라서 PBSSD 펌웨어가 제어하는 NVMe 장치들은 `nvme list`명령어를 통해 노출되지 않으며, 운영체제가 설치되어 있는 SSD만 표시됩니다. 스토리지 상태는 아래 명령어로 확인합니다.
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme10n1         /dev/ng10n1           Y3P200LXNSJ4         KBG40ZPZ128G TOSHIBA MEMORY              0x1        128.04  GB / 128.04  GB    512   B +  0 B   AEGA0103
# Most of nvme devices is not shown by nvme list command because they are controlled in user space by PBSSD.
```

**4. REST API로 PBSSD 상태 확인**  
REST API의 `GET /firmware` 엔드포인트를 호출하여 PBSSD 펌웨어의 현재 버전 정보를 조회합니다.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://localhost/api/v1/firmware'
```
```bash
{
  "commit": "70b5ec9982b62a567524042eb54797062264f68a",
  "lastUpdated": "2025-10-30-02:59:54-UTC",
  "name": "PBSSD-Edinburgh-Essential-Firmware",
  "version": "2.6.0"
}
```
REST API의 `GET /firmware/status` 엔드포인트를 호출하여 PBSSD 펌웨어의 통합 상태와 모듈별 상태와 각 구성 서비스의 버전을 조회합니다. `FirmwareServices`의 `Total` 필드는 전체 시스템 상태를 나타내며, 이 외의 모든 `name` 필드는 PBSSD 펌웨어를 구성하는 개별 모듈들입니다. 아래 예시에서는 박스 초기화(Box Initialization) 미완료된 경우입니다. 따라서 PBSSD 펌웨어에서 IO를 담당하는 `pos-essential-ioworker` 모듈의 상태는 `Not Running`이며, `Total` 상태는 `Failed`입니다.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://localhost/api/v1/firmware/status'
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
REST API의 `GET /devices` 엔드포인트를 호출하여 PBSSD 펌웨어가 제어하는 NVMe 장치의 정보를 확인합니다.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://localhost/api/v1/devices'
```
```bash
{
  "devices": [
    {
      "address": "0000:1d:00.0",
      "bdevName": "nvme7424n1",
      "capabilities": [],
      "firmware": {
        "name": "OPRA4B5Q"
      },
      "modelNumber": "SAMSUNG MZWMO30THCLF-00AW7",
      "numa": -1,
      "serialNumber": "S871NG0Y200070",
      "size": 30720827326464,
      "slotId": 7424,
      "status": -20
    },
    {
      "address": "0000:29:00.0",
      "bdevName": "nvme10496n1",
      "capabilities": [],
      "firmware": {
        "name": "OPRATB57"
      },
      "modelNumber": "SAMSUNG MZWMO30THCLF-01AW7",
      "numa": -1,
      "serialNumber": "S871NG0Y200018",
      "size": 30720827326464,
      "slotId": 10496,
      "status": -20
    },
    ...
  ],
  "message": "Devices retrieved successfully",
  "relatedJobs": null
}
```
## Stopping PBSSD Firmware 
`orc_run` 서비스를 중지하면 PBSSD 펌웨어의 실행이 중지됩니다.
```bash
$ systemctl stop orc_run
```