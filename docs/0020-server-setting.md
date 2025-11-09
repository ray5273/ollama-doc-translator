
# PBSSD Network Setting (Before Box Initialization)
네트워크 설정(network setting)은 PBSSD 내부에서 초기화할 수도 있지만, 이 문서에서는 NVMe-oF 이니시에이터(initiator)에서 PBSSD의 네트워크 인터페이스를 설정 및 관리하는 절차에 대해 안내합니다.

네트워크 설정은 박스 초기화(box initialization) 이전 단계에서만 수행하는 것을 권장합니다.

이 문서에서는 다음과 같은 목표와 환경을 가정합니다.
- 목표: 이니시에이터에서 1Gbps 관리 인터페이스를 통해 PBSSD의 100Gbps NVMe-oF 인터페이스에 정적 IP 주소를 수동으로 설정
- 환경:
  - PBSSD에 펌웨어가 정상 설치되었으며, orc_run 서비스가 실행 중
  - PBSSD는 1Gbps 관리 인터페이스를 통해 DHCP를 사용하여 IP 주소 10.1.3.8를 할당받았으며, 이니시에이터와 안정적으로 통신 가능한 상태
  - PBSSD의 100Gbps NVMe-oF 인터페이스는 현재 IP 주소가 할당되지 않은 상태이며, 수동 설정 필요

> **사용 예시 참고:**
> - 환경에 따라 일부 명령은 `sudo` 권한이 필요할 수 있습니다.
> - REST API 요청
>   - 관리자 계정으로 `admin:admin`을 사용한다고 가정합니다.
>   - self-signed 인증서를 사용한다고 가정하여, `curl` 명령에 `-k` 옵션을 포함하여 명령어를 작성하였습니다.

## Finding DHCP IP
아래 명령어를 사용하여 DHCP를 통해 자동 할당된 IP 주소를 확인할 수 있습니다. 명령어 실행 결과를 통해 타깃 PBSSD의 IP 주소가 `10.1.3.8`임을 확인할 수 있습니다. _(참고: 호스트명은 장치마다 다를 수 있습니다.)_

**1. mDNS 탐색**  
`avahi-browse -alr` 명령어를 사용하면, 로컬 네트워크에서 mDNS(Multicast DNS)를 통해 브로드캐스트되는 장비의 호스트 이름, IP 주소, 서비스 정보를 확인할 수 있습니다.
```bash
$ apt install avahi-utils
$ avahi-browse -alr
```
```bash
...
= ens17f0np0 IPv6 spdk0_10.1.3.8_1153    _nvme-disc._tcp    local
   hostname = [pbssd.local]
   address = [10.1.3.8]
   port = [1153]
   txt = ["nqn=nqn.2014-08.org.nvmexpress.discovery" "p=tcp"]
...
```

**2. IP ↔ MAC 매핑 확인**  
이니시에이터가 해당 장비와 직접 통신한 이력이 있다면, `arp -a` 명령어를 통해 로컬 ARP 테이블에 저장된 IP 주소 ↔ MAC 주소 매핑 정보를 확인할 수 있습니다.
```bash
$ arp -a
```
```bash
... 
pbssd.local (10.1.3.8) at 7c:c2:55:9f:fd:d0 [ether] on enp9s0f0
...
```

## PBSSD Firmware Network Check
100Gbps 네트워크 인터페이스가 IP 주소를 할당받지 않은 상황을 가정하므로, 1Gbps 관리 포트를 통해 REST API 요청을 발행하여 타깃 PBSSD의 네트워크 설정 정보를 확인합니다.REST API 응답을 통해 100Gbps 네트워크 인터페이스의 `portNum` 값을 확인합니다.

**1. 명령어**  
REST API의 `GET /settings/network` 엔드포인트를 호출하여 네트워크 정보를 확인합니다.
```bash
$ curl -X GET \
-u '<USERNAME>:<PASSWORD>' \
-H 'Accept: application/json'\
'https://<IP_ADDRESS>/api/v1/settings/network'
```

**2. 명령어 사용 예시**  
아래 예시에서 `"portNum": 2`는 100Gbps 네트워크 인터페이스가 위치한 포트 번호입니다.
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
      "cidr": 64,
      "ip": "fe80::7ec2:54ef:ff43:ae80",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 2,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
    },
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
    }
    ...
  ]
}
```

## Network Setting
박스 초기화(Box Initialization)를 수행하기 전에 네트워크 설정(Network Setting)이 필요합니다. `3. 명령어 사용 예시` 섹션을 참조하여, 100Gbps 네트워크 인터페이스에 정적 IP 주소를 수동으로 설정할 수 있습니다.

**1. 명령어**  
REST API의 `PUT /settings/network` 엔드포인트를 호출하여 타깃 PBSSD의 네트워크를 설정합니다. REST API를 통해 네트워크 설정을 요청할 때, `type` 필드가 지정되면 타깃 PBSSD의 `pos-essential-ioworker` 서비스가 자동으로 실행됩니다. DHCP 서버가 존재하지 않는 네트워크 환경이거나, PBSSD에 정적 IP 주소를 고정 사용할 경우, networkPortSettings 객체를 포함하여 `PUT /settings/network` 요청을 발행하여 IP 주소, DHCP 설정, DNS, 게이트웨이 등을 명시적으로 구성해야 합니다.
> 이 API는 관리자 권한이 있는 계정으로만 호출할 수 있습니다.
```bash
$ curl -X PUT \
-u '<USERNAME>:<PASSWORD>' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "type": "{network protocol}",
  "networkPortSettings": [
    {
      "isDhcpEnabled": <IS_DHCP>,
      "ip": "<IP_ADDRESS>",
      "cidr": <CIDR>,
      "gateway": "<GATEWAY_IP>",
      "dnsPrimaryAddress": "<PRIMARY_DNS_IP>",
      "dnsSecondaryAddress": "<SECONDARY_DNS_IP>",
      "mtuBytes": <MTU_BYTES>,
      "portNum": <PORT>
    }
  ]
}' \
'https://{IP_ADDRESS}/api/v1/settings/network'
```
아래는 요청 본문의 필드에 대한 설명입니다.

| 필드명                  | 타입              | 필수 여부 | 설명                                              |
|-----------------------|------------------|---------|--------------------------------------------------|
| `type`                | `string`         | 필수     | 네트워크 전송 프로토콜 (예: `TCP`, `RDMA`)             |
| `networkPortSettings` | `array`          | 선택     | 네트워크 포트 설정 목록                               |
| `isDhcpEnabled`       | `boolean`        | 필수     | DHCP 활성화 여부 (`true`: 자동 할당, `false`: 정적 IP) |
| `ip`                  | `string`         | 선택     | 정적 IP 주소 (예: `192.168.1.100`)                  |
| `cidr`                | `int`            | 선택     | 서브넷 마스크 길이 (예: `24`)                         |
| `gateway`             | `string`         | 선택     | 게이트웨이 주소 (예: `192.168.1.1`)                   |
| `dnsPrimaryAddress`   | `string`         | 선택     | 기본 DNS 서버 (예: `8.8.8.8`)                       |
| `dnsSecondaryAddress` | `string`         | 선택     | 보조 DNS 서버 (예: `8.8.4.4`)                       |
| `mtuBytes`            | `int`            | 선택     | MTU 크기 (기본값 `1500`)                            |
| `portNum`             | `int`            | 필수     | 네트워크 포트 번호 (예: `1`, `2`)                     |


**2. 명령어 사용 예시 : 네트워크 프로토콜 변경 & 변경내용 확인**  
타깃 PBSSD(`10.1.3.8`)에 연결된 네트워크를 `"type": "tcp"`로 변경하는 REST API 요청입니다.
```bash
$ curl -k -X PUT \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{ "type": "tcp"}' \
'https://10.1.3.8:443/api/v1/settings/network'
```
```bash
{"message":"API server successfully set the network settings","relatedJobs":null}
```
변경 결과 확인을 위해 네트워크 정보를 조회합니다.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json'
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
      "cidr": 64,
      "ip": "fe80::7ec2:54ef:ff43:ae80",
      "isDhcpEnabled": false,
      "mtuBytes": 1500,
      "portNum": 2,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
      "type": "tcp"
    },
    ...
  ]
}
```
**3. 명령어 사용 예시 : 네트워크 프로토콜 변경 및 단일 포트(portnum 2)의 네트워크 설정 변경 & 변경내용 확인**  
타깃 PBSSD(`10.1.3.8`)에 연결된 네트워크를 `"type": "tcp"`로 변경하고, `"portNum": 2`의 네트워크 정보를 수정하는 REST API 요청입니다. 이 문서의 목표인 100Gbps 네트워크 인터페이스의 네트워크를 설정하기 위해서 아래 명령어를 참고하여 사용하면 됩니다.
```bash
$ curl -k -X PUT \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{ "type": "tcp", "networkPortSettings": [{"isDhcpEnabled": false,"ip":"10.100.3.8", "cidr": 16, "gateway": "10.1.5.22", "dnsPrimaryAddress": "10.1.1.13", "dnsSecondaryAddress": "12.26.3.228", "mtuBytes": 9000, "portNum": 2}]}' \
'https://10.1.3.8:443/api/v1/settings/network'
```
```bash
{"message":"API server successfully set the network settings","relatedJobs":null}
```
변경 결과 확인을 위해 네트워크 정보를 조회합니다.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json'
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
**4. 명령어 사용 예시 : 네트워크 프로토콜 변경 및 여러 포트(portnum: 2, 3)의 네트워크 설정 변경 & 변경내용 확인**  
아래 예시는 타깃 PBSSD(`10.1.3.8`)에 연결된 네트워크를 `"type": "tcp"`로 변경하고, 동시에 여러 포트(`"portNum": 2`와`3`)의 네트워크 정보를 동시에 수정하는 REST API 요청입니다.
```bash
$ curl -k -X PUT \
-u 'admin:admin' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{ "type": "tcp", "networkPortSettings": [{"isDhcpEnabled": false,"ip":"10.100.3.8", "cidr": 16, "gateway": "10.1.5.22", "dnsPrimaryAddress": "10.1.1.13", "dnsSecondaryAddress": "12.26.3.228", "mtuBytes": 9000, "portNum": 2},{"isDhcpEnabled": false,"ip":"10.100.3.9", "cidr": 16, "gateway": "10.1.5.22", "dnsPrimaryAddress": "10.1.1.13", "dnsSecondaryAddress": "12.26.3.228", "mtuBytes": 9000, "portNum": 2}]}'\
'https://10.1.3.8:443/api/v1/settings/network'
```
```bash
{"message":"API server successfully set the network settings","relatedJobs":null}
```
변경 결과 확인을 위해 네트워크 정보를 조회합니다.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json'
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
    {
      "cidr": 16,
      "dnsPrimaryAddress": "10.1.1.13",
      "dnsSecondaryAddress": "12.26.3.228",
      "ip": "10.100.3.9",
      "isDhcpEnabled": false,
      "mtuBytes": 9000,
      "portNum": 3,
      "displayName": "Mellanox Technologies MT2892 Family [ConnectX-6 Dx]",
      "health": "UP",
      "type": "tcp"
    },
    ...
  ]
}
```