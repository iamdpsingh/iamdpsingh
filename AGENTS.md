# Instructions for AI editors

Read `docs/EDITING_GUIDE.md` before editing. This repository is a GitHub profile,
not a web application. The deliverable is `README.md` and its local SVG artwork.

- Preserve the charcoal `#050505`, red `#EF4444`, and orange `#F97316` identity.
- Preserve the website-style presentation: one static hero, three featured
  project covers, compact contact buttons, and a toolkit panel. Keep the longer
  catalog in native expandable sections. Use readable normal text headings.
- Keep meaningful text in Markdown. GitHub strips scripts and most custom CSS.
- Do not invent employers, dates, credentials, benchmarks, or contribution claims.
- Do not add remote image widgets, tracking pixels, dependencies, SVG scripts,
  external SVG resources, or workflows with write permissions.
- Keep actions pinned to verified full commit SHAs and checkout credentials disabled.
- Treat legacy SVGs as archived snapshots; they are not current activity metrics.
- Run `python3 scripts/validate_profile.py`,
  `python3 -m unittest discover -s tests -v`, and `git diff --check` after changes.
- Do not commit, push, or change account/repository settings unless requested.
