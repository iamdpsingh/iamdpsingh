# Instructions for AI editors

Read `docs/EDITING_GUIDE.md` before editing. This is a GitHub profile README.
The owner's latest request explicitly restores the original design from before
this chat's edits (baseline commit `6f86ae0`), superseding the monochrome and
terminal-style experiments.

- Preserve the original charcoal/red/orange waves, typing effects, social badges,
  technology grids, project-card table, and contribution-art sections.
- Edit `templates/profile.md` for the original layout and existing project cards.
- Add new project cards in `data/additional-projects.json`, then run
  `python3 scripts/build_profile.py`. Do not hard-code new cards into README.md.
- Preserve dates, evidence labels, caveats, and sources for project claims.
  Coverage is not completion; dated counts are not live counts; simulations are
  not production recoveries; reported tests are not independently rerun tests.
- Never invent a repository link: Rolewisp uses the supplied application URL.
- `docs/PROJECT_EVIDENCE.md` is generated from the additional-project evidence.
- Use only the original reviewed image hosts and inline layout styles. No scripts,
  iframes, event handlers, unreviewed image services, or executable downloaded SVGs.
- Keep action pins and checkout-credential hardening. Validation/render jobs are
  read-only; the trusted-main publish job may change only generated README,
  contribution JSON, and project-evidence documentation.
- Contribution art retained from the original design is labeled as snapshots.
  Only the dated contribution JSON summary is independently refreshed here.
- Run `python3 scripts/build_profile.py`, `python3 scripts/validate_profile.py`,
  `python3 -m unittest discover -s tests -v`, and `git diff --check` after edits.
- Verify the new cards and source links in the rendered original layout.
- Do not commit, push, or change repository settings unless requested.
