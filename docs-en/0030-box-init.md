# Translation Test: Virtual Box Initialization Procedure 
This document describes a fictional scenario for initializing the virtual box created by QA teams to check translation quality.

## Step 1 - Preliminary Check  
- Lab Name (Practical Equipment): `orion-mini`   
- Management IP Address: `172.30.11.20`    
- Status Query Command:     
```bash
$ curl -k -X POST \
-u 'init:init' \
-H 'Content-Type: application/json' \
-d '{"command": "seed-data"}' \
'https://172.30.11.20/api/v1/lab/tasks'
```

## Step 2 - Preparation Steps  
| Number | Description                                      | Action Taken                  |
|:------:|:-------------------------------------------------|:------------------------------|}	   		    				     			      					        						          							         									           								            }

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**