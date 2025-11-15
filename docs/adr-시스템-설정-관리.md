# [ADR] 시스템 설정 관리 설계 및 구현 결정사항

- 문서 상태: 승인됨 <!-- [제안됨 | 거부됨 | 승인됨 | 폐기됨 | … | [ADR-0005](0005-example.md)로 대체됨] --> <!-- 선택사항 -->
- 결정권자: 김민호, 이지영, 박동환, 최소정, 정경호, 남은서, 임재원, 강현진, 서민석, 오유진, 백태훈
- 날짜: 2024-12-17

<!-- [아래에 상황과 문제를 정의합니다, 예를 들면, 자유 형식으로 2~3 문단으로 간결하게 설명하면 좋습니다.]-->
## 상황 및 문제 정의
<!-- [상황과 문제를 아래에 정의합니다, 예를 들어 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
- 현재 ConfigurationManager가 시작될 때 시스템 설정(매개변수 포함)이 정적 구성 파일에서 로드되고, SystemSetup 초기화 과정에서 이러한 구성, 특히 데이터베이스 연결 설정이나 캐시 관리와 관련하여 ConfigurationManager를 거치지 않고 WebService 내에서 REST API를 통해 동적으로 조정 가능해야 하는 요구사항이 있어 이를 해결해야 합니다.

<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
## 결정 근거
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->

- ConfigurationManager를 거치지 않고 데이터베이스 구성을 직접 제어할 수 있도록 하여 WebService에서 직접 제어가 가능하게 합니다.
- 이전에는 데이터베이스 연결이 Connection Pool을 통해 관리되었지만, Database Driver 사용 시에도 애플리케이션 레벨에서 연결 관리를 위한 엔드포인트가 사용 가능하므로 Connection Pool이나 ConfigurationManager를 반드시 거치지 않고도 제어가 가능합니다.

<!-- [결정된 옵션과 이유를 서술합니다, 이유의 예시 : 유일한 옵션이거나 | 우리의 요구사항을 만족하거나 | 결과가 가장 좋거나 ] -->
## 결정사항
<!-- [선택된 옵션과 이유를 서술합니다, 예시 : 유일한 옵션 | 우리의 요구사항을 만족 | 최고의 결과 ] -->

### 데이터베이스 전달을 위한 실용적인 구성 명령 세트
- 이전에는 WebService 내 `database_wrapper`를 통해 애플리케이션 레이어에 노출된 각 데이터베이스 연결로 명령을 전달하기 위해 `sql command`를 사용했습니다. 데이터베이스 스펙 내 구성 명령에 관한 관련 정보는 다음과 같습니다. (원본: https://www.postgresql.org/docs/current/config-setting.html)

### 사용성 관련 옵션
- 사용자 관리의 편의를 위해 데이터베이스 스펙 구성 명령 레벨에 비해 단순화된 레벨에서 옵션을 제공하며, 두 가지 형태로 구분됩니다:

  | 제어 유형 | 이름 | 설명 | 비고 |
  | -------- | ---- | ---- | ---- |
  | PerformanceMode | HighThroughput | 처리량 중심 | 최대 1000개 연결 |
  |  | Balanced | 성능과 리소스 사용량의 균형 | 최대 500개 연결 |
  |  | ResourceSaver | 리소스 소비 최소화 | 최대 100개 연결 |
  |  | Manual | 사용자 정의 연결 상태 | - |
  | ConnectionState | 특정 연결 상태 | 제어 유형이 PerformanceMode일 때 활성화되는 사용자 정의 설정 | - |
  
- 데이터베이스 모델별 지원되는 연결 상태

  | 모델 | 유형 | NPSS | 연결 상태 | 비고 |
  | ---- | ---- | ---- | ------- | ---- |
  | PostgreSQL | RDBMS | 4 | 0 | max_connections:1000 timeout:30s pooling:enabled cache_size:1GB shared_buffers:256MB work_mem:4MB |
  |  |  |  | 1 | max_connections:750 timeout:45s pooling:enabled cache_size:512MB shared_buffers:192MB work_mem:4MB |
  |  |  |  | 2 | max_connections:500 timeout:60s pooling:enabled cache_size:256MB shared_buffers:128MB work_mem:2MB |
  |  |  |  | 3 | max_connections:250 timeout:90s pooling:enabled cache_size:128MB shared_buffers:64MB work_mem:2MB |
  |  |  |  | 4 | max_connections:100 timeout:120s pooling:enabled cache_size:64MB shared_buffers:32MB work_mem:1MB |
  | MySQL | RDBMS | 3 | 0 | max_connections:1000 timeout:28s pooling:enabled cache_size:512MB innodb_buffer_pool_size:256MB |
  |  |  |  | 1 | max_connections:750 timeout:40s pooling:enabled cache_size:384MB innodb_buffer_pool_size:192MB |
  |  |  |  | 2 | max_connections:500 timeout:55s pooling:enabled cache_size:256MB innodb_buffer_pool_size:128MB |
  |  |  |  | 3 | max_connections:250 timeout:80s pooling:enabled cache_size:128MB innodb_buffer_pool_size:64MB |
  | Redis | NoSQL | 0 | 0 | maxclients:10000 timeout:0 maxmemory:2GB save:900 1 |
  - NPSS: 지원되는 성능 상태 수 (0부터 시작하는 인덱싱)

<!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->
<!-- [예: 러닝 커브 필요, 마이그레이션 필요함] -->
<!-- [결정으로 인해 좋아지는 점과 나빠지는 점] -->
### REST API 엔드포인트
- `/system/performance-mode`
  - 시스템 레벨에서 성능 모드를 구성하고 모든 데이터베이스 연결을 통합적으로 관리합니다.
  - get
    - 현재 시스템 레벨 성능 모드를 표시합니다.
    - 시스템 레벨에서 데이터베이스들의 총 집계된 연결 사용량을 제공합니다.
  - put
    - 시스템 레벨 성능 모드를 설정합니다.
- `/databases/{instanceId}/connection-state`
  - get
    - instanceId로 식별되는 특정 데이터베이스의 현재 연결 상태를 조회하고 알려줍니다.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "데이터베이스 연결 상태가 성공적으로 조회되었습니다."
      }
      $
      ```
  - put
    - instanceId로 식별되는 특정 데이터베이스의 성능 모드를 지정된 연결 상태로 설정합니다.
    - ```bash
      $ curl -k -X PUT https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} \
      -H "Content-Type: application/json" \
      -d '{ "state": 1 }' | jq
      {
        "currentConnectionState": 1,
        "message": "데이터베이스 성능 모드가 성공적으로 업데이트되었습니다."
      }
      $
      ```
- `/databases/{instanceId}/connection-state/detail`
  - get
    - instanceId로 식별되는 특정 데이터베이스의 연결 상태 세부 정보를 제공합니다.
    - 현재 연결 상태, 데이터베이스가 지원하는 연결 상태 등.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "데이터베이스 성능 모드가 성공적으로 조회되었습니다.",
        "connectionStatesSupported": [
            {
              "maxConnections": 1000,
              "timeout_s": 30,
              "cacheSize_MB": 1024,
              "poolingEnabled": true,
              "connectionStateID": 0
            },
            {
              "maxConnections": 750,
              "timeout_s": 45,
              "cacheSize_MB": 512,
              "poolingEnabled": true,
              "connectionStateID": 1
            },
            {
              "maxConnections": 500,
              "timeout_s": 60,
              "cacheSize_MB": 256,
              "poolingEnabled": true,
              "connectionStateID": 2
            },
            {
              "maxConnections": 250,
              "timeout_s": 90,
              "cacheSize_MB": 128,
              "poolingEnabled": true,
              "connectionStateID": 3
            },
            {
              "maxConnections": 100,
              "timeout_s": 120,
              "cacheSize_MB": 64,
              "poolingEnabled": true,
              "connectionStateID": 4
            }
        ]
      }
      $
      ```

### 예외 처리
- 데이터베이스가 성능 모드를 지원하지 않는 경우
  - 일반적으로 특정 데이터베이스가 성능 모드를 지원하는지 여부는 구성 명령(Config Parameter #max_connections, States 0 ~ 31, 총 최대 32개 상태)을 통해 판단할 수 있습니다. 요청이 지원되는 연결 상태를 초과하는 경우 가능한 가장 가까운 값으로 설정합니다.
- 데이터베이스가 성능 모드를 지원하지만 잘못된 매개변수가 제공된 경우
  - 가능한 가장 가까운 값으로 설정합니다.
- 데이터베이스의 Hot Swap 이벤트 시 현재 성능 모드 상황을 확인하고 필요한 경우 구성에 맞게 조정을 적용합니다.
  - Connect/Disconnect 작업 중에 총 연결 사용량이 변경될 수 있습니다.
  - 이러한 변경사항에 대해 시스템 레벨 성능 관리와 관련된 데이터베이스 동기화 및 업데이트가 필요합니다.

### 결과 <!-- 선택사항 -->
<!-- [결정의 긍정적 측면과 단점] -->
<!-- [예: 러닝 커브 필요, 마이그레이션 필요] -->
- [결정 근거](#결정-근거)에서 언급한 바와 같이, WebService가 데이터베이스 연결 상태를 **직접적으로** **동적 제어**할 수 있습니다.

## 관련 ADR <!-- 선택사항 -->

- [링크 유형] [ADR 링크 삽입] <!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**
