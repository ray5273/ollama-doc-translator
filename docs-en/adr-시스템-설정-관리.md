<!-- [Below Context and The problem is Defines, Please provide the Korean text you would like translated. It seems like there might be a typo or an incomplete phrase at the beginning of your request. Assuming you meant to ask for a translation, here is the translation of the provided Korean text:

"If you have any questions, feel free to ask."

If you have a specific text you would like translated, please provide it, and I will be happy to assist you., Free Format: 2~3 The text provided is already in English, so there is no need for translation. Here is the text as it is:

"The text provided is already in English, so there is no need for translation. Here is the text as it is: Briefly Translation:

Describing in English:

Please provide the Korean text you would like translated. Okay.]-->
<!-- Option -->
<!-- [Proposed | Rejected | Approved | Discarded | … | [ADR-0005](0005-example.md) to Replaced] -->
# [ADR] System Configuration Management Design and Implementation Decisions

- Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ...] | Replaced by [ADR-0005](0005-example.md) --> <!-- Optional -->
- Decision Makers: Kim Min-ho, Lee Ji-young, Park Dong-hwan, Choi Min-jung, Jung Kyung-ho, Nam Seon-seo, Im Jae-won, Kang Hyun-jin, Suh Min-seok, Oh Yu-jin, Baek Tae-hoon
- Date: 2024-12-17

<!-- [Define the situation and problem below, for example, briefly explain in 2-3 paragraphs in a free format.]-->
[TRANSLATION_END]

<!-- Decision The basis Please provide the Korean text you would like translated. At every decision Different Please provide the Korean text you would like translated. It is present. -->
<!-- [Evidence 1, e.g., Performance  and Scalability] -->
<!-- [Evidence 2, e.g., Advanced Function, Community  and Support, License The

I understand you want me to translate the Korean text to English. Please provide the Korean text you would like translated. I will respond only with the English translation, without any commentary, notes, or explanations....] -->
<!-- [Context and The problem is Below Defines, Please provide the Korean text you would like translated. Enter 2~3 The text provided is already in English, so there is no need for translation. Here is the text as it is:

"The text provided is already in English, so there is no need for translation. Here is the text as it is: Briefly Translation:

Describing in English:

Please provide the Korean text you would like translated. Okay.]-->
## Situation and Problem Definition
<!-- [Define the situation and problem below, for example, in 2-3 sentences concisely.] -->
- Currently, when the ConfigurationManager starts, system settings (including parameters) are loaded from a static configuration file, and there is a requirement that these configurations, particularly database connection settings and cache management, should be dynamically adjustable within the WebService through a REST API without passing through the ConfigurationManager during the SystemSetup initialization process. This issue needs to be addressed.

<!-- [Supporting reasons, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Justification for decision 1, e.g., performance and scalability] -->
The justification for each decision may vary.

<!-- [Determined Options Reason Describes, Reasoning Example : Unique Option or | Our Requirements Satisfied | Result The most Good ] -->
<!-- [Evidence 2, e.g., Advanced Function, Community  and Support, License The...] -->
<!-- [Evidence 1, e.g., Performance  and Scalability] -->
<!-- Decision The basis Please provide the Korean text you would like translated. At every decision Different 수 It exists. -->
## Decision Rationale
<!-- The decision rationale may vary for each decision -->
<!-- [Rationale 1, e.g., Performance and Scalability] -->
<!-- [Rationale 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->

- Allows direct control of database configuration without passing through ConfigurationManager, enabling direct control within the WebService.
- Previously, database connections were managed through Connection Pool, but with the use of Database Driver, endpoints for connection management at the application level are available, allowing control without necessarily going through Connection Pool or ConfigurationManager.

<!-- Describe the chosen option and its rationale, e.g., it is the only option available or | satisfies our requirements | yields the best results | etc... -->
[TRANSLATION_END]

<!-- [Decision Because of Getting better Point Deteriorating Point] -->
<!-- [Please provide the Korean text you would like translated.: Learning Curve Need, Migration Needs] -->
<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- [Selected Options Reason Describes, Example : Unique Option | Our Requirements Satisfied | The best Result ] -->
## Decisions
<!-- [Describe the selected option and its rationale, e.g., Unique option | Satisfies our requirements | Best results] -->

### Practical Configuration Command Set for Database Delivery
- Previously, to deliver commands to each database connection exposed through the application layer via `database_wrapper` within the WebService, we used `sql command`. Relevant information regarding configuration commands within the database specification is as follows. (Original: https://www.postgresql.org/docs/current/config-setting.html)

### Options Related to Usability
- To enhance user convenience, options are provided at a simplified level compared to the database specification configuration command level, divided into two forms:

  | Control Type | Name | Description | Notes |
  | ------------ | ---- | ----------- | ----- |
  | PerformanceMode | HighThroughput | Focus on throughput | Max 1000 connections |
  |  | Balanced | Balance between performance and resource usage | Max 500 connections |
  |  | ResourceSaver | Minimize resource consumption | Max 100 connections |
  |  | Manual | Custom connection state | - |
  | ConnectionState | Specific connection state | Custom setting activated when PerformanceMode | - |
  
- Supported connection states by database model

  | Model | Type | NPSS | Connection State | Notes |
  | ----- | ---- | ---- | ---------------- | ----- |
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
  - NPSS: Number of supported performance states (indexing starts from 0)

<!-- Example: [ADR-0005](0005-example.md) for improvement -->
<!-- [Need for learning curve, migration required] -->
<!-- [Positive and negative impacts of the decision] -->

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- [Please provide the Korean text you would like translated.: Learning Curve Need, Migration Need] -->
<!-- [Decision Positive Side Disadvantages] -->
<!-- Option -->
### REST API Endpoints
- `/system/performance-mode`
  - Configures the performance mode at the system level and manages all database connections collectively.
  - get
    - Displays the current system-level performance mode.
    - Provides the aggregated connection usage of all databases at the system level.
  - put
    - Sets the system-level performance mode.
- `/databases/{instanceId}/connection-state`
  - get
    - Retrieves and informs the current connection state of a specific database identified by instanceId.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "The database connection state has been successfully retrieved."
      }
      $
      ```
  - put
    - Sets the performance mode of the specific database identified by instanceId to the specified connection state.
    - ```bash
      $ curl -k -X PUT https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} \
      -H "Content-Type: application/json" \
      -d '{ "state": 1 }' | jq
      {
        "currentConnectionState": 1,
        "message": "The database performance mode has been successfully updated."
      }
      $
      ```
- `/databases/{instanceId}/connection-state/detail`
  - get
    - Provides detailed information about the connection state of a specific database identified by instanceId.
    - Current connection state, supported connection states by the database, etc.
    - ```bash
      $ curl -k https://localhost/api/v1/databases/{instanceId}/performance-mode -u {id}:{password} | jq
      {
        "currentConnectionState": 0,
        "message": "The database performance mode has been successfully retrieved.",
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

### Error Handling
- If a database does not support performance mode,
  - The support for performance mode can generally be determined through configuration commands (Config Parameter #max_connections, States 0 ~ 31, total of 32 states). If the requested connection state exceeds the supported values, it is set to the closest possible value.
- If a database supports performance mode but incorrect parameters are provided,
  - It is set to the closest possible value.
- During a Hot Swap event for the database, check the current performance mode status and apply necessary adjustments to align with the configuration.
  - Total connection usage may change during Connect/Disconnect operations.
  - Synchronization and updates related to system-level performance management of the database are required for these changes.

### Results <!-- Optional -->
<!-- [Positive aspects of the decision and its drawbacks] -->
<!-- [e.g., Learning curve required, migration needed] -->
- As mentioned in [Decision Rationale](#decision-rationale), the WebService can **directly control** the **dynamic** state of the database connections.

## Related ADR <!-- Optional -->

- [Link Type] [Insert ADR Link] <!-- Example: [ADR-0005](0005-example.md) for improvement -->

--->

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**