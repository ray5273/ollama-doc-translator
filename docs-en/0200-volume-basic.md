# Translation Test : Data Volume Practice Scenario Guide
This document is a fictional data volume management guide created to verify the accuracy of translations. Do not apply it on real infrastructure.

The following topics are covered in this documentation.: 1) [Virtual Storage](#virtual-storage),  2) [Sandbox Volumes](#sandboxedvolumes], and 3) NVMe-oF Exposure
## Virtual Store (LVS): Creating a Training LVS on an Existing SSD or Pre-existing Volume. The example below uses the device `atlas9472n1`.  
### Step 1: Create   
```bash
$ curl -k -X POST \
-u <USERNAME>:<PASSWORD> \
-H 'Content-Type: application/json' \
-d '{"alias": "training_store/demo_lvol", "action": "detach"}' \
'https://<IP_ADDRESS>/api/v1/training/lvol/attach'
``` 
| Field | Description                                      |\n---|-------------------------------------------------------|}----------------------  	   		     			    				      					        						          							         									           								            |- -|-----------------------|:-------------:-----------------|_---_-------____-__-____--________-----_____________________________.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**