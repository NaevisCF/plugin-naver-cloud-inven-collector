<h1 align="center">Naver Cloud Collector</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <a href='https://www.ncloud.com/'><img width="320" src="https://www.dotnetpia.co.kr/wp-content/uploads/2021/04/ncp-logo-3-8.png"></a>  
  <p> 
    <br>
    <img alt="Version"  src="https://img.shields.io/badge/version-2.0.0-blue.svg?cacheSeconds=2592000"  />  
    <a href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank"><img alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" /></a> 
  </p> 
</div>    

**Plugin to collect Naver Cloud 2.0**

> SpaceONE's [plugin-naver-cloud-inven-collector](https://github.com/kiku99/plugin-naver-cloud-inven-collector) is a convenient tool to
get cloud service data from Naver Cloud platform.



Please contact us if you need any further information. (<elsd0326@gmail.com>)

Find us also at [Dockerhub](https://hub.docker.com/r/jihyungsong/plugin-naver-cloud-inven-collector)

---
## Plugin Information

### Package Version
- spaceone-api 2.0.183
- spaceone-core 2.0.88
- spaceone-inventory 2.0.dev160

### Service list

The following is a list of services being collected and service code information.

|No.| Service name   | Service Code |
|---|----------------|--------------|
|1| Server         |Compute|
|2| VServer    |Compute|
|3| Auto Scaling       |Compute|
|3| Load Balancer       |Networking|
|4| VLoad Balancer |Networking|
|5| VPC            |Networking|
|7| CDN Plus     |Content Delivery|
|8| CDN Global   |Content Delivery|
|9| Cloud DB      |Database|

### Tasks
- inventory.CloudService
- inventory.CloudServiceType
- inventory.Region

---

## Options

### Cloud Service Type : Specify what to collect

If cloud_service_types is added to the list elements in options, only the specified cloud service type is collected.
By default, if cloud_service_types is not specified in options, all services are collected.

The cloud_service_types items that can be specified are as follows.

<pre>
<code>
{
    "cloud_service_types": [
        'Compute',          
        'Database',         
        'Networking',
        'Content Delivery',
    ]
}
</code>
</pre>

### Ncloud Zone Environment
Zones are data centers and networks that are physically separate within a region at the national level.
Because each zone exists independently, failure in one zone does not affect the other.

- ### Zone list


|No.|Region | Zone 
|-|---------|-------------|
|1|Korea     |Classic, VPC: KR-1, KR-2|
|2|the western United States|Classic: USWN-1|
|3|Hong Kong|Classic: HK-1|
|4|Singapore|	Classic: SGN-1<br>VPC: SGN-4, SGN-5|
|5|Japan|Classic: JPN-1 <br>VPC: JPN-4, JPN-5|
|6|Germany|Classic: DEN-1|

---
## [Release note](RELEASE.md)


<!-- Security scan triggered at 2025-09-02 16:17:49 -->

<!-- Security scan triggered at 2025-09-02 17:04:52 -->