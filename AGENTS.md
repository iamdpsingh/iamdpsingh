# Instructions for AI editors

Read `docs/EDITING_GUIDE.md` before editing. This is a GitHub profile README,
not a standalone web application.

- The owner's latest preference is a lightweight, monochrome, text-first profile
  suitable for older PCs. Preserve its personal-workstation direction: file-style
  links, a small data-flow diagram, optional ASCII portrait, and text activity.
  Use native Markdown and GitHub's light/dark theme.
  Do not add custom colors, images, badges, animation, CSS, scripts, or fonts.
- Keep headings readable and the layout compact. Use native expandable sections
  for the full catalog and secondary information. No layout tables or fake UI.
- Add projects in `data/projects.json`; run `python3 scripts/build_profile.py`.
  Keep all existing entries unless the owner requests removal. Feature three.
- Keep facts grounded. Do not invent employers, credentials, project benchmarks,
  contribution counts, or merged open-source contributions.
- `data/contributions.json` holds actual public GitHub calendar data. Refresh via
  `python3 scripts/refresh_activity.py`; show its date and source in the README.
- Validation/render jobs stay read-only. The trusted-main refresh workflow's
  `publish` job may update only README.md and data/contributions.json. This is
  the documented exception for contribution refreshes and easy project updates.
- Pin actions to verified full commit SHAs; disable checkout credentials.
- Existing SVGs are archived artwork, not live metrics. Do not embed them.
- Run `python3 scripts/build_profile.py`, `python3 scripts/validate_profile.py`,
  `python3 -m unittest discover -s tests -v`, and `git diff --check` after edits.
- Preview desktop and narrow layouts. Verify no image or external media requests,
  no horizontal overflow, and keyboard-operable expandable sections.
- Do not commit, push, or change repository settings unless requested.
