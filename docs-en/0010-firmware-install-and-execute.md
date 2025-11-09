# PBSSD Firmware Installation & Execution Guide
This document provides guidance on the installation (PBSSD Firmware Installation) and execution (PBSSD Firmware Execution) procedures of PBSSD firmware.

This document assumes the following goals and environment:
- **Goal:** Control PBSSD firmware installation and execution
- **Environment:** Debian package for PBSSD firmware is prepared

> **Example Usage Note:**
> - Some commands may require `sudo` privileges depending on the environment.
> - REST API Requests
>   - It is assumed that the administrator account uses `admin:admin`.
>   - Commands are written with the `-k` option included in `curl` assuming the use of a self-signed certificate.

## PBSSD Firmware Installation
PBSSD firmware installation procedure.

**1. Firmware Package Installation**  
Use the following command to install the firmware:  
*Note: The PBSSD firmware Debian package must be located in the `/tmp` directory before installation.*
```bash
$ apt install /tmp/pos-essential_2.6.0_arm64.deb
```
```bash
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
...
```

**2. Firmware Installation Verification**  
After installing PBSSD firmware, verify that the relevant container images are loaded correctly by executing the `docker images` command.
```bash
$ docker images
```
```bash
REPOSITORY                         TAG                  IMAGE ID       CREATED         SIZE
anomaly_detector                   2.6.0                5bc6c9128795   5 hours ago     93.3MB
anomaly_detector                   latest               5bc6c9128795   5 hours ago     93.3MB
iow_bin                            2.6.0                32e2bc79fc17   5 hours ago     2.73GB
iow_bin                            latest               32e2bc79fc17   5 hours ago     2.73GB
pos-essential-management-ui        2.6.0                44b51bd6950d   5 hours ago     202MB
pos-essential-management-ui        latest               44b51bd6950d   5 hours ago     202MB
fluent/fluent-bit                  2.2.0                f2a704f310c2   24 months ago   81.5MB
fluent/fluent-bit                  2.6.0                f2a704f310c2   24 months ago   81.5MB
jaegertracing/all-in-one           1.50                 06ec8144ca8c   2 years ago     57.4MB
jaegertracing/all-in-one           2.6.0                06ec8144ca8c   2 years ago     57.4MB
grafana/loki                       2.6.0                33a5847e7daf   2 years ago     72.4MB
grafana/loki                       2.9.0                33a5847e7daf   2 years ago     72.4MB
prom/prometheus                    2.6.0                eb8939d5c174   2 years ago     240MB
prom/prometheus                    v2.47.0              eb8939d5c174   2 years ago     240MB
quay.io/prometheus/node-exporter   2.6.0                6a33998eca8a   2 years ago     21.9MB
quay.io/prometheus/node-exporter   v1.6.0               6a33998eca8a   2 years ago     21.9MB
otel/opentelemetry-collector       0.77.0               afb19f2adefc   2 years ago     90.7MB
otel/opentelemetry-collector       2.6.0                afb19f2adefc   2 years ago     90.7MB
```

## PBSSD Status Check Before Starting PBSSD Firmware
Before starting the PBSSD firmware, the status responses for each command have been documented. Since the PBSSD firmware services are currently not running, the PBSSD service status is `inactive`.

**1. Service Status Verification**  
The installed PBSSD firmware consists of multiple services, and the status of these services can be checked using the following commands. Given that the PBSSD firmware services are not running, the PBSSD service status is `inactive`.
```bash
$ systemctl status orc_init
```
```bash
○ orc_init.service - Daemon for running a script for pre-settings required before executing Pos Essential Orchestrator
     Loaded: loaded (/etc/systemd/system/orc_init.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Tue 2025-10-30 04:23:34 UTC; 26min ago
     ...
```
```bash
$ systemctl status orc_run
```
```bash
○ orc_run.service - pos-essential-orchestrator
     Loaded: loaded (/etc/systemd/system/orc_run.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Tue 2025-10-30 04:23:34 UTC; 26min ago
     ...
```

**2. Container Status Verification**  
The installed PBSSD firmware operates in container form, and the status of the containers can be checked using the following command. Since the PBSSD firmware services are not running, the relevant containers are not active.
```bash
$ docker ps
```
```bash
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

**3. Storage Status Verification**  
The storage status can be verified using the following command. The `nvme list` command can be used to identify NVMe devices registered with the operating system.  
*Note:* After starting the PBSSD firmware, NVMe devices managed by the firmware will not be exposed via this command.
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme0n1          /dev/ng0n1            S871NG0Y200017       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme10n1         /dev/ng10n1           Y3P200LXNSJ4         KBG40ZPZ128G TOSHIBA MEMORY              0x1        128.04  GB / 128.04  GB    512   B +  0 B   AEGA0103
/dev/nvme11n1         /dev/ng11n1           S871NG0Y200018       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme12n1         /dev/ng12n1           S871NG0Y200015       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
/dev/nvme1n1          /dev/ng1n1            S871NG0Y200022       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme2n1          /dev/ng2n1            S871NG0Y200019       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme3n1          /dev/ng3n1            S871NG0Y200014       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme4n1          /dev/ng4n1            S871NG0Y200016       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme5n1          /dev/ng5n1            S871NG0Y200023       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00  GB /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme6n1          /dev/ng6n1            S871NG0Y200069       SAMSUNG MZWMO30THCLF-01AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRATB57
/dev/nvme7n1          /dev/ng7n1            S871NG0Y200070       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
/dev/nvme8n1          /dev/ng8n1            S871NG0Y200074       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q
/dev/nvme9n1          /dev/ng9n1            S871NG0Y200071       SAMSUNG MZWMO30THCLF-00AW7               0x1          0.00   B /  30.72  TB    512   B +  0 B   OPRA4B5Q

# Development Environment Setup Guide

## Introduction
This The guide is New Developer In the project Effectively Participate Water To enable/make possible Development environment Setting up Method Welcome..

## Necessary tools and software
- **Essential tools**: Git, Visual Studio Code, Node.js
- **Recommended Tools**: Docker, Postman

## Environment Setup Steps
1. **Install Git**
   - [Git Official Website](https://git-scm.com/)From Latest Version Download and Installation is underway..
   - Installation Completed After, Git BashIt seems there might be a typo or missing text in your request as "를" by itself does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Through Version Confirmation: `git --version`

2. **Visual Studio Code Settings**
   - [VS Code Download Page](https://code.visualstudio.com/download)From Installation file Downloading.
   - Installation After, Expansion program Through Necessary Language Support Addendum (Yes: JavaScript, TypeScript).

3. **Install Node.js**
   - [Node.js Official Website](https://nodejs.org/)From LTS Version Download and Installation is underway..
   - Installation Confirmation: `node -v` And `npm -v` Command Execution

4. **Optional Docker Installation**
   - [Docker Official Website](https://www.docker.com/products/docker-desktop)From Docker DesktopThe provided text "을" translates to "as" or depends on context, often functioning as a particle indicating the object of a verb in Korean sentences. Without additional context, a direct translation isn't fully illustrative, but generally:

"as" (in certain contexts) Download and Installation is underway..
   - Installation After, Docker Version Confirmation: `docker --version`

## Project initialization
1. Project Folder Creation: `mkdir myProject && cd myProject`
2. Git Initialization: `git init`
3. Basic `.gitignore` File Creation: `echo "# Ignore files" > .gitignore`
4. `package.json` Creation: `npm init -y`

## Setting up a Test Environment (Recommended)
- **Using Postman**: API Test For Request Creation And Test
- **Using Docker**: Application Containerization And Distribution Environment Construction

## Conclusion
This Guide Through Basic Development environment Successfully You have set it up.. Now Project Development Focus Water It exists..

### Additional Resources
- [Git Official Document](https://git-scm.com/doc)
- [Node.js Developer Guide](https://nodejs.org/en/docs/)

## Starting PBSSD Firmware
`orc_run` service starts the PBSSD firmware.
```bash
$ systemctl start orc_run
```

## PBSSD Status Check After Starting PBSSD Firmware
PBSSD firmware status responses for each command are listed below after initiating the PBSSD firmware.

**1. Service Status Verification**  
The status of the `orc_init` and `orc_run` services can be verified using the following commands. Both services should be in `Active: active` state, with `orc_run` specifically showing `running`.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://localhost/api/v1/firmware/status'
```
```bash
● orc_init.service - Daemon for running a script for pre-settings required before executing Pos Essential Orchestrator
     Loaded: loaded (/etc/systemd/system/orc_init.service; enabled; vendor preset: enabled)
     Active: active (exited) since Tue 2025-10-30 04:51:17 UTC; 3s ago
     ...
```
```bash
$ systemctl status orc_run
```
```bash
● orc_run.service - Pos Essential Orchestrator
     Loaded: loaded (/etc/systemd/system/orc_run.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2025-10-30 04:51:17 UTC; 3s ago
     ...
```

**2. Container Status Verification**  
To verify the container runtime status, execute the following command if the PBSSD firmware service is running correctly. Five containers should be running: `ui`, `prometheus`, `node-exporter`, `opentelemetry-collector`, `anomaly_detector`.
```bash
$ docker ps
```
```bash
CONTAINER ID   IMAGE                                     COMMAND                  CREATED          CONTAINER ID   IMAGE                                     COMMAND                  CREATED        STATUS        PORTS     NAMES
38458f7fbb0b   quay.io/prometheus/node-exporter:v1.6.0   "/bin/node_exporter ..."   1 second ago   Up 1 second             pos-essential-node-exporter
f5aca9be9211   prom/prometheus:v2.47.0                   "/bin/prometheus --w..."   1 second ago   Up 1 second             pos-essential-prometheus
f1137a330130   pos-essential-management-ui:latest        "python3 rest/app.py"    1 second ago   Up 1 second             pos-essential-management-ui
2070f50fa42b   anomaly_detector:latest                   "/bin/sh -c ./main"      1 second ago   Up 1 second             pos-essential-ssd-anomaly-detector
6877e9285056   otel/opentelemetry-collector:0.77.0       "/otelcol --config /..."   1 second ago   Up 1 second             pos-essential-opentelemetry-collector
```

**3. Storage Status Verification**  
Upon executing the PBSSD firmware via `orc_run` service, PBSSD firmware directly controls NVMe devices from the operating system, making them invisible through the `nvme list` command. Only the SSD where the operating system resides will be displayed. Verify storage status using the following command:
```bash
$ nvme list
```
```bash
Node                  Generic               SN                   Model                                    Namespace  Usage                      Format           FW Rev  
--------------------- --------------------- -------------------- ---------------------------------------- ---------- -------------------------- ---------------- --------
/dev/nvme10n1         /dev/ng10n1           Y3P200LXNSJ4         KBG40ZPZ128G TOSHIBA MEMORY              0x1        128.04  GB / 128.04  GB    512   B +  0 B   AEGA0103
# Most NVMe devices are not shown by nvme list command due to user space control by PBSSD.
```

**4. PBSSD Status Verification via REST API**  
Retrieve the current version information of the PBSSD firmware by calling the `GET /firmware` endpoint of the REST API.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://localhost/api/v1/firmware'
```
```bash
{
  "commit": "70b5ec9982b62a567524042eb54797062264f68a",
  "lastUpdated": "2025-10-30-02:59:54-UTC",
  "name": "PBSSD-Edinburgh-Essential-Firmware",
  "version": "2.6.0"
}
```
Call the `GET /firmware/status` endpoint of the REST API to retrieve the integrated status and module statuses along with version details of each configuration service within the PBSSD firmware. The `Total` field under `FirmwareServices` indicates the overall system status, while other `name` fields represent individual modules comprising the PBSSD firmware. In the example below, box initialization is incomplete, leading to `Not Running` status for the `pos-essential-ioworker` module responsible for IO within PBSSD firmware, resulting in a `Failed` `Total` status.
```bash
$ curl -k -X GET \
-u 'admin:admin' \
-H 'Accept: application/json' \
'https://localhost/api/v1/firmware/status'
```
```bash
{
  "FirmwareServices": [
    {
      "name": "Total",
      "status": "Failed"
    },
    {
      "name": "pos-essential-orchestrator",
      "status": "Need Initialize",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-ioworker0",
      "status": "Not Running"
    },
    {
      "name": "pos-essential-ssd-anomaly-detector",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-management-ui",
      "status": "Running",
      "version": "2.6.0"
    },
    {
      "name": "pos-essential-opentelemetry-collector (Third Party)",
      "status": "Running",
      "version": "0.77.0 (2.6.0)"
    },
    {
      "name": "pos-essential-node-exporter (Third Party)",
      "status": "Running",
      "version": "2.6.0 (v1.6.0)"
    },
    {
      "name": "pos-essential-prometheus (Third Party)",
      "status": "Running",
      "version": "2.6.0 (v2.47.0)"
    },
    {
      "name": "pos-essential-ipmi-exporter (Third Party)",
      "status": "Running",
      "version": "1.6.1"
    }
  ],
  "common": {
    "message": "Firmware status retrieved successfully",
    "relatedJobs": null
  }
}
```

Call the `GET /devices` endpoint of the REST API to retrieve information about NVMe devices controlled by the PBSSD firmware.
```
REST APIIt seems there might be a typo or incomplete text provided ("의" alone doesn't form a complete phrase). Could you please provide the full Korean text you would like translated? `GET /devices` Endpoint Call them PBSSD Firmware Controlling NVMe Device's Information I confirm it..
```
```bash
{
  "devices": [
    {
      "address": "0000:1d:00.0",
      "bdevName": "nvme7424n1",
      "capabilities": [],
      "firmware": {
        "name": "OPRA4B5Q"
      },
      "modelNumber": "SAMSUNG MZWMO30THCLF-00AW7",
      "numa": -1,
      "serialNumber": "S871NG0Y200070",
      "size": 30720827326464,
      "slotId": 7424,
      "status": -20
    },
    {
      "address": "0000:29:00.0",
      "bdevName": "nvme10496n1",
      "capabilities": [],
      "firmware": {
        "name": "OPRATB57"
      },
      "modelNumber": "SAMSUNG MZWMO30THCLF-01AW7",
      "numa": -1,
      "serialNumber": "S871NG0Y200018",
      "size": 30720827326464,
      "slotId": 10496,
      "status": -20
    },
    ...
  ],
  "message": "Devices retrieved successfully",
  "relatedJobs": null
}

## Stopping PBSSD Firmware
`orc_run` service stopping halts the execution of PBSSD firmware.
```bash
$ systemctl stop orc_run
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**