<!-- [Below Context and The problem Defines, Example 들면, Freedom As a format 2~3 Please provide the Korean text you would like translated. Briefly To explain: Okay.]-->
<!-- Options -->
<!-- [Proposed | Rejected | Approved | Discarded | … | [ADR-0005](0005-example.md) to Replaced] -->
# [ADR] System Configuration Management Design and Implementation Decision Points

- Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
- Decision Makers: Kim Min-ho, Lee Ji-young, Park Dong-hwan, Choi Min-jung, Jeong Kyung-ho, Nam Seon-seo, Lim Jae-won, Kang Hyun-jin, Seo Min-seok, Oh Yu-jin, Baek Tae-hoon
- Date: 2024-12-17

<!-- Define the situation and problem below, for example, concisely describe in 2~3 paragraphs as needed. -->

<!-- Decision The basis is Every With each decision Different Water It exists. -->
<!-- [Groundwork 1, e.g., Performance  and Scalability] -->
<!-- [Groundwork 2, e.g., Advanced Function, Community  and Support, License The...] -->
<!-- [Context and The problem Below Defines, Example Listen 2~3 Please provide the Korean text you would like translated. Briefly To explain: Okay.]-->
## Situation and Problem Definition
<!-- [Define the situation and problem below, for example, concisely in 2~3 sentences.]-->
- Currently, when `ConfigurationManager` starts, system settings (including parameters) are loaded from a static configuration file, and there is a requirement that within the `SystemSetup` initialization process, these configurations, particularly database connection settings or cache management, should be dynamically adjustable via REST APIs within the WebService without going through `ConfigurationManager`. This issue needs to be addressed.

<!-- [Supporting Evidence 2, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Supporting Evidence 1, e.g., performance and scalability] -->
<!-- The basis for decision-making may vary with each decision -->

<!-- [Determined Options and Reason Describes, Reason's Example : Unique Option or | Our Requirements Satisfied or | The result is The most Good or ] -->
<!-- [Groundwork 2, e.g., Advanced Function, Community  and Support, License Back...] -->
<!-- [Groundwork 1, e.g., Performance  and Scalability] -->
<!-- Decision The basis is Every With each decision Different Water It exists. -->
## Decision Basis
<!-- Decision basis may vary for each decision -->
<!-- [Example Basis 1, e.g., Performance and Scalability] -->
<!-- [Example Basis 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->

- Enables direct control over database configuration without going through ConfigurationManager, allowing direct control from WebService.
- Previously, database connections were managed through Connection Pool, but with Database Driver usage, endpoints for connection management at the application level are available, thus eliminating the necessity to pass through Connection Pool or ConfigurationManager for control.

<!-- Describe the chosen option and reasons: e.g., unique option | meets our requirements | best results -->

<!-- [Decision made Due to Improving Point and Worsening Dot] -->
<!-- [Yes: Learning Curve Need, Migration Necessity] -->
<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- [Selected Options and Reason Describes, Example : Unique Option | Our Requirements Satisfied | The best Result ] -->
## Decisions
<!-- [Describe the selected option and reason, e.g.: Unique option | Meets our requirements | Best outcome ] -->

### Practical Configuration Commands for Database Delivery
- Previously, `sql command` was used to deliver commands to each database connection exposed at the application layer through `database_wrapper` within the WebService. Here is relevant information regarding configuration commands within the database specs: (Original: https://www.postgresql.org/docs/current/config-setting.html)

### Usability-Related Options
- To enhance user management convenience, options are provided at a simplified level compared to the database spec configuration commands, categorized into two forms:

  | Control Type | Name | Description | Note |
  | ------------ | ---- | ----------- | ---- |
  | PerformanceMode | HighThroughput | Performance-centric | Up to 1000 connections |
  |             | Balanced | Balanced performance and resource usage | Up to 500 connections |
  |             | ResourceSaver | Minimized resource consumption | Up to 100 connections |
  |             | Manual | Custom connection state | - |
  | ConnectionState | Specific Connection State | Custom setting activated when PerformanceMode is selected | - |
  
- Supported connection states per database model

  | Model | Type | NPSS | Connection State | Note |
  | ----- | ---- | ---- | --------------- | ---- |
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
  - NPSS: Indexed supported performance states (starting from 0)

<!-- Example: Improved with [ADR-0005](0005-example.md) -->
<!-- [e.g.: Requires learning curve, migration needed] -->
<!-- [Positive and negative impacts due to the decision] -->

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- [Yes: Learning Curve Need, Migration Need] -->
<!-- [Decision's Positive Side and Disadvantages] -->
<!-- Options -->
### REST API Endpoints
- `/system/performance-mode`
  - Configures performance mode at the system level and manages all database connections comprehensively.
  - **get**
    - Displays the current system-level performance mode.
    - Provides the total aggregated connection usage of databases at the system level.
  - **put**
    - Sets the system-level performance mode.
- `/databases/{instanceId}/connection-state`
  - **get**
    - Retrieves and informs about the current connection status of a specific database identified by `instanceId`.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "Database connection status was successfully retrieved."
      }
      $
      ```
  - **put**
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
  - **get**
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
  - Generally, whether a specific database supports performance mode can be determined through configuration commands (Config Parameter `#max_connections`, States 0 ~ 31, totaling 32 states). If the requested connection state exceeds supported values, it sets the closest possible value.
- When a database supports performance mode but incorrect parameters are provided:
  - Sets the value to the closest possible option.
- During a Hot Swap event for the database, checks the current performance mode and applies necessary adjustments according to configuration if needed.
  - Total connection usage may change during Connect/Disconnect operations.
  - System-level performance management synchronization and updates related to databases are required for such changes.

### Results <!-- Optional -->
<!-- [Positive aspects of the decision and drawbacks] -->
<!-- Example: Learning curve required, migration needed -->
- As mentioned in [Decision Rationale](#decision-rationale), the WebService can **directly dynamically control** the database connection state.

## Relevant ADR <!-- Optional -->

- [Link Type] [Insert ADR Link Here] <!-- Example: Improved with [ADR-0005](0005-example.md) -->

---

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**