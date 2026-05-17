# Scrum Master Factory

## Purpose

Create a Scrum Master review for any Wayfarer phase, branch, or PR.

## Inputs

- Phase brief
- Current branch
- Current git status
- Open PR list
- Roadmap section
- Diff summary

## Procedure

1. Confirm branch starts from latest `origin/main`.
2. Confirm clean preflight before implementation.
3. Identify open/duplicate/conflicting PRs.
4. Compare requested work to roadmap and phase scope.
5. Flag scope creep or unrelated changes.
6. Contribute to the final authority verdict.

## Required Output

```markdown
## Scrum Master Review
- Status:
- Branch/PR Health:
- Roadmap Alignment:
- Scope Risks:
- Council Authority Contribution:
```

## Fail Fast

Fail with `BLOCKED_REQUIRES_HUMAN_ESCALATION` only when branch sync, PR conflict, or worktree state cannot be safely resolved by Codex.
