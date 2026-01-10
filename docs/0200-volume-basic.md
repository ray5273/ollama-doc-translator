# 번역 테스트 : 데이터 볼륨 연습 시나리오
이 문서는 번역 정확도를 검증하기 위해 만든 가상의 데이터 볼륨 관리 가이드입니다. 실제 인프라에 적용하지 마세요.

이 문서는 다음 항목을 다룹니다.
1. [가상 Volume Store](#가상-volume-store)
2. [샌드박스 Volume](#샌드박스-volume)
3. [NVMe-oF 노출](#nvme-of-노출)

## 가상 Volume Store
훈련용 `LVS`는 실습 SSD나 이미 존재하는 LVol 위에 구성할 수 있습니다. 아래 예시는 `atlas9472n1` 장치를 사용합니다.

### 1. 생성
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{
  "alias": "atlas9472n1",
  "lvs_name": "training_store",
  "cluster_sz": 1048576,
  "clear_method": "none"
}' \
'https://<IP_ADDRESS>/api/v1/training/lvstore'
```

| 필드 | 설명 |
|------|------|
| `alias` | 기반 디바이스 이름 |
| `lvs_name` | 생성될 LVS 이름 |
| `cluster_sz` | 클러스터 크기 |
| `clear_method` | 공간 초기화 방식 |

### 2. 조회
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
'https://<IP_ADDRESS>/api/v1/training/lvstore'
```

### 3. 삭제
```bash
$ curl -k -X DELETE \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store"}' \
'https://<IP_ADDRESS>/api/v1/training/lvstore'
```

## 샌드박스 Volume
### 1. 생성
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{
  "alias": "training_store",
  "lvol_name": "demo_lvol",
  "size_in_mib": 51200,
  "thin_provision": true
}' \
'https://<IP_ADDRESS>/api/v1/training/lvol'
```

### 2. 조회
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
'https://<IP_ADDRESS>/api/v1/training/lvol'
```

### 3. 삭제
```bash
$ curl -k -X DELETE \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol'
```

## NVMe-oF 노출
### 1. attach 요청
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
```

### 2. 상태 확인
```bash
$ curl -k -X GET \
-u <USERNAME>:<PASSWORD> \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
```

### 3. 해제
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol", "action": "detach"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
```

## 참고 표
| 항목 | 값 |
|------|-----|
| 교육용 계정 | `trainee` |
| API 엔드포인트 | `https://<IP_ADDRESS>/api/v1/training/*` |
| 기본 컨텍스트 길이 | 32 MiB |
