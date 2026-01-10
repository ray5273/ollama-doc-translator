# 번역 테스트 : 마이크로서비스 배포 리허설
이 문서는 사내 교육용으로 사용되는 번역 테스트 문서입니다. 실제 제품과 무관하며, 다양한 문체와 기술 용어가 섞여 있는 상황을 의도적으로 구성했습니다.

이 시나리오에서는 다음 목표와 환경을 가정합니다.
- 목표: 훈련용 마이크로서비스 묶음을 시뮬레이션 서버에 배포하고 동작을 관찰
- 환경: `orion-stack` 이미지가 로컬 레지스트리에 존재하며, 학습용 컨트롤 노드가 `192.168.10.77` 주소로 접근 가능

> **연습 노트**
> - 안내된 명령은 예시이며 `sudo` 여부나 경로를 팀 환경에 맞춰 수정하세요.
> - 모든 REST 호출은 self-signed 인증서를 사용하는 상황을 가정하여 `-k` 옵션을 포함합니다.

## 1. 준비 체크리스트
배포 리허설을 시작하기 전에 다음 항목을 확인합니다.

1. 이미지 버전과 해시를 기록합니다.
2. 셸에서 테스트용 가상 환경을 활성화합니다.
3. 로그 수집 디렉토리를 비우고 새 세션을 준비합니다.

```bash
$ source ~/virtualenvs/deploy-lab/bin/activate
$ docker images | grep orion-stack
$ rm -rf ~/lab-logs/*
```

## 2. 샌드박스 상태 진단
서비스를 기동하기 전에 컨테이너, 서비스, 스토리지 상태를 점검합니다.

### 2.1 서비스 상태
```bash
$ systemctl status lab-agent
$ systemctl status lab-api
```

### 2.2 컨테이너 목록
```bash
$ docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

### 2.3 스토리지 요약
```bash
$ df -h /var/lib/orion
```

## 3. 배포 시나리오 실행
1. 아티팩트를 업로드하고 서명값을 확인합니다.
2. REST API를 이용해 `lab-api`에서 구성 변경을 등록합니다.
3. `lab-agent` 서비스에서 실제 컨테이너를 기동합니다.

```bash
$ curl -k -X POST \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{"stage": "upload", "bundle": "orion-stack:training"}' \
'https://192.168.10.77/api/v1/lab/deploy'
```

배포 진행 중에는 `journalctl -u lab-agent -f` 명령으로 메시지를 수집하고, 특정 오류 코드가 발생하면 즉시 실습 노트에 기록합니다.

## 4. 상태 관찰 및 로그 수집
다음 표는 학습자들이 기록해야 하는 핵심 상태 항목 예시입니다.

| 구분 | 확인 명령 | 기대 값 |
|------|-----------|---------|
| 서비스 응답 | `curl -k https://192.168.10.77/healthz` | `{"status":"ok"}` |
| 컨테이너 수 | `docker ps -q | wc -l` | 6 |
| CPU 점유율 | `mpstat 1 1` | 75% 이하 |

## 5. 종료 및 복구
연습이 끝나면 아래 절차로 리소스를 정리합니다.

```bash
$ systemctl stop lab-api
$ systemctl stop lab-agent
$ docker system prune -f
```

종료 로그는 `~/lab-logs/shutdown-$(date +%Y%m%d).log` 파일에 저장하고, 다음 실습을 위해 결과 요약을 팀 채널에 공유합니다.
