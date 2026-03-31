# Translation Test : Experimental Network Configuration Guide for Nebula Node Setup in Lab Environment 
This document describes the process of configuring network interfaces on a virtual device `Nebula Node` used during lab sessions. Do not apply this to actual hardware equipment yet!

### Assumptions about our environment:
- **Objective**: Assigning static IP addresses through management interface from an educational control node for high data ports in RDMA testing scenarios, 
  where the target port does not have any assigned IPs at present and manual configuration is required.
   
> ***Lab Note***    	      		     			       				         					        - Adjust commands requiring `sudo` according to your environment's permissions if necessary; always use `-k` flag for REST calls assuming self-signed certificates are in place, as shown below: 
  ```bash   						                                                      																          								    	      		     			       				         					        > ```bash
$ curl -k -X PUT \
-u 'trainer:trainer' \
-H 'Content-Type: application/json' \
-d '{
  "type": "rdma",
  "networkPortSettings": [
    {
      "portNum": 3,
      "ip": "192.168.40.10",
      "cidr": 24,
      "gateway": "192.168.40.1",
      "dnsPrimaryAddress": "1.1.1.1",
      "dnsSecondaryAddress": "8.8.8.8",
      "isDhcpEnabled": false
    }
  ]
}' \
'https://172.20.0.8/api/v1/training/network'
```bash   						                                                      																          								    	      		     			       				         					        > ```
### Applying Network Configuration ### [3.1] Structure of Request Body | Field Name  | Type           |** Description **| Port Number ** |* IP Address *** *| CIDR Block *---| Gateway **** |} 256 characters or less for each field, ensuring clarity and brevity in request payloads sent to the server endpoint
```bash   						                                                      																          								    	      		     			       				         					        > ```
### Verifying Results ### [4.] Testing Reachability: Use `curl -k -X GET ...` again for confirmation of IP assignment on port number 3. Test gateway reach with command `$ ping <gateway-ip>`, and record fabric wait times using the appropriate RDMA statistics collection commands as needed in your environment setup documentation or lab notes section
### Troubleshooting Scenarios ### [5.] - **Response Delay**: If REST calls exceed a latency of 5 seconds, check `journalctl -u nebula-orchestrator` logs for any issues.
  * **- MTU Mismatch Issues*** : Since the experimental network requires an mtuBytes value set to '9000', consider adding this field in PUT requests if necessary adjustments are required based on your lab environment's specific requirements or configurations tested during setup phases of experiments conducted within these guidelines.
  * **- Incorrect Authentication Information**: Upon encountering a `401` response, retry with the newly issued practice account credentials as per troubleshooting steps outlined above for consistency and reliability in experimental setups across different iterations planned under this framework's scope

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**