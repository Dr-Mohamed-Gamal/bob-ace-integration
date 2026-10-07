# Use Case 6 — Review the Service

Prompts that review the service against the requirement and the team's standards in a fresh context, let a person decide which findings to accept, and have Bob fix them. The same review runs again after the change of use case 2.

> Pilot use case for a bank's integration team. The review reports are not published here.

## The Prompts

| # | Prompt | What Bob does |
|---|---|---|
| 4 | [Review in a fresh context](prompts/04-review.md) | Starts a subagent that never saw the build. It reads `docs/decisions.md`, re-reads every file, maps every requirement row to a code line, traces every literal value to the requirement, the prompt or the rules, compares status and error codes, reruns the Toolkit check, and reports each finding as rule id, file and line, what is wrong, the fix. Changes no file |
| 5 | [Fix the accepted findings](prompts/05-fix-accepted-findings.md) | Fixes the findings a person accepted, records the decisions on the others, reruns both checks and updates the document |
| 7 | [Review the change](prompts/07-review-change.md) | The same review, on the change of use case 2 |

## What the Runs Showed

| Review | Findings | Notes |
|---|---|---|
| Same context, two runs | 0 and 0 | Both missed real defects, including missing status codes and an invented message catalog |
| Fresh subagent, night run | 9, 8 real | Included a typo in a JSON schema key that the audit script had missed |
| Fresh subagent, rehearsal | 12, 7 real | Two runtime bugs the Toolkit check had passed: a user-defined property used without being declared, and a validation error that still called the back end. Two false alarms: "no framework" was the lead's decision, which the reviewer could not see |
| Fresh subagent on the change, rehearsal | 4, all real | The decisions file removed the false alarms. Found: document file name not renamed to the new version, API version not raised in either API definition, a success example without the new field |

A review in the same context approves its own work. A fresh reviewer needs the decisions. Both lessons are now rules (IBM-09, IBM-11 and IBM-12 in [RULES/ibm-working-method.md](../RULES/ibm-working-method.md)).
