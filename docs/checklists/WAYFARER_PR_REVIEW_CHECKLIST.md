# Wayfarer PR Review Checklist

## Preflight

- [ ] Branch starts from latest `origin/main`.
- [ ] Working tree was clean before implementation.
- [ ] Remote permission health checked.
- [ ] Open PR state checked.
- [ ] Merge authority checked: explicit Chris request, or ordinary roadmap-bound autonomous PR before SV-1 that satisfies the autonomous merge rule.

## Scope

- [ ] PR matches phase brief.
- [ ] No unrelated file churn.
- [ ] No generated cache/import metadata included unless intentional.
- [ ] PR summary separates technical validation from design acceptance.

## Required Validation

- [ ] Godot import validation.
- [ ] `validate_vertical_slice.gd`.
- [ ] `validate_newport_asset_provenance.py` when Newport assets are touched.
- [ ] G-4.21A extraction validation when Newport core building pipeline could be affected.
- [ ] Screenshot capture/PNG verification for visual passes.
- [ ] Capture log check for screenshot passes.
- [ ] G-5 migration architecture validator when the PR touches migration planning or post-G-5 roadmap direction.
- [ ] G-6 production cutover validator when the PR touches deployment, cutover policy, route ownership, or post-G-5 release planning.
- [ ] Starter Village roadmap validator when the PR touches SV-1 planning or phase sequencing.
- [ ] Starter Village execution ledger validator when the PR touches SV-1 evidence/status.
- [ ] SV-0 tooling stack validator when the PR touches Starter Village layout, quest/dialogue, NPC movement, screenshots, runtime proof, asset cleanup, ground cohesion, or council process.
- [ ] Phase-specific Starter Village validator(s) when the PR touches world cohesion, runtime atelier assets, character motion, NPC population, interaction UX, quest arc, tavern whispers, first-session playability, or SV-1 gate readiness.
- [ ] Runtime movement proof manifest/frames for NPC or player movement phases.
- [ ] `git diff --check`.
- [ ] `git diff --cached --check`.

## Council Review

- [ ] Scrum Master review.
- [ ] Game Designer review.
- [ ] World/Layout Designer review.
- [ ] Art Director review.
- [ ] Animation/NPC Behavior Director review where applicable.
- [ ] Narrative Designer review where applicable.
- [ ] UX Designer review.
- [ ] Game Programmer review.
- [ ] QA Analyst review.
- [ ] Build/Release Engineer review.
- [ ] Final authority verdict recorded without deprecated human-review final states.
