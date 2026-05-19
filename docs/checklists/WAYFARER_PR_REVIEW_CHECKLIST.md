# Wayfarer PR Review Checklist

## Preflight

- [ ] Branch starts from latest `origin/main`.
- [ ] Working tree was clean before implementation.
- [ ] Remote permission health checked.
- [ ] Open PR state checked.
- [ ] Merge authority checked: explicit Chris request, or ordinary roadmap-bound autonomous PR before OVI-1 that satisfies the autonomous merge rule.

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
- [ ] Opening Village + Island roadmap validator when the PR touches G-14 through G-22 planning or phase sequencing.
- [ ] Opening Village + Island execution ledger validator when the PR touches OVI-1 evidence/status.
- [ ] `validate_newport_harbor_town_reconstruction.py` when the PR touches G-19R, Newport district structure, road hierarchy, MMORPG-scale avenue/wharf widths, block depth, lot spacing, walkable camera composition, or the G-19/G-20 runway after Chris screenshot critique.
- [ ] OVI-1 phase-specific validator(s) when the PR touches island topology, transition, terrain cohesion, POIs, island atelier assets, island NPCs/encounters, village-to-island quest, multi-path rumor choice, first-session loop, browser hardening, or final OVI-1 readiness.
- [ ] SV-0 tooling stack validator when the PR touches Starter Village layout, quest/dialogue, NPC movement, screenshots, runtime proof, asset cleanup, ground cohesion, or council process.
- [ ] SV-0 tool acquisition manifest validator when the PR adds, downloads, installs, configures, or depends on free tooling, addons, packages, browser resources, QA tools, or council/tooling policy.
- [ ] Starter Village layout-source usage validator when the PR touches Newport map placement, lots, building scale, service-yard reads, or world-layout source data.
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
- [ ] For Newport/OVI-1 layout work, the council confirms city structure before decoration: districts, road hierarchy, road widths, wharf apron, block depth, lots, walkable negative space, and camera readability are proven before props or UI polish.
- [ ] G-14 reports, if applicable, record `Human review required: no` and `Next phase: G-15 Opening Island Masterplan + World Topology`.
- [ ] Agent Council fails the phase if G-14 tries to stop for Chris before OVI-1.
