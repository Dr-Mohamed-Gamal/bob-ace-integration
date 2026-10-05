# Integration standards: App Connect Enterprise, API Connect and MQ

These rules apply to every task in the Bob workspace: creating a flow or an API, changing one,
documenting one and reviewing one. They were written for a bank's integration team, from its coding
standards, its API Connect checklist, its requirement and interface-document templates and what the
team said in the scoping sessions, and grown during the pilot runs of 5 October 2026: each rule added
then stops a mistake Bob made in a run. Bob reads this file on every turn (`.bob/rules/`).

If a rule and the requirement document disagree, or the requirement document is silent, stop and
ask. Do not guess.

## 1. How to work (FW)

- **FW-01** Build from the signed-off requirement document (SRS) only. Implement every field,
  condition and default it lists, and nothing it does not list.
- **FW-02** Reuse the existing framework and shared libraries, for example the REST utility
  library, the exception manager, the audit and logging libraries. Search the workspace first.
  Never write a new library, logger, error handler or utility when one already exists.
- **FW-03** Follow the nearest existing service of the same kind (same layer, same back end).
  Copy its structure, node layout and naming. Do not introduce a design no existing service uses.
- **FW-04** Names follow the team's conventions, not generic ones. Service, flow, schema, queue and file names
  come from the SRS and from the names already in the workspace. Never invent a queue name.
- **FW-05** Decide the layer before building: API Connect only, API Connect plus Online Middleware
  (ACE), or MQ. Take it from the "Application Development" column of the SRS scope table. If the
  SRS does not say, ask the lead.
- **FW-06** New requirements go in the Service Layer. Do not change the Global Layer or the
  framework libraries unless the SRS says so.
- **FW-07** Every change to existing code carries a comment with the requirement id, the author
  and the date, in the form already used in that file:
  `-- Added the below field mapping as part of <requirement id> By <author> on <date>`.
  The requirement id comes from the change SRS or the prompt, the author and the date from the
  prompt (if the prompt gives no date, run `date`; never copy a date from the SRS). Never invent or
  reuse an id. A new service has no change comment.
- **FW-08** Build only. Create the BAR when asked. Never deploy, never run `mqsideploy`, never push
  to the runtime repository. Deployment belongs to the pipeline.
- **FW-09** Target versions are ACE 13.0.7.2 with Toolkit v13, MQ 9.4 and Java 17.
- **FW-10** A REST service in Online Middleware is an ACE **REST API project**: the OpenAPI document
  is the contract and each operation is a subflow. Do not build it as an Application with HTTP Input
  and HTTP Reply nodes. (Source: the team's requirement documents list REST services as Method |
  RestAPI | OperationName | Provider, and its interface documents place them in a "Global REST
  Layer".)
- **FW-11** Never invent a value: no hostnames, URLs, domains, requirement ids, catalog or space
  names, queue names, field names or credentials that are not in the SRS or the prompt. Where a
  value is needed but unknown, use a placeholder: a property value `TODO_<NAME>`, or a URL on the
  reserved `.invalid` domain, for example `http://lms.todo.invalid/PointsInquiry`. Never put the client's
  domain in a value. List every placeholder in your final summary.
- **FW-13** Record every decision the lead gives you (answers to your questions, chosen names,
  "no framework", placeholders accepted) in `docs/decisions.md`, one line each with the date. Later
  steps and reviewers read it.
- **FW-12** An ACE project is done only when the ACE Toolkit shows no errors and no warnings for it.
  Run `python3 ../tools/toolkit_check.py <project folder>` from the workspace (it runs the Toolkit's
  own validation, about a minute) and fix every problem it reports, then run it again. The check
  reports errors only; also avoid the Toolkit's warnings. Each ACE project has
  `.settings/org.eclipse.core.resources.prefs` with exactly `eclipse.preferences.version=1` and
  `encoding/<project>=UTF-8`, where `<project>` is literal text, not the project name.

## 2. Requirement conformance (REQ)

- **REQ-01** Map each SRS row exactly: API or OMW field, back-end field, data type, and the logic
  in the "Transformation/Processing Logic" or "Description" column.
- **REQ-02** An optional field must never make the request fail when it is absent. Apply a default
  only when the SRS gives one.
- **REQ-03** A row marked `N/A` or "not required to be mapped" must not be mapped. Read and write
  only the fields and headers the SRS names, on the channel side and on the back-end side. If the
  design seems to need another one, ask.
- **REQ-04** Conditions written in prose ("mapped only if …", "set to null if …") are implemented
  exactly. Existing conditions on neighbouring fields stay unchanged.
- **REQ-05** For a change, touch only the services in the SRS scope table. One requirement usually
  affects several services, so check each one in the list.
- **REQ-06** JSON field names are camelCase. Back-end field names are used exactly as the SRS
  writes them.
- **REQ-07** Every REST API accepts the headers `ClientId`, `Authorization`, `X-USER-ID`,
  `X-MSG-ID` and `X-ORG-ID` (all mandatory). `X-TRACKING-ID` is optional and set by the middleware.
- **REQ-08** A failure response carries `statusCode`, `statusReason`, `errorCode` and `errorDesc`,
  with values from the SRS sections on HTTP status codes and error codes.
- **REQ-09** When a field is added and it is exposed to consumers, update the descriptors and the
  Swagger/OpenAPI file as well, and update the service's Interface Definition Document.

## 3. ESQL (ESQL, DB, ERR)

- **ESQL-01** One ESQL module per Compute, Database or Filter node. The module name equals the
  node's "ESQL Module" property. The module sits in an `.esql` file in the same broker schema as
  the node. The entry point is `MAIN`.
- **ESQL-02** Declare every variable with `DECLARE` and a data type before use. Clear every
  Toolkit warning about undefined variables before building.
- **ESQL-03** ESQL variable names are case sensitive. Use one spelling everywhere. The standard
  recommends uppercase names; inside an existing file, follow that file's convention.
- **ESQL-04** Give a variable its initial value on the `DECLARE` when the value is known.
- **ESQL-05** Keywords in uppercase, one statement per line, each ending with a semicolon.
- **ESQL-06** Reusable constants, functions and procedures are declared at broker-schema level,
  not inside a module. A schema-level routine cannot use correlation names (`InputRoot`,
  `OutputRoot`, `LocalEnvironment`, `OutputLocalEnvironment`, `Environment`): pass the trees as
  `REFERENCE` parameters, or keep a routine that needs them inside the module. Call them by fully-qualified name, or through a `PATH` statement placed in
  the same file outside any `MODULE`. Never define a function or procedure inside `EVAL`.
- **ESQL-07** Correlation names: in a Compute node read from `InputRoot` / `InputBody` and write
  to `OutputRoot`; in Database and Filter nodes use `Root` / `Body`. Only a Compute node creates
  an output message.
- **ESQL-08** When the code changes `LocalEnvironment`, set the Compute node's "Compute mode" so
  that it is propagated.
- **ESQL-09** Check for missing or null elements through a `REFERENCE` variable with `LASTMOVE`
  and `FIELDVALUE`. Do not put a long field path straight into `IF … IS NULL`.
- **ESQL-10** Use a `REFERENCE` variable for a structure that is read or written more than once,
  instead of repeating the full path.
- **ESQL-11** Repeating elements are indexed from 1; `[<]` is the last and `[>]` the first. Delete
  repeats in reverse order, highest index first.
- **ESQL-12** Put `CARDINALITY` into a variable before a loop. Never call it in the `WHILE`
  condition.
- **ESQL-13** `CAST` explicitly before comparing or calculating with values of different types.
  All XML field values are character. Do not rely on implicit casts.
- **ESQL-14** Character, byte and bit strings go in single quotes. Identifiers that need quoting
  go in double quotes.
- **ESQL-15** Broker properties such as `BrokerName` are read-only: never on the left of `SET`.
  Do not give a variable the name of a broker property.
- **ESQL-16** Set code page and encoding explicitly on `OutputRoot.MQMD` (`CodedCharSetId`,
  `Encoding`) and on every additional header when converting.
- **ESQL-17** A BLOB body is not parsed. Read it by position with `SUBSTRING` only.
- **ESQL-18** Keep existing `$MQSI … MQSI$` keyword comments intact.
- **DB-01** On every node that accesses a database: "Throw exception on database error" selected,
  "Treat warnings as errors" selected, Transaction set to Automatic.
- **DB-02** Where ESQL handles a database error itself, capture `SQLSTATE`, `SQLCODE`,
  `SQLERRORTEXT` and `SQLNATIVEERROR` and raise them with `THROW USER EXCEPTION`.
- **DB-03** Stored procedures: the `EXTERNAL NAME` matches the database procedure, no overloaded
  procedures, parameter count and direction match exactly (plus one per dynamic result set).
  Choose the data source or schema with the `IN` clause, not `EXTERNAL SCHEMA`.
- **ERR-01** Decide error handling for each flow on purpose. Set the transaction mode of input and
  output nodes deliberately; do not leave failure behaviour to the defaults.
- **ERR-02** Use the framework's exception handling and error-code mapping. An error response
  carries the mapped error code and description, or the generic system error code when no mapping
  exists.
- **ERR-03** Log through the existing log4j-based logging node and its existing destinations.

- **NODE-01** HTTP Request node: the "Web service URL" property is mandatory. Set it to a
  placeholder on the `.invalid` domain (FW-11) and set the real URL at run time in
  `LocalEnvironment.Destination.HTTP.RequestURL` from the user-defined property.
- **NODE-02** In ESQL, `BROKER SCHEMA a.b.c` has no semicolon. A message flow's `nsURI` and
  `nsPrefix` match its path in the project.
- **NODE-03** `THROW USER EXCEPTION` uses the framework's message catalog. When there is no
  framework, leave out `CATALOG` so ACE uses its default; never invent or placeholder a catalog name.

## 4. API Connect (API, SEC, INV, PRD, PR)

- **API-01** Design first: an OpenAPI/Swagger 2.0 or 3.0 definition before implementation. API
  files are YAML.
- **API-02** Before creating an API or a product, check the Developer Portal for the same name and
  version. No duplicates.
- **API-03** Use consistent naming across endpoints, parameters and resources. Resource names are
  nouns, not verbs: `/users`, not `/getUsers`.
- **API-04** URL format is `/<basepath>/<versionnumber>/<operationpath>`. The base path carries the
  API or product name and the version, for example `/customers/v1`. Paths are named after the
  provider system operation.
- **API-05** Keep the version current, for example `V1.0.0`. Raise it on any change, and change
  the version in the URL when several versions must run together. Stay backward compatible for
  existing clients.
- **API-06** HTTP methods: `GET` retrieves, `POST` creates, `PUT` replaces, `PATCH` updates part of
  a resource. `DELETE` is not recommended unless the provider supports it.
- **API-07** Payloads are JSON.
- **API-08** Declare request and response definitions with samples. Provide schemas and sample
  data for every HTTP status code in the SRS list, at least 200, 400, 401, 403, 404, 429, 500, 502
  and 504, in both the API Connect definition and the ACE `openapi.json`.
- **API-09** Fill in the API description, including the provider system's functional details.
- **API-10** Errors use informative codes and messages and one consistent response shape. Status
  codes: 200 success, 400 bad request (functional failure for the input), 401 unauthorized,
  404 endpoint not available, 500 time-out from the provider.
- **SEC-01** Every API uses native OAuth2 and client-id security. Scopes are defined per back-end
  system, for example `CORE` or `CARD`.
- **SEC-02** OAuth2 token expiry: 24 hours for internal consumers, 3 minutes for external
  consumers, unless the business requirement says otherwise.
- **SEC-03** HTTPS for all API traffic.
- **SEC-04** Set a rate limit for internal and external consumers in line with the business
  requirement. The default plan is 100 calls per hour as a soft limit.
- **SEC-05** No hard-coded credentials anywhere.
- **INV-01** The invoke `target-url` is built from catalog properties. Never a static endpoint.
- **INV-02** User name and password for basic authorization come from properties, not literals.
- **INV-03** The TLS profile matches the provider system's secure connectivity.
- **INV-04** Set the timeout to suit the consumer. The default is 60 seconds.
- **INV-05** State the HTTP method explicitly. Omitted or `Keep` reuses the incoming method; use
  that only on purpose.
- **INV-06** Enable "stop on error" with the relevant errors so the flow ends when the provider
  call fails. Use the header blocklist or allowlist where headers must be controlled.
- **PRD-01** An API is published only inside a product. No independent API publishing.
- **PRD-02** A product has a proper name, a short description and a version. Visibility and
  subscribability are set for the organisation or group that needs it.
- **PRD-03** Subscription approval is enabled on every product plan. Categories are maintained.
- **PRD-04** Gateway and organisation follow the interaction: internal consumer and internal
  provider use the Internal gateway under the Internal organisation; internal consumer and
  external provider use the External gateway under the Internal organisation; external consumer
  and internal provider use the External gateway under the External organisation.
- **PR-01** File names: `<APIName>.yaml` and `<ProductName>.yaml`, with no version in the file
  name, for example `CustomerDetailsAPI.yaml` and `Customers.yaml`.
- **PR-02** `azure-pipelines.yml` names the pool, the variable group and the stage templates.
- **PR-03** `product-test.properties` contains `CHANGETYPE` (`NEW` or `BUGFIX`; `BUGFIX` for a
  product replacement), `APISERVER`, `ORG`, `DEVGATEWAY`, `UATGATEWAY`, `DEVCATALOG`,
  `UATCATALOG`, `DEVSPACE`, `UATSPACE`, `NEWPRODUCT`, `OLDVERSION` and `PRODUCTYAML`.
- **PR-04** `product-prod.properties` contains `CHANGETYPE`, `PRODORG`, `PRODGATEWAY`,
  `PRODCATALOG`, `PRODSPACE`, `NEWPRODUCT`, `OLDVERSION` and `PRODUCTYAML`.
- **PR-05** Every catalog property the invoke policy uses exists in the DEV, UAT and PROD catalogs.
- **PR-06** The deployment product still includes every API currently under that product. Do not
  drop an existing API.

## 5. Interface Definition Document (DOC)

- **DOC-01** One document per service, in `docs/`, named
  `EAI_Interface_Definition_Document_<Service>_v<x.y>.md` (Markdown with the template's structure;
  it is converted to Word afterwards). It holds the complete current state of the service. Every
  change updates it, adds a Version History row, and raises the version in the header and in the
  file name (for example `_v1.0.md` becomes `_v1.1.md`).
- **DOC-02** Keep the fixed structure of `templates/EAI_Interface_Definition_Document_TEMPLATE.md`.
- **DOC-03** Data Exchange lists every input and output field of every operation, in the columns
  Common XSD Field, Description, Data Type and Transformation/Processing Logic.
- **DOC-04** The diagram shows only where the service sits: consuming applications, API gateway,
  middleware layers, back end. No infrastructure. Draw it as a Mermaid block in the document.
- **DOC-05** Document the code as it is. Do not describe behaviour that is not in the code. Mark
  anything you could not determine as "To be confirmed".

## 6. When asked to review

Do the review in a subagent (`spawn_subagent`, without the conversation history), so it judges the
files as they are and not what you remember building, then report its findings. The reviewer
re-reads every file it judges and re-runs every check itself, including
`python3 ../tools/toolkit_check.py <project folder>`. It reads `docs/decisions.md` first and does not
report a recorded decision as a finding.

Review on three questions, in this order: does the change match the requirement, does it follow
these standards, does it fit the framework. Review it as if someone else wrote it. Always do these
checks:

1. For each SRS field row, name the code line that maps it. Report every row with no line, and
   every field or header in the code that is not in the SRS (REQ-01, REQ-03).
2. List every literal value in the files: URLs, hosts, ids, codes, message catalogs, catalog, space
   and property names. For each, say where it comes from: the SRS, the prompt, the rules, or nowhere.
   A value from nowhere is a finding (FW-11); "standard" is not a source.
3. Check every change comment's requirement id against the SRS (FW-07).
4. Compare the HTTP status codes and error codes in every API file with the SRS lists (API-08, REQ-08).
5. Run the Toolkit check (FW-12).

Report each finding as one table row: rule id, file and line, what is wrong, the fix. A rule counts
as checked only when you name the file and line you looked at. Do not change any file during a
review.
