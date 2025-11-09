# NVMe-oF Connection Guide
이 문서에서는 NVMe-oF(NVMe over Fabrics) 프로토콜을 사용하여 PBSSD와 이니시에이터(initiator)를 연결하는 절차를 안내합니다. PBSSD 펌웨어 설치와 박스 초기화(Box Initialization)가 완료되고 볼륨이 `attach` 되었으면, PBSSD는 I/O 명령처리할 준비가 되었습니다. 

이 문서에서는 다음과 같은 목표와 환경을 가정합니다.
- 목표: 이니시에이터에서 100Gbps 네트워크 인터페이스를 사용하여 PBSSD 타깃의 NVMe-oF 서브시스템에 연결
- 환경:
  - PBSSD의 박스 초기화가 완료되었으며, 사용할 볼륨이 정상적으로 `attach`된 상태입니다.
  - PBSSD는 100Gbps 네트워크 인터페이스를 통해 이니시에이터와 연결되어 있으며, IP 주소 `10.100.3.8`를 사용
  - 박스 초기화는 TCP 기반 연결을 통해 완료되었으며, NVMe-oF는 TCP 전송 계층을 사용

> **사용 예시 참고:**
> - 환경에 따라 일부 명령은 `sudo` 권한이 필요할 수 있습니다.

## Discovering NVMe-oF Devices
이니시에이터는 PBSSD가 제공하는 NVMe 장치에 연결하기 전, `nvme discover` 명령어를 사용하여 NVMe-oF 네트워크에서 검색 가능한 NVMe-oF 서브시스템(NVMe Qualified Name, NQN) 목록을 확인해야 합니다.

**1. 명령어**  
`nvme discover` 명령어는 아래 형식으로 사용하여, 지정한 전송 프로토콜, 주소(traddr), 포트(trsvcid)에 해당하는 NVMe-oF 서브시스템 목록을 조회할 수 있습니다.
```bash
$ nvme discover -t <TRANSPORT_PROTOCOL> -a <TRANSPORT_ADDRESS> -s <TRANSPORT_SERVICE>
```
아래는 명령어 옵션에 대한 설명입니다.

| 옵션                   | 플래그 | 설명                                                                                            |
|------------------------|------|-----------------------------------------------------------------------------------------------|
| `transport protocol`   | `-t` | NVMe-oF(NVMe over Fabrics) 환경에 사용중인 네트워크 전송 프로토콜(예: `tcp`, `rdma`)                     |
| `transport address`    | `-a` | NVMe-oF(NVMe over Fabrics) 환경에 사용중인 네트워크 전송 프로토콜                                       |
| `transport service ID` | `-s` | NVMe-oF(NVMe over Fabrics) 환경에 사용중인 네트워크 서비스 식별자 (PBSSD I/O default port : 1152, 1153) |

**2. 명령어 사용 예시**  
`nvme discover` 명령어를 통해 타깃 PBSSD가 제공하는 NVMe-oF 서브시스템(NVMe Qualified Name, NQN) 목록을 조회합니다.
```bash
$ nvme discover -t tcp -a 10.100.3.8 -s 1152
```
```bash
Discovery Log Number of Records 8, Generation counter 8
=====Discovery Log Entry 0======
trtype:  tcp
adrfam:  ipv4
subtype: current discovery subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2014-08.org.nvmexpress.discovery
traddr:  10.100.3.8
eflags:  explicit discovery connections, duplicate discovery information
sectype: none
=====Discovery Log Entry 1======
trtype:  tcp
adrfam:  ipv4
subtype: current discovery subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2014-08.org.nvmexpress.discovery
traddr:  10.10.100.12
eflags:  explicit discovery connections, duplicate discovery information
sectype: none
=====Discovery Log Entry 2======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
traddr:  10.10.100.12
eflags:  none
sectype: none
=====Discovery Log Entry 3======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
traddr:  10.100.3.8
eflags:  none
sectype: none
=====Discovery Log Entry 4======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f
traddr:  10.10.100.12
eflags:  none
sectype: none
=====Discovery Log Entry 5======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f
traddr:  10.100.3.8
eflags:  none
sectype: none
=====Discovery Log Entry 6======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa
traddr:  10.10.100.12
eflags:  none
sectype: none
=====Discovery Log Entry 7======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa
traddr:  10.100.3.8
eflags:  none
sectype: none
```

## Connecting NVMe-oF Devices
`nvme connect` 명령어를 사용하여 NVMe-oF 서브시스템에 연결할 수 있습니다. 이 명령어로 연결된 서브시스템은 이니시에이터의 운영 체제에 NVMe 블록 장치로 등록되며, 로컬 SSD와 동일하게 디바이스 파일(예: /dev/nvme0n1)을 통해 파티션 생성, 포맷, 마운트 등의 블록 I/O 작업을 수행할 수 있습니다.

**1. 명령어**  
`nvme connect` 명령어는 아래와 같은 형식으로 사용하여, 지정한 전송 프로토콜, 주소(traddr), 포트(trsvcid), NQN(NVMe Qualified Name)에 해당하는 NVMe-oF 서브시스템에 연결할 수 있습니다.
```bash
$ nvme connect -t <TRANSPORT_PROTOCOL> -a <TRANSPORT_ADDRESS> -s <TRANSPORT_SERVICE> -n <NQN_NAME>
```
아래는 명령어 옵션에 대한 설명입니다.

| 옵션                    | 플래그 | 설명                                                                                                                               |
|------------------------|------|-----------------------------------------------------------------------------------------------------------------------------------|
| `transport protocol`   | `-t` | NVMe-oF(NVMe over Fabrics) 환경에 사용중인 네트워크 전송 프로토콜(예: `tcp`, `rdma`)                                                         |
| `transport address`    | `-a` | NVMe-oF(NVMe over Fabrics) 환경에 사용중인 네트워크 전송 프로토콜                                                                           |
| `transport service ID` | `-s` | NVMe-oF(NVMe over Fabrics) 환경에 사용중인 네트워크 서비스 식별자 (PBSSD I/O default port : 1152, 1153)                                     |
| `nqn name`             | `-n` | NVMe-oF(NVMe over Fabrics) 타깃(target)을 식별하기 위한 고유 이름 (`nvme connect`명령에서는 `subtype`이 `nvme subsystem`의 `subnqn`을 사용)    |

**2. 명령어 사용 예시**  
`nvme discover` 명령어를 사용하여 검색된 NVMe-oF 서브시스템 중, `traddr`가 `10.100.3.8`인 서브시스템의 NQN을 확인한 후, 이를 `nvme connect` 명령어의 `<NQN_NAME>` 인자에 지정하여 타깃 PBSSD가 제공하는 서브시스템에 연결합니다.
```bash
$ nvme connect -t tcp -n nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f -a 10.100.3.8 -s 1152
$ nvme connect -t tcp -n nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa -a 10.100.3.8 -s 1152
$ nvme connect -t tcp -n nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57 -a 10.100.3.8 -s 1152
```
```bash
connecting to device: nvme0
connecting to device: nvme1
connecting to device: nvme2
```
`nvme list` 명령어를 사용하면 현재 시스템에 연결된 NVMe-oF 장치를 확인할 수 있습니다. PBSSD가 제공하는 NVMe-oF 장치의 Firmware Revision(`FW Rev`) 값은 `25.05`입니다.
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme0n1          /dev/ng0n1            S871NG0Y200019       undefined                                0x1         29.88  TB /  29.88  TB    512   B +  0 B   25.05   
/dev/nvme1n1          /dev/ng1n1            S871NG0Y200015       undefined                                0x1        536.87  MB / 536.87  MB    512   B +  0 B   25.05   
/dev/nvme2n1          /dev/ng2n1            S871NG0Y200015       undefined                                0x1        536.87  MB / 536.87  MB    512   B +  0 B   25.05   
# Local NVMe devices may also be listed here.
```

`nvme list-subsys` 명령어를 사용하여 연결된 NVMe-oF 서브시스템(NVMe Qualified Name, NQN)을 확인할 수 있습니다.
```bash
$ nvme list-subsys
```
```bash
...
nvme-subsys0 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f
               hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
\
 +- nvme0 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live
nvme-subsys1 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa
                hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
\
 +- nvme1 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live

nvme-subsys2 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
                hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
\
 +- nvme2 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live
...
```

## Disconnect NVMe-oF Devices
`nvme disconnect`와 `nvme disconnect-all` 명령어를 사용하여 NVMe-oF 서브시스템과의 연결을 해제할 수 있습니다.

**1. `nvme disconnect` 명령어**  
`nvme disconnect` 명령어는 아래와 같은 형식으로 사용하여, 지정한 NQN에 해당하는 특정 NVMe-oF 서브시스템과의 연결을 해제할 수 있습니다.


```bash
$ nvme disconnect -n <NQN_NAME>
```

**2. `nvme disconnect` 명령어 사용 예시**  
연결된 서브시스템을 조회하여, 해제하고자 하는 서브시스템의 NQN 값을 확인합니다.
```bash
$ nvme list-subsys
```
```bash
...
nvme-subsys2 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
                hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
\
 +- nvme2 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live
...
```
조회된 NQN 값을 `nvme disconnect` 명령어의 `<NQN_NAME>`인자에 지정하여 사용합니다.
```bash
$ nvme disconnect -n nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
```
```bash
NQN:nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57 disconnected 1 controller(s)
```

NVMe-oF 장치가 연결 해제되면, `nvme list` 명령어의 출력 결과에서 해당 장치가 더 이상 표시되지 않습니다.
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme0n1          /dev/ng0n1            S871NG0Y200019       undefined                                0x1         29.88  TB /  29.88  TB    512   B +  0 B   25.05   
/dev/nvme1n1          /dev/ng1n1            S871NG0Y200015       undefined                                0x1        536.87  MB / 536.87  MB    512   B +  0 B   25.05   
# Local NVMe devices may also be listed here.
```

**3. `nvme disconnect-all` 명령어**  
`nvme disconnect-all` 명령어는 아래와 같은 형식으로 사용하여, 현재 연결된 모든 NVMe-oF 서브시스템과의 연결을 해제할 수 있습니다.
```bash
$ nvme disconnect-all 
```

**4. `nvme disconnect-all` 명령어 사용 예시**  
`nvme disconnect-all` 명령어로 연결을 해제합니다.
```bash
$ nvme disconnect-all 
```
연결이 해제되면 `nvme list` 명령어의 출력 결과에서 NVMe-oF 장치가 더 이상 표시되지 않습니다. `nvme disconnect-all` 명령어는 모든 원격 NVMe-oF 장치를 일괄 해제하므로, 로컬 NVMe SSD에는 영향을 주지 않습니다.
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
# Only local nvme device will appear
```