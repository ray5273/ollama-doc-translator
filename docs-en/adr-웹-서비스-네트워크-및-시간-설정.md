<!-- [Below Context and problem Defines, Example Then, Freedom As a formal matter 2~3 Please provide the Korean text you would like translated into English. Simply Explanation: Okay.]-->
<!-- Options -->
<!-- [Proposed | Rejected | Approved | Discarded | ... | [ADR-0005](0005-example.md)The provided text "로" translates to "as" or could be context-dependent, potentially meaning "with" or "by" depending on usage in a sentence. Without additional context, a direct translation isn't fully precise. Could you provide more context or the full sentence? Replacement] -->
# [ADR] Web Service Network and Time Configuration REST API Design

* Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
* Decision Makers: Yang Yoonho, Park Sanghyuk
* Date: 2024/04/25

<!-- Define the context and issues below, for example, succinctly describe in 2-3 sentences as needed. -->

<!-- Decision The basis is Every At every decision. Different Water It exists. -->
<!-- [Evidence 1, e.g., Performance And Scalability] -->
<!-- [Evidence 2, e.g., Advanced Function, Community And Support, License Back...] -->
<!-- [Context and problem Below Defines, Example Listen 2~3 Please provide the Korean text you would like translated into English. Simply Explanation: Okay.]-->
## Situation and Problem Definition
<!-- [Define the situation and problem below, for example, concisely in 2-3 sentences.] -->
To adequately support web application servers, there is a need for functionality that allows management of system network settings and time settings through REST APIs in a cloud environment server.

Decisions regarding these specifics are required.

### Basic Assumptions
- ApplicationManager operates as a static binary rather than a container, enabling direct execution of OS commands. (static-binary-adr.md)
- Linux is assumed to be Ubuntu 22.04 with kernel version 5.15.

<!-- [Supporting Evidence 2, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Supporting Evidence 1, e.g., performance and scalability] -->
<!-- The basis for decisions may vary for each decision made -->

<!-- [Determined Options and Reason It describes., Reason's Example : Unique Option or | Our Requirements Satisfied or | The result is The most Good or ] -->
<!-- [Example 2, e.g., Advanced Function, Community And Support, License Back...] -->
<!-- [Example 1, e.g., Performance And Scalability] -->
<!-- Decision The basis is Every At every decision. Different Water It exists. -->
## Decision Rationale
<!-- Decision rationale can vary for each decision -->
<!-- [Example 1, e.g., Performance and Scalability] -->
<!-- [Example 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->
When adding functionality to modify system settings, follow the following priorities:
1. Utilize libraries supported by Golang.
2. Configure using Linux system services.
3. Directly modify files to apply changes.

<!-- Describe the chosen options and reasons: e.g., unique option | meets our requirements | best results -->

## Decision
<!-- [Selected Options and Reason It describes., Example: Unique Option | Our Requirements Satisfied | The best Result ] -->
The process for determining configurations regarding REST API and documentation creation was as follows:

### Network Configuration Decisions
1. `systemd-networkd.service` (netplan) will be utilized for network setup configuration (pre-installed on Ubuntu).
   - Version: 4.2-2ubuntu2
2. Users will be guided to configure network settings on the final page of the GUI.

Network Configuration Examples:
1. The network settings API within REST API must support two methods:
    - Manual assignment of IP, DNS, gateway, etc.
    - Automatic IP assignment via DHCP
2. To maintain a single endpoint for network configuration via REST API:
   - The REST API accepts the following parameters:
     - PUT /settings/network/ parameters:
       - | Parameter  | Type, Description                                           |
         |------------|-------------------------------------------------------------|
         | type       | string (tcp/rdma), network type of the target network.         |
         | networkPortSettings | array of networkPortSettings, settings per port |
         | ntpServers | array of strings, NTP servers of the system.              |
      - Parameters within `networkPortSettings`:
       - | Parameter     | Type, Description                                                                                                                                                                                             |
         |---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
         | isDhcpEnabled | boolean, DHCP status of the target network port.                                                                                                                                                          |
         | ip            | string, IP address of the target network port.                                                                                                                                                           |
         | cidr          | integer, CIDR of the target network port.                                                                                                                                                                |
         | gateway       | string, gateway of the target network port.                                                                                                                                                               |
         | dnsPrimaryAddress | string, primary DNS of the target network port.                                                                                                                                                           |
         | dnsSecondaryAddress | string, secondary DNS of the target network port. Omitted if only primary DNS address exists.                                                                         |
         | mtuBytes       | integer(int64), MTU of the target network port. (e.g., 1500, 4200, 9000) Recommended MTU sizes based on usage: management port 1500, RDMA data port 4200, TCP data port 9000                                                                         |
         | portNum        | integer(int64), port number of the target network port. Port allocation logic handled by web service firmware.                                                                                                    |
      
   - To ensure exclusivity between DHCP and static IP configurations, simultaneous inclusion of `isDhcpEnabled=true` along with (ip | cidr | gateway | dns) parameters in API requests is prohibited:
     - DHCP Configuration: Send API request with `isDhcpEnabled=true` and omit ip, cidr, gateway, dns from body.
     - Static IP Configuration: Include ip, cidr, gateway, dns in body and send API request with `isDhcpEnabled=false`.
3. Limit DNS server settings to a maximum of two.
4. Always generate a new `/etc/netplan/99-WebService-custom.yaml` file during netplan configuration.
5. Change the extension of all configuration files under `/etc/netplan/` to "*.config.time.bak" to prevent conflicts with existing IP configurations, ensuring only `/etc/netplan/99-WebService-custom.yaml` is applied.
6. Apply network server settings using the `netplan apply` command.

<!-- Example: [ADR-0005](0005-example.md)The provided text "로" translates to "as" or "with" in English, depending on context. Without additional context, a direct translation isn't fully accurate, but generally:

- As a standalone word, it can mean "as."
- In phrases, it often translates to "with." 

Please provide more context if a precise translation is needed. Improved -->
### Time Configuration Decisions

1. Use `systemd-timedated.service` (`timedatectl`) for manual time setting support.
   - Strings inputable for timezone during manual time setting match the results of `timedatectl list-timezones`. (Validation code not included)
   - String format inputable to `timedate` follows RFC3339 date-time format (e.g., "2021-07-01T00:00:00Z").
2. Verify NTP server usage with the `timedatectl status` command.
   - Activate/deactivate NTP server using `timedatectl set-ntp true` / `timedatectl set-ntp false`.
   - Configure NTP server settings using `chrony.service`.
3. Redefine settings in `/etc/chrony/chrony.conf` to apply NTP configuration.
4. Allow input of up to three NTP servers (based on Dell BM results).
5. Maintain a single endpoint for time configuration via REST API.
   - The REST API accepts the following parameters:
     - PUT /settings/time
     - | Parameter   | Type, Description                                  |
       |-------------|----------------------------------------------------|
       | timezone    | string, System timezone.                |
       | timedate    | string \<date-time\>, System date and time  |
       | ntpServers  | array of strings, System NTP servers. |

     - To maintain exclusivity between NTP configuration and manual time setting, simultaneous inclusion of `ntpServers` (`timedate` | `timezone`) in API requests is not allowed.
       - Condition for NTP server configuration: API transmission without including `timezone` and `timedate` in the body.
       - Condition for manual time setting: API transmission without including `ntpServers` in the body.

<!-- Example: Improved by [ADR-0005](0005-example.md) -->

<!-- Example: [ADR-0005](0005-example.md)The provided text "로" translates to "as" or "with" in English, depending on context. Without additional context, a direct translation cannot specify the exact usage. Please provide more context if needed for a precise translation. However, sticking strictly to translation:

"As" or "With Improved -->
<!-- Options -->
## Related ADR <!-- Optional -->

* [Link Type] [ADR Link Insertion] <!-- Example: Improved to [ADR-0005](0005-example.md) -->

---

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**