# &lt;Service Name&gt;

**Interface Definition Document**

- Version: &lt;x.y&gt;
- Created Date: &lt;Month DD, YYYY&gt;

> Template prepared by IBM for the IBM Bob pilot from the layout of the Online Middleware Interface Definition Document. Replace every &lt;placeholder&gt;. Red text is guidance and is removed in the final document. File name: EAI_Interface_Definition_Document_&lt;Service&gt;_v&lt;x.y&gt;.docx

## Document Signoff

| Bank Contact: |
|---|
| Signature : ______________________ |
| Date : ______________________ |
| Doc Version: ______________________ |

## Version History

| Sl. No. | Author (s) | Version | Date | Change Description |
|---|---|---|---|---|
| 1 | &lt;author&gt; | 1.0 | &lt;DD Mon YYYY&gt; | Initial Draft |
| 2 |   |   |   |   |
| 3 |   |   |   |   |

> Add one row for every change to the service, with the requirement reference in the description.

**Table of Contents**

- 1 Document Overview
- 2 Logical View
  - 2.1 Logical Components Layers
- 3 General Process Implementation
  - 3.1 Behaviour
  - 3.2 Security
  - 3.3 Header and Error Mapping
  - 3.4 Exception and Error Handling
- 4 &lt;Service&gt; Services
    - 4.1.1 Summary
    - 4.1.2 Processing Logic
    - 4.1.3 Data Exchange
    - 4.1.4 Dependencies

## 1 Document Overview

This document describes the Technical Architecture of the middleware and Interface that satisfies business requirements of interacting with backend/host system solutions in real-time.

The goal of this Technical Architecture & Design document is to define the technologies, products, and techniques necessary to develop and support the system, and to ensure that the system components are compatible and comply with the enterprise-wide standards and direction defined by the bank.

This document will also:

- Describe business, logical and application view.
- Design message transformation and business functions for the services.

## 2 Logical View

### 2.1 Logical Components Layers

> Insert the diagram as an image. Show only where this service sits: consuming applications, API Gateway, the OMW layers and services, and the back end. Do not draw infrastructure.

```
Consuming Applications
        |
API Gateway
        |
OMW:  Global REST Layer | Global SOAP Layer
      <Service> API     | <Service> Service (<codes>)
        |
<Back end, e.g. CORE (FlexCube)>
```

## 3 General Process Implementation

### 3.1 Behaviour

All inquires / posting will be done using web services. The Message broker will expose the services required by consuming applications via SOAP XML or RESTFull JSON.

### 3.2 Security

The proposed solution for implementing security between the channel and middleware is as following

- **Transport level security:** All traffic between channel and middleware will be using HTTPS.

### 3.3 Header and Error Mapping

The following table describes the header of the payload message. These elements are to be filled in by the channel/application.

**EAISERVICES – HEADER**

| SN | Fields | Type | Length | M/O | Comments | Populated By |
|---|---|---|---|---|---|---|
| **EAIServices/Header/** |   |   |   |   |   |   |
| 1 | MsgVersion | String | 11 | M | Version of Common Data Model structure. | Middleware |
| 2–11 | &lt;copy from an existing IDD&gt; |   |   |   | Rows 2 to 11 of the standard header were not visible in the scoping session recording. |   |
| 12 | SrvOpCode | String | 15 | O | Unique identifier to represent operational code on the context for which the request is generated (Online/Batch/loopback) | Source Application/Requestor |
| 13 | TargetApp | String | 15 | O | Target Application name | Middleware |
| 14 | EAITimestamp | String | yyyy-MM-dd HH:mm:ss.SSSSSS | O | Defaulted to current middleware system date & time. ISO8601 format | Middleware |
| 15 | TrackingId | String | 255 | O | Additional ID for debug/logging across the services. Used within ESB domain to trace the messages across the services | Middleware |
| 16 | OrgId | String | 15 | M | Country/region identifier of the service. Ex: AE is for UAE, QA is for Qatar, BH is for Bahrain, EG is for Egypt, KW is for Kuwait and IN for India | Source Application/Requestor |
| 17 | InstanceId | String | 15 | O | Typically used for multi engine instances, internal to ESB implementation. | Middleware |
| 18 | Status | String | 15 | O | This captures the status of the service. | Middleware |
| 19 | UserId | String | 15 | M | Unique Username for each application | Source Application/Requestor |
| 20 | SecurityInfo | String | 255 | O | Reserved for content based any security | Source Application/Requestor |
| 21 | Language | String | 15 | O | Reserved for Language | Source Application/Requestor |
| 22 | AddlData1 | String | 255 | O | Additional Data | Optional |
| 23 | AddlData2 | String | 255 | O | Additional Data | Optional |

**EAI SERVICES – EXCEPTION**

| SN | Fields | Type | Length | M/O | Comments | Populated By |
|---|---|---|---|---|---|---|
| **EAIServices/Body/ExceptionDetails/** |   |   |   |   |   |   |
| 01 | Errorcode | String | 15 | O | Derived on the Error Mapping Table Code of ESB. In case the mapping is not available it will carry a generic error code representing system error | Mapped from ESB/Host Application/Provider |
| 02 | ErrorDesc | String | 255 | O | Description as per Mapping Table. If not defined it would be a generic message | Mapped from ESB/Host Application/Provider |
| 03 | Type | String | 15 | O | Represents Business or Technical Failure | Mapped from Host Application/Provider |
| 04 | Trace | String | 255 | O | Concatenation of all type of ID available in application response node | Mapped from Host Application/Provider |
| 05 | Data | String | 255 | O | Concatenation of all Error details sent by Host Application(s) | Mapped from Host Application/Provider |
| 06 | ReferenceNo | String | 32 | O | Generally holds unique reference no generated during transaction. | Mapped from Host Application/Provider |

> For a REST API, list the HTTP headers as well.

| SN | Fields | Type | Length | M/O | Comments | Populated By |
|---|---|---|---|---|---|---|
| **HTTP Headers** |   |   |   |   |   |   |
| 1 | X-USER-ID | String | 11 | M | Unique Username for each application | Source Application/Requestor |
| 2 | X-ORG-ID | String | 15 | M | Country/region identifier of the service | Source Application/Requestor |
| 3 | X-MSG-ID | String | 15 | M | Unique ID. Channel Interface must ensure that this ID is uniquely identified across all Applications along with SrcAppId. Duplicate check may be performed by HOST applications on this field | Source Application/Requestor |
| 4 | X-TRACKING-ID | String | 15 | O | Backend system message id which is expected to come in Middleware response | Middleware |

### 3.4 Exception and Error Handling

| Error Code | Description | Header/Status | Remarks |
|---|---|---|---|
| EAI-&lt;XXX&gt;-BRK-000 | Success | S | Service Completed. |

Detailed Error mapping can be referred in the attached error code mapper.

## 4 &lt;Service&gt; Services

> One or two sentences: what the service is used for.

#### 4.1.1 Summary

- **Integration Name**: &lt;Service&gt;
- **Availability:** &lt;Business and Non-Business hours&gt;
- **Backend Applications Accessed:** &lt;back end&gt;
- **Location of use:** &lt;service code&gt; - &lt;countries, e.g. AE, QA, EG, BH, KW&gt;

#### 4.1.2 Processing Logic

> One bullet per rule that the code applies: routing, enrichment, conditions, defaults. Take them from the code, not from the requirement document.

- &lt;rule 1&gt;
- &lt;rule 2&gt;

#### 4.1.3 Data Exchange

**4.1.3.1 &lt;OPERATION NAME&gt; (&lt;service code&gt;)**

**INPUT**

| Common XSD Field | Description | Data Type | Transformation/Processing Logic |
|---|---|---|---|
| **EAIServices/Body/&lt;Operation&gt;Req** |   |   |   |
| &lt;field&gt; | &lt;description&gt; | String | &lt;logic, or blank for a plain mapping&gt; |
| **EAIServices/Body/&lt;Operation&gt;Req/&lt;Group&gt; [Repeating]/&lt;Group&gt;** |   |   |   |
| &lt;field&gt; | &lt;description&gt; | String |   |

**OUTPUT**

| Common XSD Field | Description | Data Type | Transformation/Processing Logic |
|---|---|---|---|
| **EAIServices/Body/&lt;Operation&gt;Res** |   |   |   |
| Status | Status | String |   |
| ErrorCode | ErrorCode | String |   |
| ErrorDesc | ErrorDesc | String |   |
| &lt;field&gt; | &lt;description&gt; | String |   |

> Repeat 4.1.3.x for every operation of the service. List every field, input and output.

#### 4.1.4 Dependencies

> Everything the service needs at build and run time.

| Type | Name | Purpose |
|---|---|---|
| Shared library | &lt;library&gt; |   |
| Java archive | &lt;jar&gt; |   |
| Queue | &lt;queue&gt; |   |
| Database object | &lt;table or procedure&gt; |   |
| Back-end endpoint | &lt;service / operation&gt; |   |
