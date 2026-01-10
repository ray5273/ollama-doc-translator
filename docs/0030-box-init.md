# 번역 테스트 : 가상 박스 초기화 절차
이 문서는 QA 팀이 번역 품질을 점검하기 위해 만든 허구의 박스 초기화 시나리오를 설명합니다.

## 1. 초기 점검
- 실습 장비 이름: `orion-mini`
- 관리 IP: `172.30.11.20`
- 상태 조회 명령:
```bash
$ curl -k https://172.30.11.20/api/v1/lab/status
```

## 2. 준비 단계
| 단계 | 설명 |
|------|------|
| 1 | 테스트 이미지 검증 |
| 2 | 구성 백업 |
| 3 | 로그 디렉토리 정리 |

## 3. 초기화 명령
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"mode": "training", "resetLogs": true}' \
'https://172.30.11.20/api/v1/lab/init'
```

## 4. 진행 상황 추적
- `watch -n2 "curl -ks https://172.30.11.20/api/v1/lab/progress"`
- `journalctl -u lab-reset -f`

## 5. 완료 검증
초기화가 끝나면 아래 항목을 확인합니다.
1. `/var/log/lab-reset` 내부에 새 세션 폴더가 생성되었는가?
2. `systemctl status lab-core`가 `active (running)` 상태인가?
3. REST 응답의 `phase` 값이 `READY`인지 확인합니다.

## 6. 후속 작업
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"command": "seed-data"}' \
'https://172.30.11.20/api/v1/lab/tasks'
```

## 7. 보고서 작성
- 실습자는 `docs/reports/box-init-template.md` 파일에 결과를 기록합니다.
- 문제 발생 시 `lab-support@example.com`으로 로그를 첨부해 문의합니다.
