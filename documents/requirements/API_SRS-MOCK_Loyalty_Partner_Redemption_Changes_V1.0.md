# MOCK DATA – Online Middleware

**Loyalty Partner Redemption Changes**

- File Name: API_SRS-MOCK_Loyalty_Partner_Redemption_Changes_V1.0.docx
- Author: IBM Client Engineering (mock)
- Version: 1.0
- Creation Date: 02 Oct 2026
- Release Date: 02 Oct 2026
- Released By: IBM Client Engineering (mock)
- Reviewed By: To be reviewed by the Online Middleware team
- Requirement Ref.: URF-90001 (mock)

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
  - 2.2 Volumes Projections
  - 2.3 Error Response Registry
  - 2.4 Assumptions

## 1 Introduction

### 1.1 Purpose

This document is to explain the Integration requirements specifications for changes part of the Loyalty partner redemption changes.

### 1.2 Business Requirement

As part of the co-brand partner programme, OMW to accommodate mapping changes in the existing loyalty related services.

**Business Scope:** Effective **01 January 2027**, co-brand partners require the partner code on loyalty inquiries and the channel and country on redemptions.

**Functionalities :** The partner code is sent to LMS for co-brand programmes only. The country code is taken from the request when the channel sends it, otherwise from the organisation of the caller.

**Benefits :**

- Partners receive correct settlement data for redemptions.
- Customers see the points that are about to expire.

**Overall :** Modifications in the existing APIs at OMW to accommodate the above requested changes.

### 1.3 Project Scope

#### 1.3.1 In Scope

As part of the loyalty journey, online middleware team will make mapping changes in the existing Rest APIs.

| S.No | Method | RestAPI | Operation Name | Provider | Product |
|---|---|---|---|---|---|
| 1 | POST | LoyaltyPointsInquiryAPI | /loyalty-points-inquiry | LMS | Loyalty |
| 2 | POST | LoyaltyPointsRedemptionAPI | /loyalty-points-redemption | LMS | Loyalty |

#### 1.3.2 Out of Scope

Any other requirements which is not mentioned in the scope.

## 2 Project Requirements

### 2.1 Functional Requirements

#### 2.1.1 LoyaltyPointsInquiryAPI

- **Requirement Serial No.** R-01 · **Name** OMW-Interface-LoyaltyPointsInquiryAPI
- **Unique Req. Ref. No.** OMW-001 · **Priority** High

**Change Info** – Introduce new optional fields to filter the inquiry by partner and to return the points that expire soon.

OperationName: loyalty-points-inquiry(POST)

**API Details:**

- API Name: **LoyaltyPointsInquiryAPI**
- Data Format : **Application/JSON**
- Method : **POST**
- OAuth Scope Name: **LOYALTY**

**Backend API Details:**

- Application: **LMS**
- Service Name: **LMSPointsService**
- ServiceOperation: **PointsInquiry**

**Input Data**

| OMW Field | Core Field | Data Type | Description |
|---|---|---|---|
| JSON/Data | XMLNSC/PointsInquiryReq/ | Object |   |
| partnerCode | Partner_Code | String | New optional field to map the co-brand partner code. This field will be mapped to LMS only if programCode = 'COBRAND'. For any other programCode it is not sent to LMS. |
| includeExpiring | Include_Expiring | String | New optional field. Allowed values 'Y' and 'N'. Defaulted to 'N' when it is not present in the request. |

**Output Data**

| OMW Field | Core Field | Data Type | Description |
|---|---|---|---|
| JSON/Data | XMLNSC/PointsInquiryRes/ | Object |   |
| pointsExpiringNext30Days | Points_Expiring_30D | String | New optional field to return the points expiring in the next 30 days. Returned only when it is present in the LMS response. |

#### 2.1.2 LoyaltyPointsRedemptionAPI

- **Requirement Serial No.** R-02 · **Name** OMW-Interface-LoyaltyPointsRedemptionAPI
- **Unique Req. Ref. No.** OMW-002 · **Priority** High

**Change Info** – Introduce new fields to map the redemption channel and the country code to LMS.

OperationName: loyalty-points-redemption(POST)

**API Details:**

- API Name: **LoyaltyPointsRedemptionAPI**
- Data Format : **Application/JSON**
- Method : **POST**
- OAuth Scope Name: **LOYALTY**

**Backend API Details:**

- Application: **LMS**
- Service Name: **LMSPointsService**
- ServiceOperation: **PointsRedemption**

**Input Data**

| OMW Field | Core Field | Data Type | Description |
|---|---|---|---|
| JSON/Data | XMLNSC/PointsRedemptionReq/ | Object |   |
| channelCode | Channel_Code | String | New optional field to map the redemption channel. |
| countryCode | Country_Code | String | New optional field to map the two-character ISO country code. When it is not present in the request, it is defaulted from the X-ORG-ID header. |
| N/A | Credit_Currency | String | This field is not required to be mapped by OMW, as LMS derives the currency from the credit account. It is an optional field and is defaulted at LMS when not present in the OMW-LMS request. |

There is no change in the output of this API.

### 2.2 Volumes Projections

No change in the volumes of the existing APIs.

### 2.3 Error Response Registry

No change. The existing error codes and HTTP status codes of both APIs apply.

### 2.4 Assumptions

- All new fields are optional. Existing consumers that do not send them are not affected.
- The existing mandatory validations and the existing conditions on other fields remain the same.
- The API definitions (Swagger) of both APIs are updated with the new fields.
- The Interface Definition Document of each service is updated with the new fields.
