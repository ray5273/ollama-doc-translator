# [ADR] 웹 서비스 네트워크 및 시간 설정 REST API 설계

* 문서 상태: 승인됨 <!-- [제안됨 | 거부됨 | 승인됨 | 폐기됨 | ... | [ADR-0005](0005-example.md)로 대체됨] --> <!-- 선택사항 -->
* 결정권자: 양윤호, 박상혁
* 날짜: 2024/04/25

<!-- [아래에 상황과 문제를 정의합니다, 예를 들면, 자유 형식으로 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
## 상황 및 문제 정의
<!-- [상황과 문제를 아래에 정의합니다, 예를 들어 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
웹 애플리케이션 서버를 적절히 지원하기 위해, 클라우드 환경 서버에서 시스템 네트워크 설정과 시간 설정을 REST API를 통해 관리할 수 있는 기능이 필요합니다.

이러한 구체적인 사항들에 대한 결정이 필요합니다.

### 기본 가정
- ApplicationManager는 컨테이너가 아닌 정적 바이너리로 동작하여 OS 명령어를 직접 실행할 수 있습니다. (static-binary-adr.md)
- Linux는 커널 버전 5.15의 Ubuntu 22.04로 가정합니다.

<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
## 결정 근거
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
<!-- [예시 1, e.g., 성능 및 확장성] -->
<!-- [예시 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
시스템 설정을 수정하는 기능을 추가할 때 다음 우선순위를 따릅니다:
1. Golang에서 지원하는 라이브러리를 활용합니다.
2. Linux 시스템 서비스를 활용하여 구성합니다.
3. 파일을 직접 수정하여 변경사항을 적용합니다.

<!-- [결정된 옵션과 이유를 서술합니다, 이유의 예시 : 유일한 옵션이거나 | 우리의 요구사항을 만족하거나 | 결과가 가장 좋거나 ] -->
## 결정사항
<!-- [선택된 옵션과 이유를 서술합니다, 예시: 유일한 옵션 | 우리의 요구사항을 만족 | 최고의 결과 ] -->
REST API 및 문서 작성에 대한 논의 과정은 다음과 같이 결정되었습니다:

### 네트워크 구성 결정사항
1. 네트워크 설정 구성을 지원하기 위해 `systemd-networkd.service` (netplan)를 사용합니다 (Ubuntu에 사전 설치됨).
   - 버전: 4.2-2ubuntu2
2. 사용자가 GUI의 마지막 페이지에서 네트워크 설정을 구성하도록 안내합니다.

네트워크 구성 사례:
1. REST API 내의 네트워크 설정 API는 두 가지 방법을 지원해야 합니다:
    - IP, DNS, 게이트웨이 등의 수동 할당
    - DHCP를 통한 자동 IP 할당
2. REST API를 통한 네트워크 구성을 위해 단일 엔드포인트를 유지합니다:
   - REST API는 다음 매개변수를 받습니다:
     - PUT /settings/network/ 매개변수:
       - | 매개변수  | 타입, 설명                                           |
         |------------|-------------------------------------------------------------|
         | type       | string (tcp/rdma), 대상 네트워크의 네트워크 타입.     |
         | networkPortSettings | networkPortSettings 배열, 포트별 네트워크 설정 |
         | ntpServers | 문자열 배열, 시스템의 NTP 서버.              |
      - `networkPortSettings` 내의 매개변수:
       - | 매개변수     | 타입, 설명                                                                                                                                                                                             |
         |---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
         | isDhcpEnabled | boolean, 대상 네트워크 포트의 DHCP 상태.                                                                                                                                                          |
         | ip            | string, 대상 네트워크 포트의 IP 주소.                                                                                                                                                           |
         | cidr          | integer, 대상 네트워크 포트의 CIDR.                                                                                                                                                                |
         | gateway        | string, 대상 네트워크 포트의 게이트웨이.                                                                                                                                                               |
         | dnsPrimaryAddress | string, 대상 네트워크 포트의 기본 DNS.                                                                                                                                                           |
         | dnsSecondaryAddress | string, 대상 네트워크 포트의 보조 DNS. 기본 DNS 주소만 있는 경우 생략.                                                                                                        |
         | mtuBytes       | integer(int64), 대상 네트워크 포트의 MTU. (예: 1500, 4200, 9000) 사용별 권장 MTU 크기: 관리 포트는 1500, RDMA 데이터 포트는 4200, TCP 데이터 포트는 9000                                                                                                        |
         | portNum        | integer(int64), 대상 네트워크 포트의 포트 번호. 포트 할당 로직은 웹서비스 펌웨어에서 처리.                                                                                                    |
      
   - DHCP와 고정 IP 설정 간의 상호 배타성을 보장하기 위해 API 요청에 `isDhcpEnabled=true`와 (ip | cidr | gateway | dns) 매개변수를 동시에 포함하는 것을 방지합니다:
     - DHCP 구성: body에 ip, cidr, gateway, dns를 포함하지 않고 `isDhcpEnabled=true`로 API 전송.
     - 고정 IP 구성: body에 ip, cidr, gateway, dns를 포함하고 `isDhcpEnabled=false`로 API 전송.
3. DNS 서버 설정을 최대 2개로 제한합니다.
4. netplan 구성 중에 항상 새로운 `/etc/netplan/99-WebService-custom.yaml` 파일을 생성합니다.
5. `/etc/netplan/` 하위의 모든 구성 파일의 확장자를 "*.config.time.bak"로 변경하여 `/etc/netplan/99-WebService-custom.yaml`만 적용되도록 하여 기존 IP 구성과의 충돌을 방지합니다.
6. "netplan apply" 명령어를 사용하여 네트워크 서버 설정을 적용합니다.

### 시간 구성 결정사항

1. 수동 시간 설정 지원을 위해 `systemd-timedated.service` (`timedatectl`)를 사용합니다.
   - 수동 시간 설정 시 timezone에 입력 가능한 문자열 값은 `timedatectl list-timezones`의 결과와 동일합니다. (검증 코드 미포함)
   - 수동 시간 설정 시 `timedate`에 입력 가능한 문자열 형식은 RFC3339 date-time 형식을 따릅니다 (예: "2021-07-01T00:00:00Z").
2. `timedatectl status` 명령어를 사용하여 NTP 서버가 사용 중인지 확인합니다.
   - `timedatectl set-ntp true` / `timedatectl set-ntp false`를 사용하여 NTP 서버를 활성화/비활성화합니다.
   - `chrony.service`를 사용하여 NTP 서버 설정을 구성합니다.
3. `/etc/chrony/chrony.conf` 파일의 설정을 재정의하여 NTP 구성을 적용합니다.
4. 최대 3개의 NTP 서버 입력을 허용합니다 (근거: Dell BM 결과).
5. REST API를 통한 시간 구성을 위해 단일 엔드포인트를 유지합니다.
   - REST API는 다음 매개변수를 받습니다:
     - PUT /settings/time
     - | 매개변수   | 타입, 설명                                  |
       |-------------|----------------------------------------------------|
       | timezone    | string, 시스템의 시간대.                |
       | timedate    | string \<date-time\>, 시스템의 날짜시간  |
       | ntpServers  | 문자열 배열, 시스템의 NTP 서버. |

     - NTP 구성과 수동 시간 설정 간의 상호 배타성을 유지하기 위해 API 요청에 `ntpServers`와 (`timedate` | `timezone`)를 동시에 포함하는 것을 허용하지 않습니다.
       - NTP 서버 설정 조건: body에 `timezone`과 `timedate`를 포함하지 않고 API 전송.
       - 수동 시간 설정 조건: body에 `ntpServers`를 포함하지 않고 API 전송.

<!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->
## 관련 ADR <!-- 선택사항 -->

* [링크 유형] [ADR 링크 삽입] <!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**
