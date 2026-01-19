<!-- [Below Situation and The problem Defines, For example When you come, Freedom In a formal manner 2~3 In paragraph form. Concisely If you explain it Great..]-->
<!-- Options -->
<!-- [Suggested | Rejected | Approved | Discarded | … | [ADR-0005](0005-example.md) to Replaced] -->
# [ADR] System Configuration Management Design and Implementation Decisions

- Document Status: Approved <!-- [Proposed | Rejected | Approved | Withdrawn | … | Replaced with [ADR-0005](0005-example.md) ] --> <!-- Optional -->
- Decision Makers: Kim Min-ho, Lee Ji-young, Park Dong-hwan, Choi So-jeong, Jeong Kyung-ho, Nam Eun-seo, Im Jae-won, Kang Hyun-jin, Seo Min-seok, Oh Yu-jin, Baek Tae-hoon
- Date: 2024-12-17

<!-- [Define the situation and problem here, for example, it is recommended to briefly explain it in 2~3 sentences in a free form.] -->

<!-- Decision The basis/reason Okay. For each decision Different Number There is. -->
<!-- [Basis 1, e.g., Performance  and Scalability] -->
<!-- [Basis 2, e.g., High-end Function, Community  and Support, License back...] -->
<!-- [Situation and The problem Below Defines, For example Enter 2~3 In a sentence. Concisely If you explain it Okay..]-->
## Situation and Problem Definition
<!-- [Please define the situation and problem below, for example, providing a concise explanation in 2-3 sentences is recommended.] -->
- Currently, the ConfigurationManager loads system settings (including parameters) from a static configuration file when it starts, and there is a requirement that, during the SystemSetup initialization process, these configurations, particularly database connection settings and cache management, should be dynamically adjustable through REST APIs within the WebService, bypassing the ConfigurationManager.

<!-- [Reason 2, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Reason 1, e.g., performance and scalability] -->
<!-- The reason for the decision may vary depending on the decision. -->

<!-- [Decided Options and The reason I will explain., Reasons Example : The only one Either or | ours The requirements Satisfied or | The result The most Good or ] -->
<!-- [Basis 2, e.g., High-end Function, Community  and Support, License back...] -->
<!-- [Basis 1, e.g., Performance  and Scalability] -->
<!-- Decision The basis/reason Okay. For each decision Different Number There is. -->
## Reasons for Decision
<!-- The reasons for decision may vary depending on each decision -->
<!-- [Reason 1, e.g., Performance and Scalability] -->
<!-- [Reason 2, e.g., Advanced Features, Community and Support, License, etc.] -->

- Allows direct control of the database configuration from the WebService, bypassing the ConfigurationManager.
- Previously, database connections were managed through a Connection Pool, but even when using a Database Driver, endpoints are available for connection management at the application level, allowing control without necessarily using a Connection Pool or ConfigurationManager.

<!-- [Describe the decided options and reasons, e.g., because it is the only option, because it satisfies our requirements, or because it yields the best results] -->

<!-- [Based on the decision Because of Getting better Dots deteriorating dot] -->
<!-- [Okay.: Learning Curve Necessary, Migration Needed] -->
<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- [Selected Options and The reason I will explain., Example : The only one Options | Ours The requirements Satisfied | The best Result ] -->
## Decisions
<!-- [Describe the chosen option and reason, e.g., The only option | Satisfies our requirements | Best results] -->

### Practical Set of Configuration Commands for Database Delivery
- Previously, `sql command` was used to pass commands to the application layer through the `database_wrapper` within WebService to connect to each database. The following information is related to configuration commands within the database specification. (Original: https://www.postgresql.org/docs/current/config-setting.html)

### Usability Related Options
- Options are provided at a simplified level compared to the database specification configuration command level to improve usability:

  | Control Type | Name | Description | Notes |
  | -------- | ---- | ---- | ---- |
  | PerformanceMode | HighThroughput | Processing-centric | Up to 1000 connections |
  |  | Balanced | Balance of performance and resource usage | Up to 500 connections |
  |  | ResourceSaver | Minimize resource consumption | Up to 100 connections |
  |  | Manual | User-defined connection state | - |
  | ConnectionState | Specific connection state | User-defined setting that is activated when the Control Type is PerformanceMode | - |
  
- Supported connection states for each database model

  | Model | Type | NPSS | Connection State | Notes |
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
  - NPSS: Number of supported performance states (starting from 0)

<!-- Example: Improved with ADR-0005 (0005-example.md) -->
<!-- [Example: Need to learn the curve, need migration] -->
<!-- [What will be better and worse due to the decision] -->

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- [Okay.: Learning Curve Necessary, Migration Necessary] -->
<!-- [The decision Positive side by side Disadvantages] -->
<!-- Options -->
### REST API Endpoints
- `/system/performance-mode`
  - Configures the performance mode at the system level and manages all database connections centrally.
  - get
    - Displays the current system-level performance mode.
    - Provides the total aggregated connection usage for all databases at the system level.
  - put
    - Sets the system-level performance mode.
- `/databases/{instanceId}/connection-state`
  - get
    - Retrieves and informs the current connection state for a specific database identified by `instanceId`.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "Database connection state was successfully retrieved."
      }
      $
      ```
    - Retrieves the current connection state, including the connection state supported by the database.
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
- If the database does not support the performance mode:
  - Typically, you can determine whether a specific database supports the performance mode by checking the configuration parameters (Config Parameter #max_connections, States 0 ~ 31, a total of 32 states). If the request exceeds the supported connection state, it will be set to the closest value.
- If the database supports the performance mode but provides incorrect parameters:
  - It will be set to the closest value.
- When a Hot Swap event occurs for the database, check the current performance mode situation and apply adjustments as needed.
  - The total connection usage may change during Connect/Disconnect operations.
  - Synchronization and updates are required for the system-level performance management related to the database.

### Results <!-- Optional -->
<!-- [Positive and negative aspects of the decision] -->
<!-- [Example: Need to learn, migration required] -->
- As mentioned in [Decision Rationale](#decision-rationale), the WebService can **directly** **dynamically control** the database connection state.

## Related ADR <!-- Optional -->

- [Link Type] [Insert ADR Link] <!-- Example: Improved to ADR-0005(0005-example.md) -->

--->

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**