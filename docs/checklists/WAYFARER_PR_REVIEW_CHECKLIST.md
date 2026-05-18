# Wayfarer PR Review Checklist

## Preflight

- [ ] Branch starts from latest `origin/main`.
- [ ] Working tree was clean before implementation.
- [ ] Remote permission health checked.
- [ ] Open PR state checked.
- [ ] No merge performed unless explicitly requested.

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
- [ ] `git diff --check`.
- [ ] `git diff --cached --check`.

## Council Review

- [ ] Scrum Master review.
- [ ] Game Designer review.
- [ ] Art Director review.
- [ ] Game Programmer review.
- [ ] QA review.
- [ ] World/Narrative review.
- [ ] UX review.
- [ ] Technical Artist review.
- [ ] Release Manager recommendation for Chris.
