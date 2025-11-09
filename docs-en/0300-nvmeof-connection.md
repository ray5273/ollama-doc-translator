# NVMe-oF Connection Guide
This document guides you through connecting PBSSD and an initiator using the NVMe-oF (NVMe over Fabrics) protocol. Once PBSSD firmware installation and box initialization are complete, and the volume is `attached`, PBSSD is ready to process I/O commands.

This document assumes the following goals and environments:
- **Goal:** Connect to the NVMe-oF subsystem of the PBSSD target using a 100Gbps network interface from the initiator
- **Environment:**
  - Box initialization is completed, and the intended volume is properly `attached`.
  - PBSSD is connected to the initiator via a 100Gbps network interface using IP address `10.100.3.8`.
  - Box initialization was completed through TCP-based connection, and NVMe-oF utilizes the TCP transport layer.

> **Example Usage Note:**
> - Some commands may require `sudo` privileges depending on the environment.

## Discovering NVMe-oF Devices
Before an initiator connects to NVMe devices provided by PBSSD, it must use the `nvme discover` command to check the list of NVMe-oF subsystems (NVMe Qualified Name, NQN) discoverable in the NVMe-oF network.

**1. Command**  
The `nvme discover` command can be used in the following format to retrieve a list of NVMe-oF subsystems corresponding to the specified transport protocol, address (`traddr`), and port (`trsvcid`):
```bash
$ nvme discover -t <TRANSPORT_PROTOCOL> -a <TRANSPORT_ADDRESS> -s <TRANSPORT_SERVICE>
```
Here is a description of the command options:

| Option                  | Flag | Description                                                                                           |
|-------------------------|------|-------------------------------------------------------------------------------------------------------|
| `transport protocol`   | `-t` | Network transmission protocol used in the NVMe-oF (NVMe over Fabrics) environment (e.g., `tcp`, `rdma`) |
| `transport address`    | `-a` | Network transmission protocol used in the NVMe-oF (NVMe over Fabrics) environment                     |
| `transport service ID` | `-s` | Network service identifier used in the NVMe-oF (NVMe over Fabrics) environment (PBSSD I/O default port: 1152, 1153) |

**2. Command Usage Example**  
The `nvme discover` command is used to query the list of NVMe-oF subsystems (NVMe Qualified Name, NQN) provided by the target PBSSD.
```bash
$ nvme discover -t tcp -a 10.100.3.8 -s 1152
```
```bash
Discovery Log Number of Records 8, Generation counter 8
=====Discovery Log Entry 0======
trtype:  tcp
adrfam:  ipv4
subtype: current discovery subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2014-08.org.nvmexpress.discovery
traddr:  10.100.3.8
eflags:  explicit discovery connections, duplicate discovery information
sectype: none
=====Discovery Log Entry 1======
trtype:  tcp
adrfam:  ipv4
subtype: current discovery subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2014-08.org.nvmexpress.discovery
traddr:  10.10.100.12
eflags:  explicit discovery connections, duplicate discovery information
sectype: none
=====Discovery Log Entry 2======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
traddr:  10.10.100.12
eflags:  none
sectype: none
=====Discovery Log Entry 3======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
traddr:  10.100.3.8
eflags:  none
sectype: none
=====Discovery Log Entry 4======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f
traddr:  10.10.100.12
eflags:  none
sectype: none
=====Discovery Log Entry 5======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f
traddr:  10.100.3.8
eflags:  none
sectype: none
=====Discovery Log Entry 6======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  1
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa
traddr:  10.10.100.12
eflags:  none
sectype: none
=====Discovery Log Entry 7======
trtype:  tcp
adrfam:  ipv4
subtype: nvme subsystem
treq:    not required
portid:  0
trsvcid: 1152
subnqn:  nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa
traddr:  10.100.3.8
eflags:  none
sectype: none
```

## Connecting NVMe-oF Devices
Use the `nvme connect` command to connect to an NVMe-oF subsystem. With this command, the connected subsystem is registered as an NVMe block device in the initiator's operating system, allowing block I/O operations such as partitioning, formatting, and mounting through device files (e.g., `/dev/nvme0n1`) similar to local SSDs.

**1. Command**  
The `nvme connect` command can be used in the following format to connect to an NVMe-oF subsystem specified by the transmission protocol, address (`traddr`), port (`trsvcid`), and NQN (NVMe Qualified Name):
```bash
$ nvme list-subsys
```
Here is a description of the command options:

| Option  | Flag | Description                                                                                                                                                                                                 |
|---------|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `transport protocol` | `-t` | Network transmission protocol used in the NVMe-oF (NVMe over Fabrics) environment (e.g., `tcp`, `rdma`)                                                                                                    |
| `transport address` | `-a` | Network transmission protocol address used in the NVMe-oF environment                                                                                                                                      |
| `transport service ID` | `-s` | Network service identifier used in the NVMe-oF environment (PBSSD I/O default port: 1152, 1153)                                                                                                          |
| `nqn name`             | `-n` | Unique name identifying the NVMe-oF target (target) (`nvme connect` command uses `subtype` as `subnqn` for `nvme subsystem`)                                                                               |

**2. Command Usage Examples**  
After discovering NVMe-oF subsystems using the `nvme discover` command, identify the NQN of the subsystem with `traddr` as `10.10.3.8`, then specify this NQN as the `<NQN_NAME>` argument in the `nvme connect` command to connect to the target PBSSD subsystem:
```bash
$ nvme connect -t tcp -n nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f -a 10.10.3.8 -s 1152
$ nvme connect -t tcp -n nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa -a 10.10.3.8 -s 1152
$ nvme connect -t tcp -n nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57 -a 10.10.3.8 -s 1152
```
```bash
connecting to device: nvme0
connecting to device: nvme1
connecting to device: nvme2
```
Use the `nvme list` command to check currently connected NVMe-oF devices. The Firmware Revision (`FW Rev`) value provided by PBSSD for NVMe-oF devices is `25.05`.
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme0n1          /dev/ng0n1            S871NG0Y200019       undefined                                0x1         29.88 TB / 29.88 TB    512 B +  0 B   25.05   
/dev/nvme1n1          /dev/ng1n1            S871NG0Y200015       undefined                                0x1        536.87 MB / 536.87 MB    512 B +  0 B   25.05   
/dev/nvme2n1          /dev/ng2n1            S871NG0Y200015       undefined                                0x1        536.87 MB / 536.87 MB    512 B +  0 B   25.05   
# Local NVMe devices may also be listed here.
```
Use the `nvme list-subsys` command to check connected NVMe-oF subsystems (NVMe Qualified Names, NQN):
```bash
$ nvme list-subsys
```
```bash
...
nvme-subsys0 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:bcf5b9ad-7697-4615-b093-7b675f2e9c0f
               hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
    +- nvme0 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live
nvme-subsys1 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:c0e7d24f-7838-43c8-bd15-c2dd506e99aa
                hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
    +- nvme1 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live

nvme-subsys2 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
                hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
    +- nvme2 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live
...
```

# Example Markdown in Korean:

```
# Please provide the Korean text you would like translated. Markdown Example

## Title

This Part **Emphasis**It seems there might be a typo or missing context in your request as "를" by itself does not form a complete phrase or sentence in Korean for translation. Could you please provide the full text you would like translated? I use it..

- List Item 1
- List Item 2
- List Item 3

> Quote Example
```

## Title 1
This Section is It seems there might be a misunderstanding in your request as no Korean text was provided for translation. Could you please provide the Korean text you would like translated into English? Written Markdown This is an example..

### Title 2
* Emphasized Please provide the Korean text you would like translated.
* List Item 1
* List Item 2

- Order List Item 1
- Order List Item 2

Code Block Example:
```python
def hello_world():
    print("Hello, World!")
```

Link Example: [Naver](https://www.naver.com)

Table Example:
| Heat 1 | Heat 2 | Heat 3 |
|------|------|------|
| Data 1 | Data 2 | Data 3 |
| Data 4 | Data 5 | Data 6 |

<!-- This The translation of "주석은" to English is "The annotation is" or more contextually appropriate might depend on the full sentence, but generally, it refers to "The comment" or "The annotation." Without additional context, this is the direct translation. As is It remains/is maintained. -->

- 1Stage Work
- 2Stage Work
- 3Stage Work

**Important text** *Maintain unchanged format*

## Disconnect NVMe-oF Devices
Use the `nvme disconnect` and `nvme disconnect-all` commands to disconnect from the NVMe-oF subsystem.

**1. `nvme disconnect` Command**  
The `nvme disconnect` command can be used in the following format to disconnect a specific NVMe-oF subsystem associated with a given NQN:

```bash
$ nvme disconnect -n <NQN_NAME>
```

**2. Example Usage of `nvme disconnect` Command**  
First, identify the NQN value of the subsystem you wish to disconnect by listing connected subsystems:

```bash
$ nvme list-subsys
```
```bash
...
nvme-subsys2 - NQN=nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
                hostnqn=nqn.2014-08.org.nvmexpress:uuid:f69d0000-f592-11f0-8000-10ffe0aebc03
\
 +- nvme2 tcp traddr=10.10.100.11,trsvcid=1152,src_addr=10.10.10.51 live
...
```
Use the queried NQN value as the `<NQN_NAME>` parameter in the `nvme disconnect` command:

```bash
$ nvme disconnect -n nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57
```
```bash
NQN:nqn.2023-01.com.samsung.semiconductor:uuid:718c4d01-a419-4b19-bc9d-20d71df29c57 disconnected 1 controller(s)
```
After disconnecting the NVMe-oF device, it will no longer appear in the output of the `nvme list` command.

```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme0n1          /dev/ng0n1            S871NG0Y200019       undefined                                0x1         29.88  TB /  29.88  TB    512   B +  0 B   25.05   
/dev/nvme1n1          /dev/ng1n1            S871NG0Y200015       undefined                                0x1        536.87  MB / 536.87  MB    512   B +  0 B   25.05   
# Local NVMe devices may also be listed here.
```

**3. `nvme disconnect-all` Command**  
The `nvme disconnect-all` command can be used in the following format to disconnect from all currently connected NVMe-oF subsystems:

```bash
$ nvme disconnect-all 
```

**4. Example Usage of `nvme disconnect-all` Command**  
Execute the `nvme disconnect-all` command to disconnect all connections:

```bash
$ nvme disconnect-all 
```
After disconnecting, the `nvme list` command output will no longer show NVMe-oF devices. Note that the `nvme disconnect-all` command only affects remote NVMe-oF devices and does not impact local NVMe SSDs.

```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
# Only local nvme device will appear
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**