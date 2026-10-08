# Use Case 1 — Create a Service

One prompt that takes a requirement document for a new REST service to a built API Connect API and product and an ACE REST API project, with IBM Bob Shell inside the ACE Toolkit.

> Pilot use case for a bank's integration team. The runs used a mock requirement document in the team's layout, with invented content: [documents/requirements/](../documents/requirements/).

## The Input

A requirement document (SRS) for two new APIs of an invented loyalty-points project. For each API: method, path, OAuth scope, six standard headers, a JSON-to-XML field table for the request, XML-to-JSON tables for the success and failure responses, an error-code list and an HTTP status list. Its scope table says each API is built on **API Connect and the ACE middleware layer**. Only the inquiry API is built in the pilot.

## The Prompts

| # | Prompt | What Bob does |
|---|---|---|
| 1 | [Plan and build](prompts/01-plan-and-build.md) | Reads the requirement and the rules, picks the layers from the scope table, states its plan and the decisions it took for what the requirement leaves open (rule IBM-24 holds the defaults; rule IBM-25 says never ask), builds the API Connect API, product and pipeline properties and the ACE REST API project (OpenAPI document, generated main flow, one subflow per operation, ESQL), runs the Toolkit check and the runtime check, fixes what they report and reruns them until both pass |

## What It Produces

- `apic/`: the API definition (Swagger 2.0) with OAuth2 and client-id security, every status code with an example, and an invoke to ACE through a catalog property; the product with subscription approval and a rate plan; the pipeline property files with `TODO_` placeholders.
- `LoyaltyPointsInquiryAPI/`: an ACE REST API project: `.project`, `.settings`, `restapi.descriptor`, `openapi.json`, the generated main flow, the operation subflow (Try/Catch, request mapping, HTTP Request to the back end, response mapping, error handling) and its ESQL modules.
- `docs/decisions.md`: Bob's decisions, one per line with the rule each comes from.

## What the Rehearsal Showed

The Toolkit check passed the first time. Every field of the requirement was mapped and nothing else; all nine status codes were in both API definitions; there were 21 placeholders, all `TODO_…` or on the reserved `.invalid` domain, and no invented hostnames or ids. Cost: 6.3 Bobcoins for the two prompts it took then. On 8 October, with the decisions moved into the rules, the single prompt asked nothing, listed nine decisions, passed both checks on the first pass and cost 4.5 Bobcoins.

The earlier runs explain the rules that made this possible: the first build invented hosts on the client's real domain, read a back-end field the requirement never mentions, and produced an ACE project the Toolkit could not open. See rules IBM-01, IBM-02, IBM-04 and IBM-06 in [RULES/ibm-working-method.md](../RULES/ibm-working-method.md).
