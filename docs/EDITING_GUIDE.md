# Profile editing guide

Start with `AGENTS.md`. The owner's latest direction replaces the colorful
website-style graphics with a lightweight monochrome profile for older PCs.
Use a personal-workstation theme: file-style navigation, a small ASCII data-flow
diagram, an optional text portrait, plain project entries, and text-only activity.
There are no image downloads, animations, custom fonts, scripts, or stylesheets
in the rendered README. GitHub supplies its own light/dark colors and link styling;
content must stay understandable without color or graphics.

## Add a project — one file

Edit `data/projects.json` and add an object to the list:

```json
{
  "name": "Your project name",
  "url": "https://github.com/iamdpsingh/YOUR-REPOSITORY",
  "category": "Data & analytics",
  "description": "What it does, in one factual sentence."
}
```

Replace the example values with real details. Use one of `Data & analytics`,
`Applications & AI`, or `IoT & hardware` as the category. A hardware project
without a repository can omit `url`. Optional `demo` supplies an HTTPS demo link.
Names and descriptions are plain text, not HTML or Markdown.

Run:

```sh
python3 scripts/build_profile.py
python3 scripts/validate_profile.py
python3 -m unittest discover -s tests -v
git diff --check
```

No artwork or workflow edits are required. When editing JSON directly on GitHub,
the Refresh profile workflow builds and publishes the catalog after the change
reaches `main`.

To feature a project, give it `"featured": true`, a repository URL, and a `"stack"`
string such as `"Python / SQL / BigQuery"`. Remove `featured` from one existing
featured entry: there must be exactly three. Stack labels wrap as native inline
code on narrow screens. Featured category labels can describe the specific work.

Keep older projects in the expandable catalog. There is no fixed count limit;
the starting catalog has ten linked software/data projects plus three hardware
projects. Unknown catalog categories fail validation rather than hiding projects.

## Sources of truth

| Content | Edit here |
| --- | --- |
| Projects | `data/projects.json` |
| Optional ASCII portrait | `data/portrait.txt` |
| Intro, stack, generated activity layout | `scripts/build_profile.py` |
| Experience, education, certifications, footer | `README.md`, below `## Background` |
| GitHub activity | Generated `data/contributions.json` |
| Content guardrails | `scripts/validate_profile.py` |

The builder regenerates everything above `## Background` and preserves that
section and the footer. Do not rename that heading without updating the builder.
`PROJECTS_START`/`PROJECTS_END` identify the generated catalog; edit its JSON source.
No framework, package manager, API key, or third-party Python dependency is needed.

The earlier SVG artwork remains in the repository as an archive. It is not
embedded, downloaded by visitors, or used as a source of current activity.
The owner approved the current GitHub avatar as the portrait source. Its
36-column, 20-line ASCII rendering is stored in `data/portrait.txt`, inside a native
expandable section. It was derived from the verified avatar at
`https://avatars.githubusercontent.com/u/115564211?v=4` on 2026-11-21. Only plain
text is delivered; no photo is fetched or decoded by README visitors. The builder
accepts only the portrait's bounded ASCII character palette. GitHub's normal
profile UI still displays its native avatar outside this README.

## Real contribution activity, rendered as text

`scripts/refresh_activity.py` reads GitHub's public contribution calendar:
`https://github.com/users/iamdpsingh/contributions`. It extracts dated cell counts
and GitHub intensity levels, validates complete contiguous dates, and matches the
sum against GitHub's published total. The resulting JSON includes the source URL,
refresh date, total, and individual daily counts. It never downloads or executes
an external SVG generator.

The README shows the total, active days, refresh date, and date range as text.
An optional expandable ASCII calendar shows the latest 13 weeks using `. : + * #`
for GitHub's five intensity levels. Each column is one week and each row a weekday.
This representation needs no graphics or color. The daily JSON and GitHub source
are linked beside the summary.

Refresh locally:

```sh
python3 scripts/refresh_activity.py
python3 scripts/build_profile.py
```

Calendar requests have size limits, timeouts, and GitHub-only redirects. Missing
cells, changed markup, stale dates, or mismatched totals stop the refresh. The
last committed snapshot remains available with its original date. Never invent
data to fill gaps or relabel an old snapshot as current. Contributions are not
commits alone and do not establish accepted external contributions.

## Automation and security

`validate-profile.yml` builds and validates with read-only repository access.
`refresh-profile.yml` runs at 03:20 UTC daily, manually, or after project/builder
changes on `main`. It has two isolated jobs:

1. `render`: read-only checkout, public calendar request, Markdown generation,
   validation, and a short-lived artifact containing only the README and data.
2. `publish`: trusted-main only, `contents: write`, download the artifact, and
   commit only `README.md` and `data/contributions.json`. The built-in GitHub token
   is used only for the final push; checkout credentials are not persisted.

This narrow publishing job supports genuine contribution refreshes and simple
project updates. It is the documented exception to the earlier no-write workflow
rule. No personal access token, untrusted pull-request execution, force-push,
remote widgets, or external generators are needed. The publishing checkout uses
the render job's exact source commit, so concurrent changes cause a safe push
rejection instead of overwriting newer work. Rerun against the latest `main`.
All jobs have five-minute timeouts; actions use verified full commit SHAs.
Dependabot proposes updates. See [GitHub's security guidance](https://docs.github.com/en/actions/reference/security/secure-use).

The profile validator allows only the small existing native HTML subset for
expandable sections and links. Images and active content are rejected. Existing
SVG validation helpers remain for archived-artwork regression tests; archived
files are not part of the rendered profile. These checks are guardrails, not a
general-purpose sanitizer or an audit of external demos or repository settings.

## Review and AI handoff

Check desktop and 375px layouts, GitHub light/dark mode, readable code blocks,
working links, keyboard disclosures, and no image/media requests. A local preview
approximates GitHub; check the actual profile after publishing.

> Read AGENTS.md and this guide. Preserve the lightweight text-only profile.
> Edit projects in data/projects.json, keep all claims factual, build the README,
> run validation and tests, and inspect narrow and desktop layouts. Keep activity
> dated and traceable. Do not add graphics, custom colors, animation, or dependencies.
