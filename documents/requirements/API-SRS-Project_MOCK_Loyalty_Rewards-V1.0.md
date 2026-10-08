# MOCK DATA – Online Middleware

**Loyalty Rewards Phase 1**

- File Name: API-SRS-Project_MOCK_Loyalty_Rewards-V1.0.docx
- Author: IBM Client Engineering (mock)
- Version: 1.0
- Creation Date: 02 Oct 2026
- Release Date: 02 Oct 2026
- Released By: IBM Client Engineering (mock)
- Reviewed By: To be reviewed by the Online Middleware team

> This is a mock requirement document prepared by IBM for the IBM Bob pilot. It follows the layout of the Online Middleware SRS template. The project, services, fields and systems in it are invented. It is not a bank requirement.

**APPROVAL SIGNATURES**

| Name | Title | Date | Signature |
|---|---|---|---|
| Mock approver 1 | Program Manager – Loyalty | 02 Oct 2026 |   |
| Mock approver 2 | Cluster Head – Digital Channels | 02 Oct 2026 |   |
| Mock approver 3 | Manager – Online Middleware | 02 Oct 2026 |   |

Note : All stakeholders have to provide the signature if multiple stakeholders are involved

**REVISION RECORD**

| Change Number | Date | Section | Notes | Version |
|---|---|---|---|---|
| 1 | 02 Oct 2026 | All | Initial mock version | 1.0 |

**TABLE OF CONTENTS**

- 1 Introduction
  - 1.1 Purpose
  - 1.2 Business Requirement
  - 1.3 Project Scope
    - 1.3.1 In Scope
    - 1.3.2 Out of Scope
- 2 Project Requirements
  - 2.1 Functional Requirements
    - 2.1.1 LoyaltyPointsInquiryAPI
    - 2.1.2 LoyaltyPointsRedemptionAPI
  - 2.2 List of Error Codes & Error Description
  - 2.3 List of HTTP Status Codes
  - 2.4 Volumes Projections
  - 2.5 Assumptions

## 1 Introduction

### 1.1 Purpose

This document is to explain the system requirements spec for the OMW and API Connect interface changes part of the Loyalty Rewards Phase 1 project.

### 1.2 Business Requirement

As part of Loyalty Rewards Phase 1, customers will see their loyalty points and redeem them from the mobile and online banking channels. The points are held in the Loyalty Management System (LMS).

**Business Scope:** Two new APIs are exposed to the channels through API Connect and OMW: one to inquire the points balance and one to redeem points.

**Functionalities :** The channel sends a JSON request. OMW transforms it to the LMS XML request, calls LMS, and transforms the LMS XML response back to JSON.

**Benefits :**

- Customers can view and redeem loyalty points without contacting the call centre.
- One standard interface to LMS for all channels.

**Overall :** New APIs at API Connect and OMW to accommodate the above requested functionality.

### 1.3 Project Scope

#### 1.3.1 In Scope

As part of Loyalty Rewards Phase 1 scope, below APIs will be exposed to the MOBILE and ONLINE applications in OMW and API Connect Gateway.

| SL No | API Name | Backend | Application Development | Consumers |
|---|---|---|---|---|
| 1 | LoyaltyPointsInquiryAPI | LMS | API Connect and OMW | MOBILE, ONLINE |
| 2 | LoyaltyPointsRedemptionAPI | LMS | API Connect and OMW | MOBILE |

#### 1.3.2 Out of Scope

Any other requirements which is not mentioned in the scope. In particular:

- Points accrual and partner on-boarding.
- Changes to the existing GetToken API.

## 2 Project Requirements

### 2.1 Functional Requirements

#### 2.1.1 LoyaltyPointsInquiryAPI

- **Requirement Serial No.** R-01 · **Name** API-Interface-LoyaltyPointsInquiryAPI
- **Unique Req. Ref. No.** API-001 · **Priority** High

**LoyaltyPointsInquiryAPI** will interact with the LMS system and is used to retrieve the loyalty points balance of a customer.

**API Details:**

- API Name: **LoyaltyPointsInquiryAPI**
- API Data Format : **application/json**
- API Method : **POST**
- API oAuth Scope Name: **LOYALTY**
- API Path: **/loyalty-points-inquiry**

**Backend Details:**

- Application Name: **LMS**
- Protocol: **HTTP (XML)**
- Service Operation: **PointsInquiry**

**REST API Header Parameters**

| SN | Fields | Type | Length | M/O | Description | Populated By |
|---|---|---|---|---|---|---|
| **HTTP Request Headers** |   |   |   |   |   |   |
| 1 | ClientId | String |   | M | Client Id which is subscribed | Source Application/Requestor |
| 2 | Authorization | String |   | M | Bearer: Token received from get token API | Source Application/Requestor |
| 3 | X-USER-ID | String | 11 | M | Unique Username for each application | Source Application/Requestor |
| 4 | X-MSG-ID | String | 15 | M | Unique ID. Channel Interface must ensure that this ID is uniquely identified across all Applications along with SrcAppId. Duplicate check may be performed by HOST applications on this field | Source Application/Requestor |
| 5 | X-ORG-ID | String | 15 | M | Country/region identifier of the service. Ex: AE is for UAE | Source Application/Requestor |
| 6 | X-TRACKING-ID | String | 15 | O | Backend system message id which is expected to come in Middleware response | Middleware |

**INPUT**

| API Field | LMS Field | Data Type | Transformation/Processing Logic |
|---|---|---|---|
| JSON/Data/ | XMLNSC/PointsInquiryReq/ |   |   |
| cifNumber | CIF_Number | String | Mandatory |
| programCode | Program_Code | String | Mandatory. Allowed values: RETAIL, COBRAND |
| cardNumber | Card_Number | String | Optional |
| fromDate | From_Date | String | Optional. Format yyyy-MM-dd |
| toDate | To_Date | String | Optional. Format yyyy-MM-dd |

**OUTPUT (Success)**

| API Field | LMS field | Data Type | Transformation/Processing Logic |
|---|---|---|---|
| JSON/Data/ | XMLNSC/PointsInquiryRes/ |   |   |
| cifNumber | CIF_Number | String |   |
| memberId | Member_Id | String |   |
| tierCode | Tier_Code | String |   |
| pointsBalance | Points_Balance | String |   |
| pointsPending | Points_Pending | String |   |
| pointsExpiryDate | Points_Expiry_Date | String |   |
| status | Status | String |   |

**OUTPUT (If Failure)**

| API field | LMS field | Transformation/Processing Logic |
|---|---|---|
| JSON/Data | XMLNSC/PointsInquiryRes/ |   |
| statusCode |   | HTTP status code. Refer section 2.3 |
| statusReason |   | HTTP status. Refer section 2.3 |
| errorCode | Error_Code | OMW Error Code. Refer section 2.2 |
| errorDesc | Error_Desc | OMW Error Desc. Refer section 2.2 |

#### 2.1.2 LoyaltyPointsRedemptionAPI

- **Requirement Serial No.** R-02 · **Name** API-Interface-LoyaltyPointsRedemptionAPI
- **Unique Req. Ref. No.** API-002 · **Priority** High

**LoyaltyPointsRedemptionAPI** will interact with the LMS system and is used to redeem the loyalty points of a customer.

**API Details:**

- API Name: **LoyaltyPointsRedemptionAPI**
- API Data Format : **application/json**
- API Method : **POST**
- API oAuth Scope Name: **LOYALTY**
- API Path: **/loyalty-points-redemption**

**Backend Details:**

- Application Name: **LMS**
- Protocol: **HTTP (XML)**
- Service Operation: **PointsRedemption**

**REST API Header Parameters**

| SN | Fields | Type | Length | M/O | Description | Populated By |
|---|---|---|---|---|---|---|
| **HTTP Request Headers** |   |   |   |   |   |   |
| 1 | ClientId | String |   | M | Client Id which is subscribed | Source Application/Requestor |
| 2 | Authorization | String |   | M | Bearer: Token received from get token API | Source Application/Requestor |
| 3 | X-USER-ID | String | 11 | M | Unique Username for each application | Source Application/Requestor |
| 4 | X-MSG-ID | String | 15 | M | Unique ID. Channel Interface must ensure that this ID is uniquely identified across all Applications along with SrcAppId. Duplicate check may be performed by HOST applications on this field | Source Application/Requestor |
| 5 | X-ORG-ID | String | 15 | M | Country/region identifier of the service. Ex: AE is for UAE | Source Application/Requestor |
| 6 | X-TRACKING-ID | String | 15 | O | Backend system message id which is expected to come in Middleware response | Middleware |

**INPUT**

| API Field | LMS Field | Data Type | Transformation/Processing Logic |
|---|---|---|---|
| JSON/Data/ | XMLNSC/PointsRedemptionReq/ |   |   |
| cifNumber | CIF_Number | String | Mandatory |
| memberId | Member_Id | String | Mandatory |
| redemptionRefNo | Redemption_Ref_No | String | Mandatory. Unique reference generated by the channel |
| pointsToRedeem | Points_To_Redeem | String | Mandatory |
| redemptionType | Redemption_Type | String | Mandatory. Allowed values: CASHBACK, VOUCHER |
| creditAccountNo | Credit_Account_No | String | Optional |
| voucherCode | Voucher_Code | String | Optional |
| remarks | Remarks | String | Optional |

**OUTPUT (Success)**

| API Field | LMS field | Data Type | Transformation/Processing Logic |
|---|---|---|---|
| JSON/Data/ | XMLNSC/PointsRedemptionRes/ |   |   |
| redemptionRefNo | Redemption_Ref_No | String |   |
| lmsReferenceNo | LMS_Reference_No | String |   |
| pointsRedeemed | Points_Redeemed | String |   |
| pointsBalance | Points_Balance | String |   |
| status | Status | String |   |

**OUTPUT (If Failure)**

| API field | LMS field | Transformation/Processing Logic |
|---|---|---|
| JSON/Data | XMLNSC/PointsRedemptionRes/ |   |
| statusCode |   | HTTP status code. Refer section 2.3 |
| statusReason |   | HTTP status. Refer section 2.3 |
| errorCode | Error_Code | OMW Error Code. Refer section 2.2 |
| errorDesc | Error_Desc | OMW Error Desc. Refer section 2.2 |

### 2.2 List of Error Codes & Error Description

| Error Code | Error Description | Remarks |
|---|---|---|
| EAI-LMS-BRK-000 | Success | Service completed |
| EAI-LMS-BRK-001 | Mandatory field missing | Returned with HTTP status 400 |
| EAI-LMS-BRK-002 | Invalid field value or format | Returned with HTTP status 400 |
| EAI-LMS-BRK-003 | Provider time-out | Returned with HTTP status 500 |
| EAI-LMS-BRK-004 | Provider error | Error returned by LMS. The LMS code and description are passed in errorDesc |
| EAI-LMS-BRK-999 | System error | Generic error when no mapping exists |

### 2.3 List of HTTP Status Codes

| Status Code | Status Reason | Usage |
|---|---|---|
| 200 | Success | Request processed |
| 400 | Bad Request | Functional failure for the given input data |
| 401 | Unauthorized | Validate the security details |
| 403 | Forbidden | Client has no permission for the API |
| 404 | Not Found | API endpoint is not available |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Time out from provider |
| 502 | Bad Gateway | Provider not reachable |
| 504 | Gateway Timeout | Gateway timed out |

### 2.4 Volumes Projections

| API Name | Year 1 (per day) | Year 2 (per day) | Year 3 (per day) |
|---|---|---|---|
| LoyaltyPointsInquiryAPI | 20,000 | 30,000 | 45,000 |
| LoyaltyPointsRedemptionAPI | 2,000 | 3,000 | 4,500 |

### 2.5 Assumptions

- The access token is obtained from the existing GetToken API. The scope LOYALTY is created in API Connect.
- LMS exposes PointsInquiry and PointsRedemption as XML over HTTPS. For the pilot, LMS is simulated by a mock service.
- Both APIs are plain one-to-one field mappings, JSON to XML on the request and XML to JSON on the response. No enrichment logic is required.
- Consumers and provider are internal, so the APIs are published in the Internal API Gateway under the Internal Organization.
