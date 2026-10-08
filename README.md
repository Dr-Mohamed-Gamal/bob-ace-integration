# IBM Bob on App Connect Enterprise — Pilot Use Cases

Four pilot use cases for a bank's integration team, run with **IBM Bob Shell** inside the **IBM App Connect Enterprise (ACE) Toolkit**: create a REST service on ACE and API Connect from a requirement document, write its Interface Definition Document, review it against the team's standards, and apply a change requirement. Six prompts in one chat, nothing asked of the developer, steered by a standards rules file and IBM's ACE skills, and checked at every step by the ACE Toolkit's own validation.

> The bank's documents, code and the reports made from them are not published here. The runs used mock requirement documents and a mock document template prepared by IBM for the pilot, in the team's layout with invented content; they are in [documents/](documents/). This repository describes the inputs and why each is used, the method, every prompt as sent, and what the runs showed.

Page: [index.html](index.html) (GitHub Pages).

## Use Cases

| # | Use case | What Bob does | Prompts | Clean rehearsal, 5 Oct 2026 |
|---|---|---|---|---|
| **1** | [Create a service](use-case-1-create-service/) | Plans the service, decides what the requirement leaves open from the rules, builds the API Connect API and product and the ACE REST API project, and runs both checks until they pass | Prompt 1 | Toolkit check passed first time; all fields and status codes; open values left as marked placeholders · 6.3 Bobcoins |
| **3** | [Document it](use-case-3-interface-document/) | Writes the Interface Definition Document in the team's template from the code as built | Prompt 2 | All sections and fields; matches the code · 0.9 Bobcoins |
| **6** | [Review it](use-case-6-review/) | Reviews in a fresh-context subagent against the requirement and the rules; a person accepts findings; Bob fixes them | Prompts 3 and 4 (review, then fix), and prompt 6 (review the change after use case 2) | 7 changes accepted and made, incl. 2 runtime fixes · 10.0 Bobcoins with fixes |
| **2** | [Change it](use-case-2-change/) | Applies a change requirement: new fields with conditions and defaults, dated change comments, both API definitions, the document's version | Prompt 5 | All gates passed · 6.7 Bobcoins |

The numbers follow the team's list of use cases. Use cases 4 (troubleshooting) and 5 (root-cause analysis) were parked for a later phase. Total for the rehearsal: 23.8 Bobcoins.

## How Bob Is Steered

| Part | What it does |
|---|---|
| **The bank's standards** in `.bob/rules/` ([RULES/client-standards.md](RULES/client-standards.md)) | 79 numbered rules: how to work, requirement conformance, ESQL, API Connect, the Interface Definition Document, and how to review. Every review finding cites a rule id |
| **IBM's working method** in `.bob/rules/` ([RULES/ibm-working-method.md](RULES/ibm-working-method.md)) | 26 rules, IBM-01 to IBM-26: placeholders instead of invented values, the defaults for what the requirement leaves open and no questions to the developer (IBM-24, IBM-25, since 8 October), the two checks, the test cases Bob writes from the requirement (IBM-26, since 8 October), the decisions file, the Interface Definition Document, how a review is run, and the ACE run-time details each check confirmed (compute mode, user-defined properties, parser domain, error routing, content type, exception numbers). Kept apart from the bank's standards so the bank can see which is which |
| **IBM's ACE skills** | The ACE Toolkit adds IBM's open-source `ace-flowpilot` skills to the workspace. They give Bob the exact project files, node types and ESQL patterns ACE expects |
| **A Toolkit check** ([tools/toolkit_check.py](tools/toolkit_check.py)) | Runs the Toolkit's own build and validators headless (`mqsicreatebar -cleanBuild` on a copy) and prints the Toolkit's problem markers. It also fails when the BAR holds no compiled flow, so a project the Toolkit does not recognise cannot pass |
| **A runtime check** ([tools/runtime_check.py](tools/runtime_check.py)) | Deploys the REST API to a local, throw-away integration server and calls it with the requirement's cases against a mock back end: validation errors, success mapping, back-end error, timeout, and the change's conditions and defaults. It sets the back-end URL as a deploy-time property, so it also proves the URL can be configured. Bob runs both checks before calling an ACE project done (rule IBM-04). Since 8 October it also takes a cases file that Bob writes from the requirement (`--cases`, rule IBM-26, example in [tools/cases-example.json](tools/cases-example.json)), so the cases are no longer hard-coded for one service, and in that mode it fails when the integration server log shows an error during the run |
| **The Interface Definition Document in Markdown** ([tools/md_to_docx.py](tools/md_to_docx.py)) | Bob writes the document in Markdown from the template's `.md` copy; the converter makes the Word file next to it (rule IBM-10) |
| **A decisions file** | Bob records its own decisions and the lead's in `docs/decisions.md` (rules IBM-09, IBM-25), so later steps and reviewers can see them |
| **A Toolkit import handover** ([tools/toolkit_import.py](tools/toolkit_import.py)) | Hands a new project folder to the running Toolkit, which opens its import wizard with the folder filled in; the developer ticks the project and clicks Finish (rule IBM-04, since 8 October). The Toolkit has no silent import |
| **Fresh-context reviews** | The review prompt asks for a subagent: a second Bob that never saw the build, reads the files as they are and reruns the checks |

Bob Shell starts inside the Toolkit through a Local Terminal entry that runs [tools/bob-shell-toolkit.sh](tools/bob-shell-toolkit.sh). The script also sets the terminal size, which the Toolkit's terminal does not report to the programs it runs.

## The Six Prompts

| # | Use case | Prompt |
|---|---|---|
| 1 | 1 · plan and build | Read `requirements/API-SRS-Project_MOCK_Loyalty_Rewards-V1.0.md`. Plan and build LoyaltyPointsInquiryAPI: first say which layer each part goes in, the files you will create and the decisions you took (IBM-24, IBM-25), then build it. Do not ask me anything: every value comes from the SRS, the rules and the workspace. Author: `<author>`. Today is `<date>`. Build only LoyaltyPointsInquiryAPI now and do not write the Interface Definition Document yet. Record the decisions in `docs/decisions.md`. Run both checks in IBM-04 until they pass. |
| 2 | 3 · document | Write the Interface Definition Document for the service you just built, following IBM-10. Today is `<date>`. |
| 3 | 6 · review | Review what you built against the standards, using a subagent with a fresh context. Do not change any file. |
| 4 | 6 · fix | Fix findings `<accepted>`. `<others>` are by design: `<why>`. Record these decisions in `docs/decisions.md`. Then run both checks in IBM-04, and update the Interface Definition Document where the behaviour it describes has changed. |
| 5 | 2 · change | Read `requirements/API_SRS-MOCK_Loyalty_Partner_Redemption_Changes_V1.0.md` and apply the change for LoyaltyPointsInquiryAPI. The requirement id is URF-90001, the author is `<name>` and the date is `<date>`. |
| 6 | 6 · review the change | Review the URF-90001 change against the change SRS and the standards, using a subagent with a fresh context. Do not change any file. |

Until 7 October the flow had seven prompts: a plan that ended with Bob's questions, and a decisions block from the lead that answered them. The block is now rule IBM-24 and rule IBM-25 tells Bob to decide and record instead of asking, so prompt 1 plans and builds in one go. The cost figures below from the 5 to 7 October runs refer to the seven-prompt flow.

## What the Runs Showed

- **Reviews in the same context approve their own work.** Twice a same-context review reported zero findings on code with real defects. With a subagent, the same prompt found eight, then twelve findings, most of them real, including two runtime bugs the Toolkit check passed.
- **Without the decisions, a fresh reviewer reports them as defects.** The decisions file fixed that: the last review found four real gaps and no false alarms.
- **A model guesses values it does not have.** The first build invented hosts on the client's real domain and copied an example requirement id from the rules. Placeholders only (rule IBM-01) stopped it in every later run.
- **The Toolkit is the judge, and Bob cannot see it.** The headless Toolkit check gives Bob the Toolkit's errors; it does not report warnings, so a person still reads the Problems view after each step.
- **A rule can cause a defect.** A rule to move procedures to schema level, without saying they then cannot touch the message trees, led Bob to create seven Toolkit warnings. Both affected rules were corrected after the rehearsal.
- **Tell Bob the date**, or it copies the requirement's date into change comments and documents.

## Trial Runs (6–7 October)

After a colleague's review of this kit, the method was tightened and the whole flow was run five more times, the seven prompts in one chat each:

- **Every run passed both checks and the audits**: the Toolkit check, the runtime check with 7 requirement cases after the build and 13 after the change, and versions raised together. Three runs had no review findings at all; in the other two, the change review found a new field missing from an API example, which rule IBM-23 now covers.
- **One more run inside the ACE Toolkit's own terminal (7 October)**, from a new Toolkit workspace with this repository's rules, tools and prompts, every prompt sent in the "IBM Bob Shell" terminal. Both checks passed at every step (7 of 7 cases after the build, 13 of 13 after the change), and after Project > Clean the Toolkit's Problems view showed no errors and no warnings. The review of the build found two real gaps, the HTTP Request node's failure terminal (IBM-19) and the position of `x-ibm-configuration` in the API Connect file (INV-01), which Bob fixed in prompt 5. The change review found one API Connect request example without the new fields. 22.1 Bobcoins, 53 minutes.
- **A project that builds is not yet a service that works.** Deploying earlier outputs on a local integration server showed issues that neither the build nor a review had shown: a compute mode value, the response parser domain, where errors are caught. The runtime check now runs these cases at every step, and Bob corrects what it reports.
- **Bob fixes from the checks' output.** When the runtime check failed during a build, Bob read the failing case and corrected the code in the same step.
- **A whole run takes about 45 minutes and 17–32 Bobcoins.**

## Six Prompts, No Questions (8 October)

The team asked for two things: that the developer supplies no answers, and that Bob tests the flows itself in an integration server with data taken from the requirement. The first changed the flow: prompt 2's decisions block became rule IBM-24, rule IBM-25 tells Bob to decide from the requirement, the rules and the workspace and to record each decision, and prompt 1 now plans and builds in one go. Prompts 2 to 6 are unchanged. The second is rule IBM-26 and the runtime check's cases-file mode.

The six-prompt flow was run once, headless, in one chat, on a new workspace with the rules of this version:

| Prompt | Result | Bobcoins |
|---|---|---|
| 1 plan and build | No questions. Nine decisions stated and recorded. Toolkit check passed, runtime check 7 of 7, audit passed, first pass | 4.5 |
| 2 document | Markdown and Word, v1.0 | 1.7 |
| 3 review | Three findings: the client-id header name in the API Connect file, the error code in the 502 examples, and a back-end status header read on the error path (by design). No file changed | 2.7 |
| 4 fix | Two fixed, one recorded as a decision. Toolkit check passed | 3.6 |
| 5 change | All three fields; Toolkit check passed, runtime check 13 of 13, audit passed, versions aligned | 6.9 |
| 6 review the change | No findings. No file changed | 2.6 |

23.4 Bobcoins in 50 minutes of Bob time. Rule IBM-26 was then tried in a fresh chat on the same workspace: Bob read both requirement documents, wrote 15 cases (two more than the hand-written set: a second missing mandatory field, and a value outside the allowed list for the new field) and passed 15 of 15 with a clean integration-server log on its first run, 0.9 Bobcoins. The first attempt at prompt 3 ended in a "Request Failed" error from Bob's service after the review subagent had finished; the same prompt sent again in the same chat completed. That retry is the only error of the run.

Also on 8 October: the import handover ([tools/toolkit_import.py](tools/toolkit_import.py)) was confirmed on macOS, where handing a project folder to the running Toolkit opened "Import Projects from File System or Archive" with the folder filled in; the Windows launcher's `--launcher.openFile` relay is still to be tried on a bank laptop. The Toolkit has no silent import and no Bob plugin, and IBM's own ACE skill tells the developer to use File > Import.

## What Changed in the Rules (6 October)

During the runs each mistake Bob made became a rule, first inside the bank's standards file. On 6 October the additions were split out: the bank's file is back to the version from the scoping session with four corrections (FW-07 example comment, FW-10 REST API project, ESQL-06 correlation names, API-08 status code 404), and IBM's instructions to Bob moved to their own file. The Interface Definition Document went back to Word, the bank's format; the Markdown version used on 5 October was a convenience for checking. Four rules were then adjusted for the bank's real workspace (reuse of existing names, a Toolkit check that also runs on Windows, status codes only on new APIs, FW-10 to be confirmed). Details on the [page](index.html#rules).

## What Changed on 7 October

- **IBM-13 to IBM-17** (from the colleague's review): the exact compute mode for LocalEnvironment changes, reading a user-defined property through an `EXTERNAL` variable, ESQL functions without parentheses, no `Data` wrapper in the payload, and every version raised together. Review checks 6–9 were added to IBM-12.
- **IBM-18 to IBM-21**, each confirmed on an integration server: the XML parser domain on the HTTP Request node, error routing around the TryCatch node, the JSON content type on replies, and the exception numbers for a back-end timeout. IBM-14 now shows the exact flow XML for the property.
- **IBM-22** keeps a plan short; **IBM-23** adds a changed field to every example as well as the schema.
- **IBM-10**: the Interface Definition Document is written in Markdown and converted to Word, instead of edited in Word directly.
- **The Toolkit check** fails on a BAR with no compiled flow; **the runtime check** is new.
- **A `.bobignore` file** in the workspace with the two lines `.github/` and `.metadata/` keeps Bob from reading the Toolkit's second copy of the skills and its metadata.
- **The Bob Shell launcher** sets the terminal size (`COLUMNS`, `LINES`), which the Toolkit's terminal does not report. With it, the whole flow runs in the Toolkit's terminal.

## The Colleague's Kit: Issues Found and How This Version Handles Them

The colleague's kit was run the same way: its sample output deployed on a local integration server and called with the requirement's cases. It started and passed 11 of 13 cases; with the four fixes below it passed 13 of 13. Every item was checked on the integration server or the Toolkit, not only by reading.

| Found in the colleague's kit | Evidence | In this version |
|---|---|---|
| The back-end URL is read through an `EXTERNAL` variable, but the property is not defined on the subflow, so no deploy can change it: every call goes to the placeholder URL | The BAR lists no `LMS_URL` property; a deploy-time override of the HTTP Request node's URL is ignored, because the ESQL sets the placeholder URL | IBM-14 shows the exact flow XML for the property and the override key; the runtime check fails when the property is missing |
| JSON replies go out with `Content-Type: text/xml`, copied from the back end's reply | 9 of 13 runtime replies | IBM-20; the runtime check tests every reply |
| A back-end timeout returns EAI-LMS-BRK-999 instead of EAI-LMS-BRK-003: the code looks for BIP3165 and the text `Timeout`, while ACE reports BIP3151 "A timeout occurred…" | The exception list printed on the integration server: BIP3162 › BIP3152 › BIP3151 | IBM-21 with a tested exception-list loop; the runtime check has a timeout case |
| The decisions file records the BIP3165 check as correct by design, overruling a reviewer who had questioned it | Same evidence as above | A decision about behaviour is checked by the runtime check, not by agreement |
| An empty optional field (`includeExpiring`) is sent to the back end as an empty value instead of the default `N` | The mock back end received `<Include_Expiring></Include_Expiring>` | Prompt 2 decides it: an empty optional field counts as not present; the runtime check has the case |
| The published sample output is from the first run, before the kit's final rules | Its document is at version 1.2 while the API is at 1.1.0 | Outputs are judged by the checks at each step, not by a stored sample |
| The setup copies an MCP configuration with a fixed local port (`60164`) into every workspace | The port belongs to one machine's Bob session; another machine uses a different one | Not adopted: Bob writes its own MCP configuration |
| The setup script needs zsh and looks for the skills in `.bob/ace-flowpilot`; the Toolkit 13.0.9 installs them in `.bob/skills/ace-flowpilot` and `.github/skills/ace-flowpilot`, so the script downloads a second copy from GitHub | Checked on a new Toolkit workspace | Not adopted: the Toolkit installs the skills, and `.bobignore` hides the second copy from Bob |
| A new chat for each step after the build, because Bob stopped replying at about 168k tokens | The stall followed a step that filled the chat with tool output; the one-chat rehearsal reached 202k tokens and finished, and the five trial runs used one chat each | Kept one chat; IBM-10 removed the step that filled the chat |
| After the change, the API is at 1.1.0 while the product stays at 1.0.0 with `CHANGETYPE=NEW` | Product file and properties | An open question for the bank: how its pipeline expects a changed API |

The colleague's points about this kit were right on four counts, and those changes are listed under "What Changed on 7 October": the empty-BAR guard, the Markdown route for the document, IBM-13 to IBM-17, and review checks 6–9.

## Running It Yourself

What you need: IBM App Connect Enterprise 13 with its Toolkit (13.0.9 was used), IBM Bob Shell 2.0.x, Python 3 with `python-docx` (for the Word document), The two mock requirement documents and the Interface Definition Document template are in [documents/](documents/).

1. Clone this repository and run `python3 tools/new_workspace.py`. It creates `bob-workspace/` next to `tools/` with the two rules files in `.bob/rules/`, the `.bobignore` file and the empty folders, and lists the files still to add.
2. The script has copied the requirement documents and the template from `documents/` into the workspace. `bob-workspace/` is in `.gitignore`, so what Bob builds there never leaves your machine.
3. Open the ACE Toolkit on `bob-workspace` as the workspace. It installs IBM's ace-flowpilot skill into `.bob/skills/` itself.
4. In the Toolkit, Settings > Terminal > Local Terminal, add an entry "IBM Bob Shell" that runs `tools/bob-shell-toolkit.sh` with the workspace as the working directory. The script reads the API key from `~/.bob/bob_api_key` and sets the terminal size the Toolkit does not report. On Windows, start Bob Shell in a terminal next to the Toolkit instead.
5. Window > Show View > Terminal, open an "IBM Bob Shell" terminal, Agent mode, one chat, and send the six prompts in order from the use-case folders, each pasted as one line with `<author>` and `<date>` filled in. Prompt 4 is written from the review's findings in the shape the use-case-6 folder shows.
6. Approve the checks when Bob asks (`arch -arm64 /usr/bin/python3 ../tools/…` on Apple silicon). After each step, run `python3 ../tools/toolkit_import.py bob-workspace/<project>` once, or File > Import, and read the Problems view.

What to expect, from the 8 October run: no question from Bob, both checks green after prompt 1 (7 cases) and after prompt 5 (13 cases, or 15 with the cases file), three findings in the first review and none in the second, about 25 Bobcoins for the six prompts. Rule IBM-26 (the cases file) was tested in its own chat on 8 October; its place inside prompts 1 and 5 has not yet been run as one flow, so the first full run of this version is also that test: if Bob skips the cases file, send "Write the test cases from the SRS following IBM-26 and run the runtime check with them" as an extra message.

## Repository

| Path | What it is |
|---|---|
| [index.html](index.html) | The page |
| [use-case-*/](use-case-1-create-service/) | One folder per use case: README and the prompts |
| [documents/](documents/) | The mock requirement documents (new service, change) and the Interface Definition Document template, Markdown and Word |
| [RULES/client-standards.md](RULES/client-standards.md) | The bank's standards, with four corrections from the runs |
| [RULES/ibm-working-method.md](RULES/ibm-working-method.md) | IBM's working method for Bob |
| [tools/](tools/) | The workspace setup script, the Toolkit check, the runtime check with its example cases file, the Toolkit import handover, the Markdown-to-Word converter and the Bob Shell launcher for the Toolkit terminal |
| `bob-workspace/` | Your workspace, created by the setup script; holds the unpublished documents; ignored by git |
