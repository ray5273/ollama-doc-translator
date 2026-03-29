<!-- [Below Context and The problem is Defines, Please provide the Korean text you would like translated. It seems like there might be a typo or an incomplete phrase at the beginning of your request. Assuming you meant to ask for a translation, here is the translation of the provided Korean text:

"If you have any questions, please feel free to ask."

If you have a specific text you would like translated, please provide it, and I will be happy to assist you., Free Format: 2~3 The text provided is already in English, so there is no need for translation. If you have any specific text in Korean that needs translation, please provide it, and I will be happy to assist you. Briefly Translation:

Describing in English:

Please provide the Korean text you would like translated. Okay.]-->
<!-- Option -->
<!-- [Proposed | Rejected | Approved | Discarded | ... | [ADR-0005](0005-example.md) to Replaced] -->
# [ADR] Web Service Network and Time Setting REST API Design

* Document Status: Approved <!-- [Proposed | Rejected | Approved | Abandoned | ... | Replaced by [ADR-0005](0005-example.md)] --> <!-- Optional -->
* Decision Makers: Yang Yun-ho, Park Sang-hyuk
* Date: 2024/04/25

<!-- Define the context and problem, for example, in 2-3 sentences freely. -->
[TRANSLATION_END]

<!-- Decision The basis Please provide the Korean text you would like translated. Every decision Different 수 It exists. -->
<!-- [Evidence 1, e.g., Performance  and Scalability] -->
<!-- [Evidence 2, e.g., Advanced Function, Community  and Support, License The

I understand you want me to translate the Korean text to English. Please provide the Korean text you would like translated. I will respond only with the English translation, without any commentary, notes, or explanations....] -->
<!-- [The situation The problem is Below I define, Please provide the Korean text you would like translated. Enter 2~3 The text provided is already in English, so there is no need for translation. If you have any other text to translate, please provide it. Briefly Translation:

Describing in English:

Please provide the Korean text you would like translated. Okay.]-->
## Situation and Problem Definition
<!-- [Define the situation and problem below, for example, in 2-3 sentences concisely.] -->
To adequately support a web application server, it is necessary to have a feature that manages system network settings and time settings through a REST API in a cloud environment server.

Decisions regarding these specific aspects are required.

### Basic Assumptions
- ApplicationManager operates as a static binary rather than a container, allowing direct execution of OS commands. (static-binary-adr.md)
- Assume Linux is running on Ubuntu 22.04 with kernel version 5.15.

<!-- [Supporting reasons, e.g., advanced features, community and support, licensing, etc.] -->
<!-- [Justification for decision 1, e.g., performance and scalability] -->
The justification for each decision may vary.
[TRANSLATION_END]

<!-- [Determined Options Reason Describes, Reason Example : Unique Option or | Our Requirements Satisfied | Result The most Good ] -->
<!-- [Example 2, e.g., Advanced Function, Community  and Support, License 등...] -->
<!-- [Example 1, e.g., Performance  and Scalability] -->
<!-- Decision The basis Please provide the Korean text you would like translated. At every decision Different The text provided is incomplete and appears to be a placeholder or an error. Here is the translation of the available text:

"The text provided is incomplete and appears to be a placeholder or an error."

Translation: "The text provided is incomplete and seems to be a placeholder or an error. It is present. -->
## Decision Rationale
<!-- Decision rationale may vary for each decision -->
<!-- [Example 1, e.g., performance and scalability] -->
<!-- [Example 2, e.g., advanced features, community and support, licensing, etc...] -->
When adding a feature to modify system settings, the following priorities are followed:
1. Utilize libraries supported by Golang.
2. Leverage Linux system services for configuration.
3. Directly modify files to apply changes.

<!-- Describe the chosen option and its rationale, e.g., unique option or | satisfies our requirements | yields the best results | etc... -->
[TRANSLATION_END]

<!-- [Selected Options Reason Describes, Example: Unique Option | Our Requirements Satisfied | The best Result ] -->
## Decision Summary
<!-- [Describe the selected option and reason, e.g., Unique option | Satisfies our requirements | Best outcome ] -->
The decision-making process for REST API and documentation creation is as follows:

### Network Configuration Decisions
1. Use `systemd-networkd.service` (netplan) to support network configuration setup (pre-installed on Ubuntu).
   - Version: 4.2-2ubuntu2
2. Guide the user to configure network settings on the last page of the GUI.

Network Configuration Example:
1. The network settings API within the REST API should support two methods:
    - Manual assignment of IP, DNS, Gateway, etc.
    - Automatic IP assignment via DHCP
2. Maintain a single endpoint for network configuration through the REST API:
   - The REST API accepts the following parameters:
     - PUT /settings/network/ parameters:
       - | Parameter   | Type, Description                                         |
         |--------------|------------------------------------------------------------|
         | type         | string (tcp/rdma), network type of the target network.   |
         | networkPortSettings | array of networkPortSettings, settings per port |
         | ntpServers   | array of strings, NTP servers for the system.           |
      - Parameters within `networkPortSettings`:
       - | Parameter    | Type, Description                                        |
         | isDhcpEnabled | boolean, DHCP status of the target network port.       |
         | ip            | string, IP address of the target network port.          |
         | cidr          | integer, CIDR of the target network port.               |
         | gateway       | string, Gateway of the target network port.             |
         | dnsPrimaryAddress | string, Primary DNS of the target network port.     |
         | dnsSecondaryAddress | string, Secondary DNS of the target network port. Omit if only primary DNS exists. |
         | mtuBytes      | integer(int64), MTU of the target network port.          | (e.g., 1500, 4200, 9000) Recommended MTU sizes: Management port 1500, RDMA data port 4200, TCP data port 9000 |
         | portNum       | integer(int64), Port number of the target network port.   | Port allocation logic handled in the web service firmware. |
3. Ensure mutual exclusivity between DHCP and static IP configurations by preventing simultaneous inclusion of `isDhcpEnabled=true` and (ip | cidr | gateway | dns) parameters in API requests:
   - DHCP configuration: Send API request with `isDhcpEnabled=true` and do not include ip, cidr, gateway, dns in the body.
   - Static IP configuration: Send API request with ip, cidr, gateway, dns included and `isDhcpEnabled=false`.
4. Limit DNS server configurations to a maximum of two.
5. Always create a new `/etc/netplan/99-WebService-custom.yaml` file during netplan configuration.
6. Change the extension of all configuration files under `/etc/netplan/` to "*.config.time.bak" to avoid conflicts with existing IP configurations, ensuring only `/etc/netplan/99-WebService-custom.yaml` is applied.
7. Use the "netplan apply" command to apply network server settings.

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
### Time Configuration Decisions

1. Use `systemd-timedated.service` (`timedatectl`) for manual time setting support.
   - The string values inputable for timezone during manual time setting are the same as the results of `timedatectl list-timezones`. (No validation code included)
   - The string format inputable for `timedate` during manual time setting follows the RFC3339 date-time format (e.g., "2021-07-01T00:00:00Z").
2. Use the `timedatectl status` command to check if the NTP server is active.
   - Use `timedatectl set-ntp true` / `timedatectl set-ntp false` to enable/disable the NTP server.
   - Configure NTP settings using `chrony.service`.
3. Redefine the settings in `/etc/chrony/chrony.conf` to apply NTP configuration.
4. Allow up to 3 NTP server inputs (based on Dell BM results).
5. Maintain a single endpoint for time configuration via REST API.
   - The REST API accepts the following parameters:
     - PUT /settings/time
     - | Parameter   | Type, Description                               |
       |-------------|-------------------------------------------------|
       | timezone    | string, The timezone of the system.            |
       | timedate    | string \<date-time\>, The date and time of the system. |
       | ntpServers  | array of strings, The NTP servers of the system. |

     - To maintain mutual exclusivity between NTP configuration and manual time setting, do not allow simultaneous inclusion of `ntpServers` and (`timedate` | `timezone`) in API requests.
       - NTP configuration condition: Do not include `timezone` and `timedate` in the body of the API request.
       - Manual time setting condition: Do not include `ntpServers` in the body of the API request.

<!-- Example: Improved to [ADR-0005](0005-example.md) -->

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- Option -->
## Related ADR <!-- Optional -->

* [Link Type] [Insert ADR Link] <!-- Example: [ADR-0005](0005-example.md) improved -->

--->
> **⚠️ This document is an AI-translated document.**

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**