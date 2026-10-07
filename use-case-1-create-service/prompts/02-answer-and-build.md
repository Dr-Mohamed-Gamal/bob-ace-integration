# Prompt 2 — Answer and build

Send after reading the plan. This decisions block answered every question Bob asked in the trial runs of 6–7 October; change a decision here if the lead decides otherwise. Replace <author> and <date>. In the Bob Shell terminal, paste it as one line: Enter sends the message.

```text
Answers and decisions:
- Framework: there is no framework in this workspace. Handle errors inline in the ESQL, write no new libraries, mark each plug-in point with `TODO framework`, and leave out CATALOG on THROW USER EXCEPTION.
- Nearest service: follow skills/shared/ExampleAPI in the ace-flowpilot skill (same project files, natures and structure). No broker schema: files in the project root, like ExampleAPI.
- LMS URL: the user-defined property is `LMS_URL`, default http://lms.todo.invalid/PointsInquiry. Plain HTTP for now, no TLS profile.
- Paths: base path `/loyalty/v1` in both the ACE REST API and API Connect, operation path `/loyalty-points-inquiry`.
- API Connect: files in `apic/`. The invoke calls ACE (not LMS) through the catalog property `omw-loyalty-url`. One product `LoyaltyRewards`, containing only LoyaltyPointsInquiryAPI for now; the redemption API joins it later. Pipeline values and org, gateway and catalog names as `TODO_` placeholders.
- Author: <author>. Today is <date>. A new service has no change comments.
- Headers: send no extra headers or credentials to LMS; the SRS names none. Generate X-TRACKING-ID as a UUID in OMW and return it as a response header.
- Validation: reject a missing mandatory field with EAI-LMS-BRK-001 and an invalid programCode with EAI-LMS-BRK-002, both HTTP 400, without calling LMS. An optional field sent as an empty string counts as not present.
- Subflow layout: one Compute node per step (request mapping, response mapping, error handling), each with its own ESQL module (ESQL-01), and an HTTP Request node that calls LMS.
Build only LoyaltyPointsInquiryAPI now and do not write the Interface Definition Document yet. Record these decisions in `docs/decisions.md`. Run both checks in IBM-04 until they pass. Go ahead and build it as planned.
```
