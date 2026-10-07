# Prompt 5 — Fix the accepted findings

Send after a person has read the review and decided. The finding numbers and reasons change with each review, so this prompt is written each time; keep its shape: what to fix, what is by design and why, then the checks and the document.

As sent in one trial run (7 October), after a review with three findings:

```text
Fix F-1 and F-2 as proposed. F-3 is by design: BuildValidationError writes OutputRoot, so under ESQL-06 it stays inside the module. Record these decisions in `docs/decisions.md`. Then run both checks in IBM-04, and update the Interface Definition Document where the behaviour it describes has changed.
```

When the review finds nothing to fix:

```text
The review found nothing to fix. Record in `docs/decisions.md` that the review found no findings, and change no other file.
```
