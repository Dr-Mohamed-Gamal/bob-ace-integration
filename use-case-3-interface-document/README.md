# Use Case 3 — Document the Service

One prompt that writes the service's Interface Definition Document (IDD) in the team's template, from the code as built.

> Pilot use case for a bank's integration team. The template and the documents made from it are not published here.

## The Input

The team's IDD template: sign-off, version history, logical view, security, header and error mapping, exception handling, and per operation a summary, processing logic, data exchange tables (input, success output, failure output) and dependencies. Plus the service Bob built in use case 1.

## The Prompt

| # | Prompt | What Bob does |
|---|---|---|
| 3 | [Write the Interface Definition Document](prompts/03-interface-document.md) | Fills every section from the code: processing logic as coded, every field, every error code with its HTTP status, a Mermaid diagram of where the service sits, and a first version-history row dated with the date in the prompt |

## What the Rehearsal Showed

Every template section and every field was present, the date came from the prompt, and the error behaviour the document describes matched the code. Cost: 0.9 Bobcoins.

In an earlier run the document described the requirement's error rule while the code did something else at the time; the fresh review in use case 6 is what catches that kind of drift (rule DOC-05).
