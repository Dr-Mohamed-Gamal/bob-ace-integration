# IBM working method for Bob in this workspace

These are IBM's instructions to Bob, not the client's standards. They say how Bob works here: what to do
when a value is unknown, how to check an ACE project, where decisions are kept and how a review is
run. Each one answers a mistake Bob made in the pilot dry runs of 5 and 6 October 2026. The client's
standards are in [`client-standards.md`](client-standards.md); when the two disagree, follow the client's standards and record it in `docs/decisions.md`.

## Values and fields

- **IBM-01** Never invent a value: no hostnames, URLs, domains, requirement ids, catalog or space
  names, queue names, field names or credentials that are not in the SRS, the prompt or the existing
  code in the workspace. Reuse the names the workspace already uses (FW-04). Where a value is needed
  and none of these has it, use a placeholder: a property value `TODO_<NAME>`, or a URL on the
  reserved `.invalid` domain, for example `http://lms.todo.invalid/PointsInquiry`. Never put the
  client's domain in a value. List every placeholder in your final summary. Fixed product values
  are not invented values: for example the API Connect gateway type `datapower-api-gateway`.
  *(Dry run: Bob put three invented hosts on the client's real domain into the code.)*
- **IBM-02** Read and write only the fields and headers the SRS names, on the channel side and on
  the back-end side (FW-01). If the design seems to need another one, do not add it; record the gap in `docs/decisions.md`.
  *(Dry run: Bob read a back-end field the SRS never mentions.)*
- **IBM-03** Take dates from the prompt. If the prompt gives none, run `date`. Never copy a date
  from the SRS into a change comment or a document.
  *(Dry run: every change comment carried the SRS date.)*

- **IBM-24** Defaults for this workspace, applied when the SRS and the workspace give nothing better.
  Each one was agreed with the lead in the trial runs of 6 and 7 October 2026:
  - Framework: there is no framework in this workspace. Handle errors inline in the ESQL, write no new
    libraries, mark each plug-in point with `TODO framework`, and leave out CATALOG on THROW USER EXCEPTION.
  - Nearest service: follow `skills/shared/ExampleAPI` in the ace-flowpilot skill (same project files,
    natures and structure). No broker schema: files in the project root, like ExampleAPI.
  - Back-end URL: one user-defined property per back end named `<BACKEND>_URL` (for LMS: `LMS_URL`), default
    `http://<backend>.todo.invalid/<ServiceOperation>`, for LMS `http://lms.todo.invalid/PointsInquiry`
    (IBM-01, IBM-14). Plain HTTP, no TLS profile.
  - Paths: base path `/<domain>/v1` from the SRS project name (Loyalty: `/loyalty/v1`) in both the ACE REST API
    and API Connect; the operation path is the SRS "API Path".
  - API Connect: files in `apic/`. The invoke calls ACE (not the back end) through the catalog property
    `omw-<domain>-url` (Loyalty: `omw-loyalty-url`). One product per SRS project, named after it
    (`LoyaltyRewards`), containing only the APIs built so far. Pipeline values and org, gateway and catalog
    names as `TODO_` placeholders.
  - A new service has no change comments. Author and date come from the prompt (IBM-03).
  - Headers: send no extra headers or credentials to the back end unless the SRS names them. Generate
    `X-TRACKING-ID` as a UUID in OMW and return it as a response header (SRS header 6, populated by Middleware).
  - Validation: reject a missing mandatory field with the SRS "Mandatory field missing" code and a value outside
    the SRS allowed values with the "Invalid field value" code, both HTTP 400, without calling the back end
    (for this SRS: EAI-LMS-BRK-001 and EAI-LMS-BRK-002). An optional field sent as an empty string counts as
    not present.
  - Subflow layout: one Compute node per step (request mapping, response mapping, error handling), each with
    its own ESQL module (ESQL-01), and an HTTP Request node that calls the back end.
- **IBM-25** Do not ask the developer questions and do not stop to wait for answers. Decide every open point
  from the SRS, these rules, the client's standards and the workspace, in that order; where none of them has
  the value, apply IBM-24 or a placeholder (IBM-01). Write each decision in `docs/decisions.md` (IBM-09) with
  the date and its source, then continue. State the decisions at the top of your reply.
  *(Trial runs 6 and 7 October: the five questions Bob asked were all answerable from the SRS and these rules.
  Trial run 8 October with this rule: no questions, both checks passed, 4.5 Bobcoins for plan and build.)*

- **IBM-22** When asked for a plan, keep it short: the layer for each part, one line per file you will
  create, and the decisions you took under IBM-24 and IBM-25. No code, no file contents. Read only what the plan needs: the SRS, the
  rules and the skill's `ExampleAPI`.
  *(Toolkit run 6 Oct: Bob read the whole workspace for the plan and ran out of response length.)*

## Checking an ACE project

- **IBM-04** An ACE project is done only when the ACE Toolkit shows no errors and no warnings for
  it. If `tools/toolkit_check.py` is in the repository, run
  `python3 ../tools/toolkit_check.py <project folder>` from the workspace (Windows, macOS or Linux):
  it runs the Toolkit's own build and validators on a copy, about a minute. Fix every problem it
  reports and run it again. On macOS, if `python3` fails with an `xcrun` architecture error (the
  Toolkit terminal runs as x86_64 on Apple silicon), run `arch -arm64 /usr/bin/python3 ../tools/toolkit_check.py
  <project folder>` instead. If the check is not available or cannot find ACE, say so and ask the
  developer to refresh the project in the Toolkit and paste the Problems view. The check reports
  errors only, so also avoid the warnings listed in IBM-05 to IBM-08. A Toolkit warning that a
  correlation name (`OutputRoot`, `OutputLocalEnvironment`, `InputRoot`…) "cannot be resolved" is an
  error in practice: the integration server refuses to deploy the project.
  When the Toolkit check passes, run `python3 ../tools/runtime_check.py <project folder>` (add `--change`
  after a change requirement). It deploys the project to a local integration server and calls it with
  the SRS cases against a mock LMS, about a minute. Fix every failure it reports and run both checks
  again. The runtime check runs twice: with its built-in cases when the project is the pilot's
  LoyaltyPointsInquiryAPI, and always with the cases file you wrote from the SRS (IBM-26). The project
  is done only when every check passes.
  When both pass, run `python3 ../tools/toolkit_import.py <project folder>` once for a new project: it hands
  the folder to the running Toolkit, which opens its import wizard with the folder filled in; the developer
  ticks the project and clicks Finish. Say so in your summary.
  *(Dry run: Bob's first ACE project compiled but would not open in the Toolkit. Runtime test 6 Oct:
  a project that passed the Toolkit check did not deploy, and another passed 1 of 13 SRS cases.)*
- **IBM-05** Each ACE project has `.settings/org.eclipse.core.resources.prefs` with exactly
  `eclipse.preferences.version=1` and `encoding/<project>=UTF-8`, where `<project>` is literal text,
  not the project name.
- **IBM-06** HTTP Request node: the "Web service URL" property is mandatory. Set it to a placeholder
  on the `.invalid` domain (IBM-01) and set the real URL at run time in the Compute node before it:
  `OutputLocalEnvironment.Destination.HTTP.RequestURL` from the user-defined property (IBM-14).
- **IBM-07** In ESQL, `BROKER SCHEMA a.b.c` has no semicolon. A message flow's `nsURI` and
  `nsPrefix` match its path in the project.
- **IBM-08** `THROW USER EXCEPTION` uses the framework's message catalog. When there is no
  framework, leave out `CATALOG` so ACE uses its default; never invent or placeholder a catalog name.

## Run-time behaviour (the runtime check tests these)

- **IBM-26** Before the runtime check, write the service's test cases from the SRS into
  `tests/<project>.cases.json`, in the format described at the top of `tools/runtime_check.py` (`--cases`;
  `tools/cases-example.json` is a complete example). Cover: the success path with every output field and
  every input field sent to the back end; one case per error code in the SRS error list that the service
  can produce; one per mandatory field missing; one per field with allowed values, sent with a value
  outside them; the back-end timeout (a `delay` longer than 3 seconds) and a back-end HTTP error; and,
  after a change requirement, one case per condition and default it adds (a field sent and not sent to the
  back end, a default applied when the field is absent and when it is empty, an output field present and
  absent). Take every value from the SRS tables and invent none; do not ask (IBM-25). Then run
  `python3 ../tools/runtime_check.py <project folder> --cases tests/<project>.cases.json` and fix the
  service, or the case where it misread the SRS, until every case passes and the integration server log
  shows no error message. Keep the file: the change step extends it.

- **IBM-13** A Compute node whose ESQL writes `OutputLocalEnvironment` (for example
  `Destination.HTTP.RequestURL`, `Destination.HTTP.ReplyStatusCode` or variables) has
  `computeMode="destinationAndMessage"` in the flow file (ESQL-08). The default, `message`, drops
  every LocalEnvironment change. Use `all` only when the node also writes the ExceptionList. The
  attribute takes exactly one of `message`, `destination`, `destinationAndMessage`, `exception`,
  `exceptionAndMessage`, `exceptionAndDestination`, `all`; any other value builds and acts as `message`.
  *(Test runs 6 Oct: the LMS URL, the reply status and the tracking id were set but never propagated,
  once with the default and once with `LocalEnvironmentAndMessage`.)*
- **IBM-14** Read a user-defined property only through an ESQL `EXTERNAL` variable declared at module
  level, for example `DECLARE LMS_URL EXTERNAL CHARACTER 'http://lms.todo.invalid/PointsInquiry';`,
  and define the same property on the subflow that contains the Compute node, or no deploy can set it.
  In the `.subflow`, directly after `<eSuperTypes …/>`:
  ```xml
  <eStructuralFeatures xmi:type="ecore:EAttribute" xmi:id="Property.LMS_URL" name="LMS_URL" defaultValueLiteral="http://lms.todo.invalid/PointsInquiry">
    <eType xmi:type="ecore:EDataType" href="http://www.eclipse.org/emf/2002/Ecore#//EString"/>
  </eStructuralFeatures>
  ```
  and inside `<propertyOrganizer>` (`bundleName` is the subflow name, `pluginId` the project name):
  ```xml
  <propertyDescriptor groupName="Group.Basic" configurable="true" userDefined="true" describedAttribute="Property.LMS_URL">
    <propertyName xmi:type="utility:TranslatableString" key="Property.LMS_URL" bundleName="<subflow>" pluginId="<project>"/>
  </propertyDescriptor>
  ```
  Never read it as `Properties.<NAME>`: that is the message's Properties folder.
  *(Test runs 6 Oct: `Properties.LMS_URL` compiled and would have sent an empty URL; two other
  projects declared the variable but not the property, so the URL could never be changed.)*
- **IBM-15** ESQL functions that take no argument are written without parentheses:
  `UUIDASCHAR`, `CURRENT_TIMESTAMP`, `CURRENT_DATE`. `UUIDASCHAR()` is a syntax error.
  *(Test run 6 Oct: the Toolkit check failed on `UUIDASCHAR()`.)*

- **IBM-16** In the SRS field tables, `JSON/Data/` is ACE's JSON message root (`InputRoot.JSON.Data`,
  `OutputRoot.JSON.Data`), not a field. The fields sit directly under it: `InputRoot.JSON.Data.cifNumber`.
  The JSON payload has no `Data` wrapper object, in the ESQL, in `openapi.json` and in the API Connect
  definition.
  *(Test run 6 Oct: Bob wrapped every request and response in `{"Data": {...}}`; real channel
  requests would all have failed with EAI-LMS-BRK-001.)*

- **IBM-17** A change raises every version together (API-05, DOC-01): `info.version` in `openapi.json`
  and in the API Connect definition, to the same value; the Interface Definition Document's header
  `Version`, a new Version History row with that version, and its file name
  (`..._v<x.y>.md` and `.docx`, with the old files removed). One change, one version step.
  APIs use three parts and the document uses two: API `1.1.0` and document `1.1` are the same step and
  match.
  *(Test run 6 Oct: the API Connect definition went to 1.1.0, openapi.json stayed 1.0.0, and the
  document said 1.1 in its header, 1.2 in its history and v1.0 in its file name.)*

- **IBM-23** A change that adds a field updates, in the same step: the request or response schema **and
  every example of that message** (request examples and the 200 example), in `openapi.json` and in the
  API Connect definition; the Interface Definition Document's Data Exchange table; and the versions
  (IBM-17). Before you finish a change, list each new field and the files and lines where it now
  appears.
  *(Trial runs 6 Oct: three of four changes left a new field out of an example.)*

- **IBM-18** An HTTP Request node that calls an XML back end has `messageDomainProperty="XMLNSC"`.
  Without it the reply is parsed as BLOB and `InputRoot.XMLNSC` is empty.
  *(Runtime test 6 Oct: every success reply was `{}`.)*
- **IBM-19** A TryCatch node catches only what fails downstream of its `try` terminal. A Compute node
  that validates the request before the back-end call sends its error reply itself, through a second
  terminal (`PROPAGATE TO TERMINAL 'out1'` wired to the subflow output), instead of throwing. Wire the
  HTTP Request node's `error` and `failure` terminals to the error-handling Compute node. Keep values
  the error path needs, such as the tracking id, in `Environment.Variables`: on the catch path the
  LocalEnvironment is restored to what the TryCatch node received, the Environment is not.
  *(Runtime test 6 Oct: validation errors came back as raw HTTP 500s; with the error terminal unwired,
  an LMS HTTP 500 left the caller waiting 180 seconds.)*
- **IBM-20** A Compute node that builds a JSON reply sets
  `SET OutputRoot.Properties.ContentType = 'application/json';`, also after copying
  `InputRoot.Properties` from the back-end reply. Response headers are set as
  `SET OutputRoot.HTTPResponseHeader."X-TRACKING-ID" = trackingId;` (tested).
  *(Runtime test 6 Oct: JSON replies went out as `text/xml`.)*
- **IBM-21** HTTP Request failures arrive nested: BIP2230 › BIP3162 › BIP3152 › BIP3151 for a timeout,
  or BIP3150 when the back end cannot be reached. Find the deepest exception with this loop (tested at
  run time; `MOVE … OF …` is not ESQL), then compare its number, and any text in upper case:
  ```sql
  DECLARE errNumber INTEGER 0;
  DECLARE errText CHARACTER '';
  DECLARE ex REFERENCE TO InputExceptionList.*[1];
  WHILE LASTMOVE(ex) DO
    IF ex.Number IS NOT NULL THEN
      SET errNumber = ex.Number;
      SET errText = ex.Text;
    END IF;
    MOVE ex LASTCHILD;
  END WHILE;
  IF errNumber = 3151 OR CONTAINS(UPPER(errText), 'TIMEOUT') THEN  -- EAI-LMS-BRK-003
  ```
  A reply on the HTTP Request node's `error` terminal (LMS answered with an HTTP error) has no
  exception: `errNumber` stays 0.
  *(Runtime test 6 Oct: a timeout check for BIP3165 and 'Timeout' never matched, so timeouts became
  EAI-LMS-BRK-999.)*

## Decisions

- **IBM-09** Record every decision the lead gives you or that you take under IBM-25 (answers, chosen names,
  "no framework", placeholders accepted, findings left by design) in `docs/decisions.md`, one line
  each with the date. Later steps and reviewers read it.
  *(Dry run: a fresh reviewer reported the lead's decisions as defects.)*

## The Interface Definition Document

- **IBM-10** Write the Interface Definition Document in Markdown first: copy the structure of
  `templates/EAI_Interface_Definition_Document_TEMPLATE.md` exactly, fill every section from the code,
  and save it as `docs/EAI_Interface_Definition_Document_<Service>_v<x.y>.md`. Then make the Word file
  (DOC-01) with `python3 ../tools/md_to_docx.py <that .md file>`, which writes the `.docx` next to it.
  Do not edit the `.docx` template with the Office tools. Draw the diagram (DOC-04) as a text block.
  *(Test run 6 Oct: editing the Word template directly spent 13.5 Bobcoins and left every
  placeholder unfilled.)*

## Reviews

- **IBM-11** Do a review in a subagent (`spawn_subagent`, without the conversation history), so it
  judges the files as they are and not what you remember building, then report its findings.
  *(Dry runs: two reviews in the same context reported no findings on code with real defects; the
  same prompt with a subagent found eight.)*
- **IBM-12** The reviewer reads `docs/decisions.md` first and does not report a recorded decision
  as a finding. It re-reads every file it judges and always does these checks:
  1. For each SRS field row, name the code line that maps it. Report every row with no line, and
     every field or header in the code that is not in the SRS (REQ-01, IBM-02).
  2. List every literal value in the files: URLs, hosts, ids, codes, message catalogs, catalog,
     space and property names. For each, say where it comes from: the SRS, the prompt, the rules, or
     nowhere. A value from nowhere is a finding (IBM-01); "standard" is not a source.
  3. Check every change comment's requirement id, author and date (FW-07, IBM-03).
  4. Compare the HTTP status codes and error codes in every API file with the SRS lists (API-08,
     REQ-08).
  5. Run the Toolkit check (IBM-04).
  6. In every Compute node module, check each correlation name (ESQL-07): it reads `InputRoot`,
     `InputLocalEnvironment` or `Environment` and writes `OutputRoot`, `OutputLocalEnvironment` or
     `Environment`. `LocalEnvironment` or `Root` in a Compute node is a finding.
  7. Check that every file the standards require exists: the API and product YAML (PR-01),
     `azure-pipelines.yml` (PR-02), both properties files (PR-03, PR-04) and the Interface Definition
     Document in `docs/` (DOC-01, IBM-10). A missing file is a finding. Check that a file exists
     with a file listing; a `.docx` is binary, so do not judge it by reading it as text.
  8. Compare the JSON payload shape in the ESQL, `openapi.json` and the API Connect definition with
     the SRS tables (IBM-16).
  9. For a change, compare every version: `info.version` in `openapi.json` and in the API Connect
     definition, and the document's header, last Version History row and file name (IBM-17).
  10. Run the runtime check (IBM-04) and report every failure it prints. Check IBM-13, IBM-14 and
      IBM-18 to IBM-21 in the flow and ESQL files.
  A rule counts as checked only when the reviewer names the file and line it looked at.
