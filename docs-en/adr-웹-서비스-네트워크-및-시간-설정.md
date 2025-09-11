<!-- [아래에 상황과 문제를 정의합니다, 예를 들면, 자유 형식으로 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
<!-- 선택사항 -->
<!-- [제안됨 | 거부됨 | 승인됨 | 폐기됨 | ... | [ADR-0005](0005-example.md)로 대체됨] -->
# [ADR] Web Service Network and Time Configuration REST API Design

* Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
* Decision Makers: Yang Yoonho, Park Sanghyuk
* Date: 2024/04/25

<!-- Define the situation and problem below, for example, succinctly describe in 2~3 sentences as needed. -->

<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
<!-- [근거 1, e.g., 성능 및 확장성] -->
<!-- [근거 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [상황과 문제를 아래에 정의합니다, 예를 들어 2~3 문장으로 간결하게 설명하면 좋습니다.]-->
## Situation and Problem Definition
<!-- Define the situation and problem below, for example, in 2-3 concise sentences. -->
To adequately support a web application server, there is a need for a feature that allows managing system network settings and time settings within a cloud environment server via REST APIs.

Decisions regarding these specifics are required.

### Basic Assumptions
- ApplicationManager operates as a static binary rather than a container, enabling direct execution of OS commands. (static-binary-adr.md)
- Linux is assumed to be Ubuntu 22.04 with kernel version 5.15.

<!-- [Supporting Evidence 2, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Supporting Evidence 1, e.g., performance and scalability] -->
<!-- The basis for decisions may vary for each decision made -->

<!-- [결정된 옵션과 이유를 서술합니다, 이유의 예시 : 유일한 옵션이거나 | 우리의 요구사항을 만족하거나 | 결과가 가장 좋거나 ] -->
<!-- [예시 2, e.g., 고급 기능, 커뮤니티 및 지원, 라이선스 등...] -->
<!-- [예시 1, e.g., 성능 및 확장성] -->
<!-- 결정 근거는 매 결정마다 다를 수 있습니다 -->
## Decision Rationale
<!-- Decision rationale can vary for each decision made -->
<!-- [Example 1, e.g., Performance and Scalability] -->
<!-- [Example 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->
When adding a feature to modify system settings, follow the following priorities:
1. Utilize libraries supported by Golang.
2. Configure using Linux system services.
3. Directly modify files to apply changes.

<!-- Describe the chosen options and reasons: reasons might include | being the only option | meeting our requirements | yielding the best results | -->

<!-- [선택된 옵션과 이유를 서술합니다, 예시: 유일한 옵션 | 우리의 요구사항을 만족 | 최고의 결과 ] -->
## Decision Points
<!-- [Describe the selected option and reason, e.g., Unique option | Meets our requirements | Best results ] -->
The discussion process regarding the setup for REST API and documentation has been decided as follows:

### Network Configuration Decisions
1. `systemd-networkd.service` (netplan) will be used to support network configuration setup (pre-installed on Ubuntu).
   - Version: 4.2-2ubuntu2
2. Users will be guided to configure network settings on the last page of the GUI.

Network Configuration Examples:
1. The network settings API within REST API should support two methods:
    - Manual assignment of IP, DNS, gateway, etc.
    - Automatic IP assignment via DHCP
2. To maintain a single endpoint for network configuration via REST API:
   - The REST API accepts the following parameters:
     - PUT /settings/network/ Parameters:
       - | Parameter  | Type, Description                                           |
         |------------|-------------------------------------------------------------|
         | type       | string (tcp/rdma), Network type of the target network.       |
         | networkPortSettings | Array of network port settings, |
         | ntpServers | Array of strings, NTP servers for the system.              |
      - Parameters within `networkPortSettings`:
       - | Parameter     | Type, Description                                                                                                                                                                                             |
         |---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
         | isDhcpEnabled | boolean, DHCP status for the target network port.                                                                                                                                                          |
         | ip            | string, IP address for the target network port.                                                                                                                                                           |
         | cidr          | integer, CIDR for the target network port.                                                                                                                                                                |
         | gateway        | string, Gateway for the target network port.                                                                                                                                                               |
         | dnsPrimaryAddress | string, Primary DNS for the target network port.                                                                                                                                                           |
         | dnsSecondaryAddress | string, Secondary DNS for the target network port. Omitted if only primary DNS address is provided.                                                                         |
         | mtuBytes       | integer(int64), MTU for the target network port. (e.g., 1500, 4200, 9000) Recommended MTU sizes based on use case: Management port - 1500, RDMA data port - 4200, TCP data port - 9000                                                                         |
         | portNum        | integer(int64), Port number for the target network port. Port allocation logic handled by web service firmware.                                                                                                    |
      
   - To ensure exclusivity between DHCP and static IP configurations, simultaneous inclusion of `isDhcpEnabled=true` along with (ip | cidr | gateway | dns) parameters in API requests is prohibited:
     - DHCP Configuration: Send API request with `isDhcpEnabled=true` and omit ip, cidr, gateway, dns from the body.
     - Static IP Configuration: Include ip, cidr, gateway, dns in the body and send API request with `isDhcpEnabled=false`.
3. DNS server settings are limited to a maximum of two servers.
4. A new `/etc/netplan/99-WebService-custom.yaml` file is always created during netplan configuration.
5. Change the extension of all configuration files under `/etc/netplan/` to "*.config.time.bak" to prevent conflicts with existing IP configurations, ensuring only `/etc/netplan/99-WebService-custom.yaml` is applied.
6. Use the "netplan apply" command to apply network server settings.

<!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->
### Time Configuration Decisions

1. Use `systemd-timedated.service` (`timedatectl`) to support manual time setting.
   - For manual time setting, the string values inputable for timezone are identical to those listed by `timedatectl list-timezones`. (Validation code not included)
   - For manual time setting, the string format inputable to `timedate` follows the RFC3339 date-time format (e.g., "2021-07-01T00:00:00Z").
2. Use the `timedatectl status` command to verify if the NTP server is active.
   - Activate/deactivate the NTP server using `timedatectl set-ntp true` / `timedatectl set-ntp false`.
   - Configure NTP server settings using `chrony.service`.
3. Redefine settings in the `/etc/chrony/chrony.conf` file to apply NTP configuration.
4. Allow input of up to three NTP servers (based on Dell BM results).
5. Maintain a single endpoint for time configuration via REST API.
   - The REST API accepts the following parameters:
     - PUT /settings/time
     - | Parameter   | Type, Description                                  |
       |-------------|----------------------------------------------------|
       | timezone    | string, System timezone.                |
       | timedate    | string \<date-time\>, System date and time  |
       | ntpServers  | array of strings, System NTP servers. |

     - To maintain exclusivity between NTP configuration and manual time setting, simultaneous inclusion of `ntpServers` and (`timedate` | `timezone`) in API requests is not allowed.
       - Condition for NTP server configuration: API transmission without including `timezone` and `timedate` in the body.
       - Condition for manual time setting: API transmission without including `ntpServers` in the body.

<!-- Example: Improved by [ADR-0005](0005-example.md) -->

<!-- 예시: [ADR-0005](0005-example.md)로 개선됨 -->
<!-- 선택사항 -->
## Related ADR <!-- Optional -->

* [Link Type] [ADR Link Insertion] <!-- Example: Improved with ADR-0005(0005-example.md) -->

---

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**