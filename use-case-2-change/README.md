# Use Case 2 — Change the Service

One prompt that applies a change requirement to the existing service.

> Pilot use case for a bank's integration team. The change requirement is a mock in the team's layout, with invented content: [documents/requirements/](../documents/requirements/).

## The Input

A change requirement (id URF-90001) for two existing APIs. For the inquiry API: a new optional field mapped to the back end only for one programme code, a new optional field defaulted to 'N' when absent, and a new output field returned only when the back end sends it. For the redemption API, which is not in the workspace: two new fields and one field explicitly marked as not to be mapped.

## The Prompt

| # | Prompt | What Bob does |
|---|---|---|
| 5 | [Apply the change](prompts/05-change.md) | Maps the three new fields with their conditions and default, adds a change comment with the requirement id, author and date at each change, updates both API definitions and the document (fields, processing logic, version history), runs the Toolkit check, and leaves the redemption API alone |

## What the Rehearsal Showed

All checks passed: the programme-code condition, the 'N' default, the guarded output field, change comments dated with the date in the prompt, both API definitions, the document's version raised in its header. The review of the change (use case 6, prompt 7) then found the gaps a person should fix: the document file name and the API versions were not raised. Cost: 6.7 Bobcoins.

Without the date in the prompt, an earlier run dated every change comment with the requirement's date (rules FW-07 and IBM-03).
