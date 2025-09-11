<!-- [아래에 상황과 문제를 정의합니다, 예를 들면, 자유 형식으로 2~3 문단으로 간결하게 설명하면 좋습니다.]-->
<!-- 선택사항 -->
<!-- [제안됨 | 거부됨 | 승인됨 | 폐기됨 | … | [ADR-0005](0005-example.md)로 대체됨] -->
# [ADR] System Configuration Management Design and Implementation Decision Points

- Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
- Decision Makers: Kim Minho, Lee Jiyeong, Park Dong-hwan, Choi Min-jung, Jeong Kyung-ho, Nam Seon-seo, Lim Jae-won, Kang Hyun-jin, Seo Min-seok, Oh Yu-jin, Baek Tae-hoon
- Date: 2024-12-17

<!-- Define the situation and problem below, for example, concisely describe in 2-3 paragraphs as needed. -->

<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [상황과 문제를 아래에 정의합니다, 예를 들어 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
## Situation and Problem Definition
<!-- Define the situation and problem below, for example, in 2-3 concise sentences. -->
- Currently, when `ConfigurationManager` starts, system settings (including parameters) are loaded from a static configuration file. There is a requirement that during the initialization of `SystemSetup`, these configurations, particularly database connection settings or cache management, should be dynamically adjustable via REST APIs within the WebService without going through `ConfigurationManager`. This issue needs to be addressed.

<!-- [Supporting Evidence 2, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Supporting Evidence 1, e.g., performance and scalability] -->
<!-- The basis for decision-making may vary with each decision -->

<!-- [결정된 옵션과 이유를 서술합니다, 이유의 예시 : 유일한 옵션이거나 | 우리의 요구사항을 만족하거나 | 결과가 가장 좋거나 ] -->
<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
## Decision Rationale
<!-- Decision rationale can vary for each decision made -->
<!-- [Example Basis 1, e.g., Performance and Scalability] -->
<!-- [Example Basis 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->

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
- Previously, `sql command` was used to deliver commands to each database connection exposed at the application layer via `database_wrapper` within the WebService. Relevant information regarding configuration commands in the database specs is as follows: (Original: https://www.postgresql.org/docs/current/config-setting.html)

### Usability-Related Options
- To enhance user management convenience, options are provided at a simplified level compared to the database spec configuration commands, categorized into two forms:

  | Control Type | Name | Description | Notes |
  | ------------ | ---- | ----------- | ----- |
  | PerformanceMode | HighThroughput | Performance-centric | Supports up to 1000 connections |
  |             | Balanced | Balanced performance and resource usage | Supports up to 500 connections |
  |             | ResourceSaver | Minimizes resource consumption | Supports up to 100 connections |
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
  - NPSS: Indexed supported performance states starting from 0

<!-- Example: Improved by ADR-0005 (0005-example.md) -->
<!-- [e.g.: Requires learning curve, migration needed] -->
<!-- [Pros and Cons resulting from this decision] -->

<!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->
<!-- [예: 러닝 커브 필요, 마이그레이션 필요] -->
<!-- [결정의 긍정적 측면과 단점] -->
<!-- 선택사항 -->
### REST API Endpoints
- `/system/performance-mode`
  - Configures performance mode at the system level and manages all database connections comprehensively.
  - **GET**
    - Displays the current system-level performance mode.
    - Provides the total aggregated connection usage of databases at the system level.
  - **PUT**
    - Sets the system-level performance mode.
- `/databases/{instanceId}/connection-state`
  - **GET**
    - Retrieves and informs about the current connection status of a specific database identified by `instanceId`.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "Database connection status was successfully retrieved."
      }
      $
      ```
  - **PUT**
    - Sets the performance mode of a specific database identified by `instanceId` to the specified connection state.
    - ```bash
      $ curl -k -X PUT https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} \
      -H "Content-Type: application/json" \
      -d '{ "state": 1 }' | jq
      {
        "currentConnectionState": 1,
        "message": "Database performance mode was successfully updated."
      }
      $
      ```
- `/databases/{instanceId}/connection-state/detail`
  - **GET**
    - Provides detailed connection status information for a specific database identified by `instanceId`.
    - Includes current connection state, supported connection states by the database, etc.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "Database performance mode was successfully retrieved.",
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

### Exception Handling
- When a database does not support performance mode:
  - Generally, whether a specific database supports performance mode can be determined through configuration commands (Config Parameter #max_connections, States 0 ~ 31, totaling 32 states). If the requested connection state exceeds supported values, it defaults to the closest supported value.
- When a database supports performance mode but incorrect parameters are provided:
  - Defaults to the closest supported value.
- During a Hot Swap event for the database, the current performance mode status is checked, and necessary adjustments are applied according to configuration.
  - Total connection usage may change during Connect/Disconnect operations.
  - System-level performance management synchronization and updates related to these changes are required.

### Results <!-- Optional -->
<!-- [Positive aspects and drawbacks of the decision] -->
<!-- [Example: Learning curve required, migration needed] -->
- As mentioned in [Decision Rationale](#decision-rationale), the WebService can **directly dynamically control** the database connection state.

## Related ADRs <!-- Optional -->

- [Link Type] [Insert ADR Link Here] <!-- Example: [ADR-0005](0005-example.md) -->

---

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**