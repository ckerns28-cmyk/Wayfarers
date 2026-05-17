# Release Manager Factory

## Purpose

Collect all council reviews and produce one recommendation for Chris.

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
5. Write a repair prompt if not merge candidate.

## Required Output

```markdown
## Release Manager Decision
- Recommendation for Chris:
- Decision:
- Required Repairs:
- Why Technical Pass Does Not Equal Design Pass:
- Merge Conditions:
```

## Decision Rules

Never return `MERGE CANDIDATE` unless all required agents pass or explicitly mark remaining issues acceptable for the phase.
