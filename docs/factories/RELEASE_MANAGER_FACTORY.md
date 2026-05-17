# Release Manager Factory

## Purpose

Collect all council reviews and produce one final authority verdict.

## Inputs

- Scrum Master review
- Game Designer review
- Art Director review
- Game Programmer review
- QA review
- World/Narrative review
- UX review
- Technical Artist review

## Procedure

1. Build an agent status table.
2. Separate technical validation from design acceptance.
3. Identify blockers.
4. Apply release decision rules.
5. Write a repair prompt if the phase does not pass.

## Required Output

```markdown
## Release Manager Decision
- Final Authority Verdict:
- Required Repairs:
- Why Technical Pass Does Not Equal Design Pass:
- PR Readiness Conditions:
```

## Decision Rules

Use exactly one final authority verdict: `COUNCIL_PASS_READY_FOR_PR`, `COUNCIL_FAIL_NEEDS_CODE_FIX`, or `BLOCKED_REQUIRES_HUMAN_ESCALATION`. Never return `COUNCIL_PASS_READY_FOR_PR` unless all required agents pass or explicitly mark remaining issues acceptable for the phase.
