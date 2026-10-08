# Prompt 1 — Plan and build

Send first, in a new chat. Replace <author> and <date>. Bob states its plan and the decisions it took at the top of its reply, then builds; every open point is decided from the requirement, the rules (IBM-24 defaults, IBM-25) and the workspace, and recorded in `docs/decisions.md`. Nothing is asked of the developer. Until 7 October this was two prompts: a plan with questions, then a decisions block from the lead; the block became rule IBM-24.

```text
Read `requirements/API-SRS-Project_MOCK_Loyalty_Rewards-V1.0.md`. Plan and build LoyaltyPointsInquiryAPI: first say which layer each part goes in, the files you will create and the decisions you took (IBM-24, IBM-25), then build it. Do not ask me anything: every value comes from the SRS, the rules and the workspace. Author: <author>. Today is <date>. Build only LoyaltyPointsInquiryAPI now and do not write the Interface Definition Document yet. Record the decisions in `docs/decisions.md`. Run both checks in IBM-04 until they pass.
```
