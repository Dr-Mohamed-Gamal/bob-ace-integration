# Prompt 2 — Answer and build

Send after reading the plan. This decisions block answered every question Bob asked in two runs; change a decision here if the lead decides otherwise.

```text
Answers and decisions: no broker schema (files in the project root, like ExampleAPI). There is no framework in this workspace: keep it self-contained, write no new libraries, and mark each plug-in point with `TODO framework`. The user-defined property for the LMS URL is `LMS_URL`. API Connect: base path `/loyalty/v1`, files in `apic/`, calling ACE through the catalog property `omw-loyalty-url`; one product `LoyaltyRewards` (the redemption API joins it later); pipeline values as `TODO_` placeholders. Send no extra headers or credentials to LMS: the SRS names none. Generate X-TRACKING-ID as a UUID in OMW and return it as a response header. Reject an invalid `programCode` with EAI-LMS-BRK-002 and HTTP 400. Build only `LoyaltyPointsInquiryAPI` now and do not write the Interface Definition Document yet. Go ahead and build it as planned.
```
