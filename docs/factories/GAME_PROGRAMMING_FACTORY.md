# Game Programming Factory

## Purpose

Create an engineering review for Godot implementation, maintainability, automation, pathing, collision, and regression risk.

## Inputs

- Source diff
- Godot import output
- Vertical slice output
- Screenshot automation output
- Pathing/collision data

## Procedure

1. Check scene/data architecture.
2. Check implementation scope.
3. Check collision, pathing, and interaction metadata.
4. Check screenshot automation stability.
5. Check that debug/proof systems are gated.

## Required Output

```markdown
## Game Programmer Review
- Status:
- Implementation Quality:
- Data/Scene Structure:
- Collision/Pathing:
- Automation:
- Regression Risks:
- Recommendation for Chris:
```

## Fail Fast

Fail if implementation breaks runtime loading, sprite rendering, required validation, or screenshot automation.
