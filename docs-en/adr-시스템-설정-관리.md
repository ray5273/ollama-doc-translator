<!-- [아래에 상황과 문제를 정의합니다, 예를 들면, 자유 형식으로 2~3 문단으로 간결하게 설명하면 좋습니다.]-->
<!-- 선택사항 -->
<!-- [제안됨 | 거부됨 | 승인됨 | 폐기됨 | … | [ADR-0005](0005-example.md)로 대체됨] -->
# [ADR] System Configuration Management Design and Implementation Decisions

- Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
- Decision Makers: Kim Minho, Lee Jiyeong, Park Dong-hwan, Choi Min-jung, Jeong Kyung-ho, Nam Seon-seo, Im Jae-won, Kang Hyun-jin, Seo Min-seok, Oh Yu-jin, Baek Tae-hoon
- Date: 2024-12-17

<!-- Define the situation and problem below, for example, concisely in 2-3 paragraphs as needed. -->

<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [상황과 문제를 아래에 정의합니다, 예를 들어 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
## Situation and Problem Definition
<!-- [Define the situation and problem below, for example, concisely in 2~3 sentences.] -->
- Currently, when the `ConfigurationManager` starts, system settings (including parameters) are loaded from a static configuration file, and there is a requirement that these settings, particularly database connection settings or cache management, should be dynamically adjusted through REST APIs within the WebService without going through `ConfigurationManager` during the `SystemSetup` initialization process. This issue needs to be addressed.

<!-- [Supporting Reason 2, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Supporting Reason 1, e.g., performance and scalability] -->
<!-- The basis for decision-making may vary with each decision -->

<!-- [결정된 옵션과 이유를 서술합니다, 이유의 예시 : 유일한 옵션이거나 | 우리의 요구사항을 만족하거나 | 결과가 가장 좋거나 ] -->
<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
## Decision Rationale
<!-- Decision rationale can vary for each decision made -->
<!-- [Example Reason 1, e.g., Performance and Scalability] -->
<!-- [Example Reason 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->

- Enable direct control over database configuration without passing through ConfigurationManager, allowing direct control from WebService.
- Previously, database connections were managed through Connection Pool, but with Database Driver usage, endpoints for connection management at the application level are available, thus eliminating the necessity to always go through Connection Pool or ConfigurationManager for control.

<!-- Describe the chosen option and its rationale: e.g., unique option | meets our requirements | yields the best results -->

<!-- [결정으로 인해 좋아지는 점과 나빠지는 점] -->
<!-- [예: 러닝 커브 필요, 마이그레이션 필요함] -->
<!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->
<!-- [선택된 옵션과 이유를 서술합니다, 예시 : 유일한 옵션 | 우리의 요구사항을 만족 | 최고의 결과 ] -->
## Decisions
<!-- [Describe the selected option and reason, e.g.: Unique option | Meets our requirements | Best outcome ] -->

### Practical Configuration Commands for Database Delivery
- Previously, `sql command` was used to deliver commands to each database connection exposed at the application layer through `database_wrapper` within the WebService. Relevant configuration command information within the database specs is as follows. (Original: https://www.postgresql.org/docs/current/config-setting.html)

### Usability-Related Options
- To enhance user management convenience, options are provided at a simplified level compared to the database spec configuration commands, categorized into two forms:

  | Control Type | Name | Description | Notes |
  | ------------ | ---- | ----------- | ----- |
  | PerformanceMode | HighThroughput | Throughput-centric | Up to 1000 connections |
  |             | Balanced | Balanced performance and resource usage | Up to 500 connections |
  |             | ResourceSaver | Minimize resource consumption | Up to 100 connections |
  |             | Manual | Custom connection state | - |
  | ConnectionState | Specific Connection State | Custom setting activated when PerformanceMode is selected | - |
  
- Supported connection states per database model

  | Model | Type | NPSS | Connection State | Notes |
  | ----- | ---- | ---- | --------------- | ----- |
  | PostgreSQL | RDBMS | 4 | 0 | max_connections:1000 timeout:30s pooling:enabled cache_size:1GB shared_buffers:256MB work_mem:4MB |
  |       |      |      | 1 | max_connections:750 timeout:45s pooling:enabled cache_size:512MB shared_buffers:192MB work_mem:4MB |
  |       |      |      | 2 | max_connections:500 timeout:60s pooling:enabled cache_size:256MB shared_buffers:128MB work_mem:2MB |
  |       |      |      | 3 | max_connections:250 timeout:90s pooling:enabled cache_size:128MB shared_buffers:64MB work_mem:2MB |
  |       |      |      | 4 | max_connections:100 timeout:120s pooling:enabled cache_size:64MB shared_buffers:32MB work_mem:1MB |
  | MySQL | RDBMS | 3 | 0 | max_connections:1000 timeout:28s pooling:enabled cache_size:512MB innodb_buffer_pool_size:256MB |
  |       |      |      | 1 | max_connections:750 timeout:40s pooling:enabled cache_size:384MB innodb_buffer_pool_size:192MB |
  |       |      |      | 2 | max_connections:500 timeout:55s pooling:enabled cache_size:256MB innodb_buffer_pool_size:128MB |
  |       |      |      | 3 | max_connections:250 timeout:80s pooling:enabled cache_size:128MB innodb_buffer_pool_size:64MB |
  | Redis | NoSQL | 0 | 0 | maxclients:10000 timeout:0 maxmemory:2GB save:900 1 |
  | NPSS: Supported Performance Levels (Indexing starts from 0) | - | - | - |

<!-- Example: Improved by ADR-0005 (0005-example.md) -->
<!-- [e.g.: Requires learning curve, migration needed] -->
<!-- [Positive and negative impacts of the decision] -->

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

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**