# 번역 테스트 : NVMe-oF 연결 연습
이 문서는 번역 품질을 검증하기 위해 구성된 가상의 NVMe-oF 연결 시나리오입니다. 실습 대상은 `orion-target` 이니시에이터입니다.

## 1. 환경 요약
| 구분 | 정보 |
|------|------|
| 타깃 NQN | `nqn.2024-01.test.orion` |
| 관리 IP | `172.40.1.5` |
| 데이터 포트 | `192.168.90.10` |
| 프로토콜 | TCP |

## 2. 사전 점검
1. `nvme list-subsys` 명령으로 기존 연결을 확인합니다.
2. `/etc/nvme/hostnqn` 파일이 최신인지 확인합니다.
3. 방화벽에서 4420 포트가 열려 있는지 검증합니다.

## 3. 연결 명령
```bash
$ sudo nvme connect \
-t tcp \
-n nqn.2024-01.test.orion \
-a 192.168.90.10 \
-s 4420
```

## 4. 상태 확인
```bash
$ sudo nvme list
$ sudo nvme netapp ontapdevices -o json
```

## 5. 세션 해제
```bash
$ sudo nvme disconnect -n nqn.2024-01.test.orion
```

## 6. 문제 해결
- **연결 실패**: `dmesg | tail` 로 커널 로그를 확인하고, 필요 시 `sudo nvme connect` 명령에 `-l 3600` 옵션을 추가하여 타임아웃을 늘립니다.
- **성능 저하**: `sudo nvme smart-log /dev/nvme1n1` 명령으로 지연 시간 및 에러 카운터를 확인합니다.
- **보안 정책**: 테스트 타깃은 self-signed 인증서를 사용하므로 TLS 연결이 필요한 경우 `--tls` 플래그와 인증서 경로를 명시해야 합니다.
