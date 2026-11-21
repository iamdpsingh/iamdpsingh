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
- The owner removed the capability manifest, SQL bio, and project DAG. Do not
  reintroduce them. The personal addition is a halftone-dot avatar print card.
- `data/avatar-pattern.json` is a 64x64 hexadecimal luminance sample of the
  owner-approved GitHub avatar. Preserve its source and identity; no invented face.
- The card combines a short row-by-row print animation with factual, dated
  contribution counts. Do not relabel those as uptime, SLA, token, or eval metrics.
- Only exact `AVATAR_STYLE` CSS is permitted: opacity-only, one pass under three
  seconds, static final state, reduced-motion fallbacks. No scripts or SMIL.
- Use only the original reviewed image hosts and inline layout styles. No scripts,
  iframes, event handlers, unreviewed image services, or executable downloaded SVGs.
- Keep action pins and checkout-credential hardening. Validation/render jobs are
  read-only; the trusted-main publish job may change only generated README,
  contribution JSON, project-evidence documentation, and generated avatar SVGs.
- Contribution art retained from the original design is labeled as snapshots.
  Only the dated contribution JSON summary is independently refreshed here.
- Run `python3 scripts/build_profile.py`, `python3 scripts/validate_profile.py`,
  `python3 -m unittest discover -s tests -v`, and `git diff --check` after edits.
- Verify the new cards and source links in the rendered original layout.
- Do not commit, push, or change repository settings unless requested.
