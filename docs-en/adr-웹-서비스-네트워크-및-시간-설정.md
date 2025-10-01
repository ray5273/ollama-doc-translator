<!-- [Below Context and problem Defines, Example Then, Freedom As a formal response:

In English: "Formally 2~3 Please provide the Korean text you would like translated into English. Simply Explain please. Okay.]-->
<!-- Options -->
<!-- [Proposed | Rejected | Approved | Discarded | ... | [ADR-0005](0005-example.md)The provided text "로" translates to "as" or could be context-dependent, potentially meaning "with" or another preposition depending on usage within a sentence. Without additional context, a direct translation isn't fully precise. Could you provide more context or the full sentence? Replacement] -->
# [ADR] Web Service Network and Time Configuration REST API Design

* Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
* Decision Makers: Yang Yoonho, Park Sanghyuk
* Date: 2024/04/25

<!-- Define the context and issues below, for example, succinctly describe in 2~3 sentences as needed. -->

<!-- Decision The basis is Every At every decision Different Water It exists. -->
<!-- [Evidence 1, e.g., Performance And Scalability] -->
<!-- [Evidence 2, e.g., Advanced Function, Community And Support, License Back...] -->
<!-- [Context and problem Below Defines, Example Listen 2~3 Please provide the Korean text you would like translated into English. Simply Explain please. Okay.]-->
## Situation and Problem Definition
<!-- [Define the situation and problem below, for example, concisely in 2~3 sentences.]-->
To adequately support web application servers, there is a need for a feature that allows management of system network settings and time settings within a cloud environment server via REST API.

Decisions regarding these specifics are required.

### Basic Assumptions
- ApplicationManager operates as a static binary rather than a container, enabling direct execution of OS commands. (static-binary-adr.md)
- Linux is assumed to be Ubuntu 22.04 with kernel version 5.15.

<!-- [e.g., Advanced features, community and support, licensing for basis 2] -->
<!-- [e.g., Performance and scalability for basis 1] -->
<!-- The basis for decisions may vary for each decision made -->

<!-- [Determined Options and Reason It describes., Reason Example : Unique Option or | Our Requirements Satisfied or | The result is The most Good or ] -->
<!-- [Example 2, e.g., Advanced Function, Community And Support, License Back...] -->
<!-- [Example 1, e.g., Performance And Scalability] -->
<!-- Decision The basis is Every At every decision Different Water It exists. -->
## Decision Rationale
<!-- Decision rationale can vary for each decision -->
<!-- [Example 1, e.g., Performance and Scalability] -->
<!-- [Example 2, e.g., Advanced Features, Community and Support, Licensing, etc...] -->
When adding functionality to modify system settings, follow these priorities:
1. Utilize libraries supported by Golang.
2. Configure using Linux system services.
3. Directly modify files to apply changes.

<!-- Describe the chosen options and reasons: e.g., unique option | meets our requirements | best results -->

<!-- [Selected Options and Reason It describes., Example: Unique Option | Our Requirements Satisfied | The best Result ] -->
## Decision Points
<!-- [Describe the selected option and reason, e.g., Unique option | Meets our requirements | Best results ] -->
The discussion process regarding REST API development and documentation has been decided as follows:

### Network Configuration Decisions
1. Use `systemd-networkd.service` (netplan) to support network setup configuration (pre-installed on Ubuntu).
   - Version: 4.2-2ubuntu2
2. Guide users to configure network settings on the last page of the GUI.

Network Configuration Examples:
1. The network settings API within REST API should support two methods:
    - Manual assignment of IP, DNS, gateway, etc.
    - Automatic IP assignment via DHCP
2. Maintain a single endpoint for network configuration via REST API:
   - The REST API accepts the following parameters:
     - PUT /settings/network/ parameters:
       - | Parameter  | Type, Description                                           |
         |------------|-------------------------------------------------------------|
         | type       | string (tcp/rdma), Network type of the target network.       |
         | networkPortSettings | Array of network port settings, |
         | ntpServers | Array of strings, NTP servers of the system.              |
      - Parameters within `networkPortSettings`:
       - | Parameter     | Type, Description                                                                                                                                                                                             |
         |---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
         | isDhcpEnabled | boolean, DHCP status of the target network port.                                                                                                                                                          |
         | ip            | string, IP address of the target network port.                                                                                                                                                           |
         | cidr          | integer, CIDR of the target network port.                                                                                                                                                                |
         | gateway        | string, Gateway of the target network port.                                                                                                                                                               |
         | dnsPrimaryAddress | string, Primary DNS of the target network port.                                                                                                                                                           |
         | dnsSecondaryAddress | string, Secondary DNS of the target network port. Omitted if only primary DNS address exists.                                                                         |
         | mtuBytes       | integer(int64), MTU of the target network port. (e.g., 1500, 4200, 9000) Recommended MTU sizes based on usage: Management port - 1500, RDMA data port - 4200, TCP data port - 9000                                                                         |
         | portNum        | integer(int64), Port number of the target network port. Port allocation logic handled by web service firmware.                                                                                                    |
      
   - To ensure exclusivity between DHCP and static IP configurations, avoid including both `isDhcpEnabled=true` along with (ip | cidr | gateway | dns) parameters in API requests:
     - DHCP Configuration: Send API request with `isDhcpEnabled=true` and omit ip, cidr, gateway, dns from the body.
     - Static IP Configuration: Include ip, cidr, gateway, dns in the body and send API request with `isDhcpEnabled=false`.
3. Limit DNS server settings to a maximum of two.
4. Always generate a new `/etc/netplan/99-WebService-custom.yaml` file during netplan configuration.
5. Change the extension of all configuration files under `/etc/netplan/` to "*.config.time.bak" to prevent conflicts with existing IP configurations, ensuring only `/etc/netplan/99-WebService-custom.yaml` is applied.
6. Apply network server settings using the `netplan apply` command.

### Time Configuration Decisions

1. Use `systemd-timedated.service` (`timedatectl`) for manual time setting support.
   - For manual time setting, the string values inputable for timezone are identical to the results of `timedatectl list-timezones`. (Validation code not included)
   - For manual time setting, the string format inputable to `timedate` follows the RFC3339 date-time format (e.g., "2021-07-01T00:00:00Z").
2. Use the `timedatectl status` command to verify if the NTP server is active.
   - Activate/deactivate the NTP server using `timedatectl set-ntp true` / `timedatectl set-ntp false`.
   - Configure NTP server settings using `chrony.service`.
3. Redefine settings in the `/etc/chrony/chrony.conf` file to apply NTP configuration.
4. Allow up to three NTP server inputs (based on Dell BM results).
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

<!-- Example: [ADR-0005](0005-example.md)The provided text "로" translates to "as" or could be contextually interpreted differently depending on usage (e.g., particle, suffix). Without additional context, a direct translation is challenging, but generally, it functions similarly to "as" in English sentences. Please provide more context if a precise translation is needed. 

Given the instruction to respond solely with the translation:
"as Improved -->

<!-- Example: [ADR-0005](0005-example.md)The provided text "로" translates to "as" or "with" in English, depending on context. Without additional context, a direct translation isn't fully accurate, but generally:

- As a standalone word, it can mean "as."
- In phrases, it often translates to "with."

Please provide more context if a precise translation is needed. Improved -->
<!-- Options -->
## Related ADR <!-- Optional -->

* [Link Type] [ADR Link Insertion] <!-- Example: Improved with [ADR-0005](0005-example.md) -->

---

> **⚠️ This document is an AI-translated document.**

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**