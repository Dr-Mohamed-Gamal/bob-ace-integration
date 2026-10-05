# IBM working method for Bob in this workspace

These are IBM's instructions to Bob, not the client's standards. They say how Bob works here: what to do
when a value is unknown, how to check an ACE project, where decisions are kept and how a review is
run. Each one answers a mistake Bob made in the pilot dry runs of 5 October 2026. The client's
standards are in [`client-standards.md`](client-standards.md); when the two disagree, ask.

## Values and fields

- **IBM-01** Never invent a value: no hostnames, URLs, domains, requirement ids, catalog or space
  names, queue names, field names or credentials that are not in the SRS, the prompt or the existing
  code in the workspace. Reuse the names the workspace already uses (FW-04). Where a value is needed
  and none of these has it, use a placeholder: a property value `TODO_<NAME>`, or a URL on the
  reserved `.invalid` domain, for example `http://lms.todo.invalid/PointsInquiry`. Never put the
  client's domain in a value. List every placeholder in your final summary.
  *(Dry run: Bob put three invented hosts on the client's real domain into the code.)*
- **IBM-02** Read and write only the fields and headers the SRS names, on the channel side and on
  the back-end side (FW-01). If the design seems to need another one, ask.
  *(Dry run: Bob read a back-end field the SRS never mentions.)*
- **IBM-03** Take dates from the prompt. If the prompt gives none, run `date`. Never copy a date
  from the SRS into a change comment or a document.
  *(Dry run: every change comment carried the SRS date.)*

## Checking an ACE project

- **IBM-04** An ACE project is done only when the ACE Toolkit shows no errors and no warnings for
  it. If `tools/toolkit_check.py` is in the repository, run
  `python3 ../tools/toolkit_check.py <project folder>` from the workspace (Windows, macOS or Linux):
  it runs the Toolkit's own build and validators on a copy, about a minute. Fix every problem it
  reports and run it again. If the check is not available or cannot find ACE, say so and ask the
  developer to refresh the project in the Toolkit and paste the Problems view. The check reports
  errors only, so also avoid the warnings listed in IBM-05 to IBM-08.
  *(Dry run: Bob's first ACE project compiled but would not open in the Toolkit.)*
- **IBM-05** Each ACE project has `.settings/org.eclipse.core.resources.prefs` with exactly
  `eclipse.preferences.version=1` and `encoding/<project>=UTF-8`, where `<project>` is literal text,
  not the project name.
- **IBM-06** HTTP Request node: the "Web service URL" property is mandatory. Set it to a placeholder
  on the `.invalid` domain (IBM-01) and set the real URL at run time in
  `LocalEnvironment.Destination.HTTP.RequestURL` from the user-defined property.
- **IBM-07** In ESQL, `BROKER SCHEMA a.b.c` has no semicolon. A message flow's `nsURI` and
  `nsPrefix` match its path in the project.
- **IBM-08** `THROW USER EXCEPTION` uses the framework's message catalog. When there is no
  framework, leave out `CATALOG` so ACE uses its default; never invent or placeholder a catalog name.

## Decisions

- **IBM-09** Record every decision the lead gives you (answers to your questions, chosen names,
  "no framework", placeholders accepted, findings left by design) in `docs/decisions.md`, one line
  each with the date. Later steps and reviewers read it.
  *(Dry run: a fresh reviewer reported the lead's decisions as defects.)*

## The Interface Definition Document

- **IBM-10** Write the Interface Definition Document as a Word file (DOC-01), with your built-in
  Office tools (the `office-insights` skill). Start from `templates/EAI_Interface_Definition_Document_TEMPLATE.docx`
  and keep its structure; the `.md` copy of the template has the same content as text. Draw the
  diagram (DOC-04) as an image in the document.

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
  A rule counts as checked only when the reviewer names the file and line it looked at.
