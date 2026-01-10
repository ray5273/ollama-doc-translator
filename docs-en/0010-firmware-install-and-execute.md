# Translation Test : Microservices Deployment Rehearsal Manual for Training Purposes Only! This document is intended solely as a training tool and contains various styles of writing along with technical jargon intentionally mixed together. 

In this scenario, we assume the following goals and environment:
- Goal: Deploying a simulated microservices bundle to simulate server operations observationally
- Environment: The `orion-stack` image exists in your local repository; access control node is reachable at address `<192.168.10.77>`. 

**Practice Note*** - Commands provided are examples and should be adjusted according to team environment regarding the use of 'sudo' or paths as necessary.</b></i><br/>- All REST calls assume usage with self-signed certificates, hence include `-k` option in commands.

## 1. Preparation Checklist Before Deployment Rehearsal Starts: Verify each item below before proceeding to deployment rehearsal steps.<ul>
<li>Record the image version and hash.</li><br/>\
<li>Activate a test virtual environment from shell access.]</p></list>>
```bash
$ systemctl stop lab-api
$ systemctl stop lab-agent
$ docker system prune -f
```
## 2. Diagnosing Sandbox State Before Service Activation: Check container, service status before initiating services.<ul><li class="list-item">Service Status Checks</b></i>>`systemctl status lab-agent`, `lab-api`. </span>>> <br/>\                                                            			      				       					        						         							          																	           
<p>Container List: `<code style = "color : blue; "> $ docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`</span></b><br/>\                                                            			      				       					        						         							          																	           
<p>Storage Summary: `<code style = "color : green; "> $ df -h /var/lib/orion 
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**