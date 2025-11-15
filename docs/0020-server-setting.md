# 번역 테스트 : 실험용 네트워크 구성 가이드
이 문서는 실습 랩에서 사용되는 가상 장비 `Nebula Node`의 네트워크 인터페이스를 설정하는 과정을 설명합니다. 실제 장비에는 적용하지 마세요.

이 시나리오에서 가정하는 환경은 다음과 같습니다.
- 목표: 교육용 컨트롤 노드에서 관리 인터페이스를 통해 고속 데이터 포트에 정적 IP를 부여
- 환경:
  - `nebula-orchestrator` 서비스가 실행 중이며, 관리 인터페이스는 `172.20.0.8` 주소로 접근 가능
  - 데이터 포트는 아직 IP가 없는 상태이며, RDMA 테스트를 위해 수동 설정이 필요

> **실습 메모**
> - `sudo` 권한이 필요한 명령은 환경에 맞게 조정하세요.
> - REST 호출은 self-signed 인증서를 가정하여 항상 `-k` 플래그를 사용합니다.

## 1. DHCP 주소 찾기
### 1.1 mDNS 탐색
```bash
$ avahi-browse -alr | grep nebula
```

### 1.2 ARP 테이블 확인
```bash
$ arp -a | grep nebula
```

## 2. 현재 네트워크 상태 조회
### 2.1 REST 요청 예시
```bash
$ curl -k -X GET \
-u 'trainer:trainer' \
-H 'Accept: application/json' \
'https://172.20.0.8/api/v1/training/network'
```

### 2.2 예상 응답
```bash
{
  "ports": [
    {"portNum": 1, "displayName": "Intel X710", "ip": "172.20.0.8"},
    {"portNum": 3, "displayName": "Mellanox CX6", "ip": null}
  ],
  "message": "training snapshot"
}
```

## 3. 네트워크 설정 적용
### 3.1 요청 본문 구조
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `type` | `string` | 사용 프로토콜 (`tcp`, `rdma`) |
| `networkPortSettings` | `array` | 포트별 구성 목록 |
| `portNum` | `int` | 대상 포트 번호 |
| `ip` | `string` | 설정할 IP |
| `cidr` | `int` | 서브넷 |
| `gateway` | `string` | 게이트웨이 |

### 3.2 명령어 예시
```bash
$ curl -k -X PUT \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{
  "type": "rdma",
  "networkPortSettings": [
    {
      "portNum": 3,
      "ip": "192.168.40.10",
      "cidr": 24,
      "gateway": "192.168.40.1",
      "dnsPrimaryAddress": "1.1.1.1",
      "dnsSecondaryAddress": "8.8.8.8",
      "isDhcpEnabled": false
    }
  ]
}' \
'https://172.20.0.8/api/v1/training/network'
```

## 4. 결과 검증
1. `curl -k -X GET ...`으로 다시 조회하여 `portNum` 3에 IP가 적용되었는지 확인합니다.
2. `ping 192.168.40.1 -c 2` 명령으로 게이트웨이 도달 여부를 테스트합니다.
3. `rdma-statistic collect` 명령으로 패브릭 대기 시간을 기록합니다.

## 5. 문제 해결 시나리오
- **응답 지연**: REST 호출이 5초 이상 지연되면 `journalctl -u nebula-orchestrator` 로그를 확인합니다.
- **MTU 불일치**: 실험 네트워크는 `mtuBytes 9000`을 요구하므로, 필요한 경우 PUT 요청에 해당 필드를 추가합니다.
- **잘못된 인증 정보**: `401` 응답이 발생하면 새로 발급된 실습 계정으로 재시도합니다.
