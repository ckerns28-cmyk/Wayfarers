# QA Factory

## Purpose

Create an exact validation report with command status for required Wayfarer checks.

## Inputs

- Repo root
- Godot binary path
- Python binary path
- Phase validation requirements
- Screenshot artifact directory

## Procedure

1. List every required command.
2. Run commands when requested and safe.
3. Mark unrun commands `SKIPPED_WITH_COMMAND`.
4. Include exact command text for skipped checks.
5. Distinguish technical pass from design approval.

## Required Output

```markdown
## QA Review
- Status:
- Command Results:
- Skipped Commands:
- Screenshot/PNG Verification:
- Capture Log:
- Council Authority Contribution:
```

## Fail Fast

Fail with `COUNCIL_FAIL_NEEDS_CODE_FIX` when a required technical command fails.
