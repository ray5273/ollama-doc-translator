<!-- [Below Situation and The problem Defines, For example When you come, Freedom In a formal manner 2~3 In a sentence. Concisely If you explain it Okay..]-->
<!-- Options -->
<!-- [Suggested | Rejected | Approved | Discarded | ... | [ADR-0005](0005-example.md) to Replaced] -->
# [ADR] Web Service Network and Time Setting REST API Design

* Document Status: Approved <!-- [Proposed | Rejected | Approved | Canceled | ... | Replaced with [ADR-0005](0005-example.md) ] --> <!-- Optional -->
* Decision Maker: Yang Yoon-ho, Park Sang-hyeok
* Date: 2024/04/25

<!-- [Define the situation and problem here, for example, it is good to briefly explain in 2~3 sentences in a free form.] -->

<!-- Decision The basis/reason Okay. For each decision Different Number There is. -->
<!-- [Basis 1, e.g., Performance  and Scalability] -->
<!-- [Basis 2, e.g., High-end Function, Community  and Support, License back...] -->
<!-- [Situation and The problem Below Defines, For example Enter 2~3 In a sentence. Concisely If you explain it Okay..]-->
## Situation and Problem Definition
<!-- [Please define the situation and problem below, for example, in a concise manner of 2~3 sentences.] -->
To properly support a web application server, the ability to manage system network settings and time settings through a REST API in a cloud environment server is required.

The following specific details need to be determined.

### Basic Assumptions
- ApplicationManager operates as a static binary and can execute OS commands directly. (static-binary-adr.md)
- Assumes Ubuntu 22.04 with Linux kernel version 5.15.

<!-- [Reason 2, e.g., advanced features, community and support, license etc...] -->
<!-- [Reason 1, e.g., performance and scalability] -->
<!-- The reason for each decision may vary. -->

<!-- [Decided Options and The reason I will explain., Reasons Example : The only one Either or | ours The requirements Satisfied or | The result The most Good/Okay ] -->
<!-- [Example 2, e.g., High-end Function, Community  and Support, License back...] -->
<!-- [Example 1, e.g., Performance  and Scalability] -->
<!-- Decision The basis/reason Okay. For each decision Different Number There is. -->
## Reasons for Decision
<!-- The reasons for decision may vary depending on each decision -->
<!-- [Example 1, e.g., Performance and Scalability] -->
<!-- [Example 2, e.g., Advanced Features, Community and Support, License, etc...] -->
When adding the functionality to modify the system settings, follow the following priority:
1. Utilize libraries supported by Golang.
2. Configure using Linux system services.
3. Apply changes by directly modifying the file.

<!-- [Describe the chosen option and the reason, e.g., because it is the only option | because it satisfies our requirements | because it yields the best results] -->

<!-- [Selected Options and The reason I will write it., Example: The only one Options | ours The requirements Satisfied | The best Result ] -->
## Decisions
<!-- [Describe the chosen option and reason, e.g., The only option | Satisfies our requirements | Best result] -->
The discussion process regarding REST API and document creation was decided as follows:

### Network Configuration Decisions
1. We will use `systemd-networkd.service` (netplan) to support network configuration. (Pre-installed on Ubuntu)
   - Version: 4.2-2ubuntu2
2. Guide users to configure network settings from the last page of the GUI.

Network configuration example:
1. The REST API must support two methods for network configuration:
    - Manual assignment of IP, DNS, gateway, etc.
    - Automatic IP assignment via DHCP
2. Maintain a single endpoint for network configuration via REST API:
   - The REST API receives the following parameters:
     - PUT /settings/network/ parameters:
       - | Parameter | Type, Description |
         |------------|-------------------------------------------------------------|
         | type       | string (tcp/rdma), network type of the target network.     |
         | networkPortSettings | networkPortSettings array, network settings for each port |
         | ntpServers | string array, NTP servers for the system.              |
      - Parameters within `networkPortSettings`:
       - | Parameter     | Type, Description |
         |---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
         | isDhcpEnabled | boolean, DHCP status of the target network port.                                                                                                                                                          |
         | ip            | string, IP address of the target network port.                                                                                                                                                           |
         | cidr          | integer, CIDR of the target network port.                                                                                                                                                                |
         | gateway        | string, gateway of the target network port.                                                                                                                                                               |
         | dnsPrimaryAddress | string, primary DNS of the target network port.                                                                                                                                                           |
         | dnsSecondaryAddress | string, secondary DNS of the target network port. Omit if only the primary DNS address is present.                                                                                                        |
         | mtuBytes       | integer(int64), MTU of the target network port. Recommended MTU size: 1500 for management ports, 4200 for RDMA data ports, and 9000 for TCP data ports.                                                                                                        |
         | portNum        | integer(int64), port number of the target network port. Port allocation logic is handled by the web service firmware.                                                                                                    |
      
   - To ensure mutual exclusivity between DHCP and fixed IP settings, we will prevent the inclusion of `isDhcpEnabled=true` and (ip | cidr | gateway | dns) parameters in the API request:
     - DHCP configuration: Send API with `isDhcpEnabled=true` without including ip, cidr, gateway, and dns in the body.
     - Fixed IP configuration: Send API with ip, cidr, gateway, and dns, with `isDhcpEnabled=false`.
3. Limit DNS server configuration to a maximum of 2.
4. Always create a new `/etc/netplan/99-WebService-custom.yaml` file during netplan configuration.
5. Change the extension of all configuration files in `/etc/netplan/` to "*.config.time.bak" to ensure that only `/etc/netplan/99-WebService-custom.yaml` is applied, preventing conflicts with existing IP configurations.
6. Apply the network server settings using the "netplan apply" command.

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
### Time Configuration Decisions

1. To support manual time setting, we use `systemd-timedated.service` (`timedatectl`).
   - When manually setting the time, the timezone string value that can be entered in `timedatectl` is the same as the result of `timedatectl list-timezones` (without verification code).
   - When manually setting the time, the string format that can be entered in `timedate` follows the RFC3339 date-time format (e.g., "2021-07-01T00:00:00Z").
2. Use the `timedatectl status` command to verify if the NTP server is in use.
   - Use `timedatectl set-ntp true` / `timedatectl set-ntp false` to enable/disable the NTP server.
   - Configure the NTP server using `chrony.service`.
3. Apply the NTP configuration by overriding the settings in `/etc/chrony/chrony.conf`.
4. Allow up to 3 NTP server inputs (based on Dell BM results).
5. Maintain a single endpoint for time configuration via REST API.
   - The REST API receives the following parameters:
     - PUT /settings/time
     - | Parameter | Type, Description |
       |-------------|----------------------------------------------------|
       | timezone    | string, System time zone.                |
       | timedate    | string <date-time>, System date and time  |
       | ntpServers  | String array, System NTP servers. |
   - To maintain the mutual exclusivity between NTP configuration and manual time setting, we do not allow including both `ntpServers` and (`timedate` | `timezone`) in the API request.
     - NTP server configuration condition: API transmission without including `timezone` and `timedate` in the body.
     - Manual time setting condition: API transmission without including `ntpServers` in the body.

<!-- Example: Improved with [ADR-0005](0005-example.md) -->

<!-- Example: [ADR-0005](0005-example.md) to Improved -->
<!-- Options -->
## Related ADR <!-- Optional -->

* [Link type] [Insert ADR link] <!-- Example: Improved to [ADR-0005](0005-example.md) -->

--->

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**