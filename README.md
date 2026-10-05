# IBM Bob on App Connect Enterprise — Pilot Use Cases

Four pilot use cases for a bank's integration team, run with **IBM Bob Shell** inside the **IBM App Connect Enterprise (ACE) Toolkit**: create a REST service on ACE and API Connect from a requirement document, write its Interface Definition Document, review it against the team's standards, and apply a change requirement. Seven prompts in one chat, steered by a standards rules file and IBM's ACE skills, and checked at every step by the ACE Toolkit's own validation.

> The bank's documents, code and the reports made from them are not published here. The runs used mock requirement documents prepared for the pilot. This repository describes the inputs and why each is used, the method, every prompt as sent, and what the runs showed.

Page: [index.html](index.html) (GitHub Pages).

## Use Cases

| # | Use case | What Bob does | Prompts | Clean rehearsal, 5 Oct 2026 |
|---|---|---|---|---|
| **1** | [Create a service](use-case-1-create-service/) | Plans the service, asks what the requirement leaves open, builds the API Connect API and product and the ACE REST API project, and runs the Toolkit check until it passes | 2 | Toolkit check passed first time; all fields and status codes; no invented values · 6.3 Bobcoins |
| **3** | [Document it](use-case-3-interface-document/) | Writes the Interface Definition Document in the team's template from the code as built | 1 | All sections and fields; matches the code · 0.9 Bobcoins |
| **6** | [Review it](use-case-6-review/) | Reviews in a fresh-context subagent against the requirement and the rules; a person accepts findings; Bob fixes them | 2 (+1 after the change) | 12 findings, 7 real, incl. 2 runtime bugs the Toolkit check passed · 10.0 Bobcoins with fixes |
| **2** | [Change it](use-case-2-change/) | Applies a change requirement: new fields with conditions and defaults, dated change comments, both API definitions, the document's version | 1 | All gates passed · 6.7 Bobcoins |

The numbers follow the team's list of use cases. Use cases 4 (troubleshooting) and 5 (root-cause analysis) were parked for a later phase. Total for the rehearsal: 23.8 Bobcoins.

## How Bob Is Steered

| Part | What it does |
|---|---|
| **The bank's standards** in `.bob/rules/` ([RULES/client-standards.md](RULES/client-standards.md)) | 79 numbered rules: how to work, requirement conformance, ESQL, API Connect, the Interface Definition Document, and how to review. Every review finding cites a rule id |
| **IBM's working method** in `.bob/rules/` ([RULES/ibm-working-method.md](RULES/ibm-working-method.md)) | 12 rules, IBM-01 to IBM-12: placeholders instead of invented values, the Toolkit check, the decisions file, the Interface Definition Document as Word, how a review is run. Kept apart from the bank's standards so the bank can see which is which |
| **IBM's ACE skills** | The ACE Toolkit adds IBM's open-source `ace-flowpilot` skills to the workspace. They give Bob the exact project files, node types and ESQL patterns ACE expects |
| **A Toolkit check** ([tools/toolkit_check.py](tools/toolkit_check.py)) | Runs the Toolkit's own build and validators headless (`mqsicreatebar -cleanBuild` on a copy) and prints the Toolkit's problem markers. Bob runs it before calling an ACE project done (rule IBM-04) |
| **A decisions file** | Bob records the lead's decisions in `docs/decisions.md` (rule IBM-09), so later steps and reviewers can see them |
| **Fresh-context reviews** | The review prompt asks for a subagent: a second Bob that never saw the build, reads the files as they are and reruns the checks |

Bob Shell starts inside the Toolkit through a Local Terminal entry that runs [tools/bob-shell-toolkit.sh](tools/bob-shell-toolkit.sh).

## The Seven Prompts

| # | Use case | Prompt |
|---|---|---|
| 1 | 1 · plan | Read `requirements/API-SRS-Project_MOCK_Loyalty_Rewards-V1.0.md`. Tell me how you will build LoyaltyPointsInquiryAPI: which layer each part goes in, the files you will create, and any question you have. Do not create anything yet. |
| 2 | 1 · build | The decisions block in [use case 1](use-case-1-create-service/prompts/02-answer-and-build.md), ending "Go ahead and build it as planned." |
| 3 | 3 · document | Write the Interface Definition Document for the service you just built, as a Word file. Follow `templates/EAI_Interface_Definition_Document_TEMPLATE.docx`. Today is `<date>`. |
| 4 | 6 · review | Review what you built against the standards, using a subagent with a fresh context. Do not change any file. |
| 5 | 6 · fix | Fix findings `<accepted>`. `<others>` are by design: `<why>`. Record these decisions and the ones I gave you before in `docs/decisions.md`. Then run the Toolkit check, and update the Interface Definition Document where the behaviour it describes has changed. |
| 6 | 2 · change | Read `requirements/API_SRS-MOCK_Loyalty_Partner_Redemption_Changes_V1.0.md` and apply the change for LoyaltyPointsInquiryAPI. The requirement id is URF-90001, the author is `<name>` and the date is `<date>`. |
| 7 | 6 · review the change | Review the URF-90001 change against the change SRS and the standards, using a subagent with a fresh context. Do not change any file. |

## What the Runs Showed

- **Reviews in the same context approve their own work.** Twice a same-context review reported zero findings on code with real defects. With a subagent, the same prompt found eight, then twelve findings, most of them real, including two runtime bugs the Toolkit check passed.
- **Without the decisions, a fresh reviewer reports them as defects.** The decisions file fixed that: the last review found four real gaps and no false alarms.
- **A model guesses values it does not have.** The first build invented hosts on the client's real domain and copied an example requirement id from the rules. Placeholders only (rule IBM-01) stopped it in every later run.
- **The Toolkit is the judge, and Bob cannot see it.** The headless Toolkit check gives Bob the Toolkit's errors; it does not report warnings, so a person still reads the Problems view after each step.
- **A rule can cause a defect.** A rule to move procedures to schema level, without saying they then cannot touch the message trees, led Bob to create seven Toolkit warnings. Both affected rules were corrected after the rehearsal.
- **Tell Bob the date**, or it copies the requirement's date into change comments and documents.

## What Changed in the Rules (6 October)

During the runs each mistake Bob made became a rule, first inside the bank's standards file. On 6 October the additions were split out: the bank's file is back to the version from the scoping session with four corrections (FW-07 example comment, FW-10 REST API project, ESQL-06 correlation names, API-08 status code 404), and IBM's instructions to Bob moved to their own file. The Interface Definition Document went back to Word, the bank's format; the Markdown version used on 5 October was a convenience for checking. Four rules were then adjusted for the bank's real workspace (reuse of existing names, a Toolkit check that also runs on Windows, status codes only on new APIs, FW-10 to be confirmed). Details on the [page](index.html#rules).

## Repository

| Path | What it is |
|---|---|
| [index.html](index.html) | The page |
| [use-case-*/](use-case-1-create-service/) | One folder per use case: README and the prompts |
| [RULES/client-standards.md](RULES/client-standards.md) | The bank's standards, with four corrections from the runs |
| [RULES/ibm-working-method.md](RULES/ibm-working-method.md) | IBM's working method for Bob |
| [tools/](tools/) | The headless Toolkit check and the Bob Shell launcher for the Toolkit terminal |
