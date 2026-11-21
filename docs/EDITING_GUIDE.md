# Profile editing guide

The owner's latest request is to restore the original GitHub profile design from
before this chat's edits, then add V-INDEX / Rolewisp and Data Pipeline Immune
System carefully. This replaces the intermediate minimalist, website-style, and
monochrome experiments. Read `AGENTS.md` first.

## Original layout

`templates/profile.md` restores the README from commit `6f86ae0`: charcoal/red/orange
waves, typing SVGs, social badges, technology icon grids, two-column project cards,
experience, education, GitHub stats, and contribution art. Preserve that design.
The restoration also supplies missing image alternatives, describes the 2025
internship as experience rather than current employment, updates the month badge,
and distinguishes preserved artwork snapshots from the current dated summary.

The original layout deliberately uses hosted image services and a card table.
Those are restored at the owner's explicit request. Do not replace them with a
new design or claim the profile is self-contained, entirely local, or text-only.
External cards can be unavailable independently of this repository. GitHub strips
most custom CSS and controls the outer page. Layout tables and original animations
retain the limitations of the source design; no responsive or accessibility audit
of all historical widgets is implied.

## Personal halftone avatar

The owner asked to remove the capability manifest, SQL bio, and Source → system →
product DAG, then clarified the replacement as **halftone dots forming the face**.
Those three additions, their generator code, and their assets are removed.
The original decorative developer GIF beside the bio is replaced by the personal
avatar card; the header, technology grids, and compact project cards remain.

`data/avatar-pattern.json` stores a 64-by-64 luminance sample of the owner's
approved GitHub avatar at `https://avatars.githubusercontent.com/u/115564211?v=4`,
sampled on 2026-11-21. Each character is hexadecimal brightness (`0` dark, `f`
light). The source photo is sampled, not redrawn into an invented identity.
The final asset uses SVG circles of varying radius: bright dots on dark surfaces
and dark ink dots on light surfaces. It is not an ASCII-character portrait.

Design brief: a recognizable monochrome halftone portrait that prints row by row,
paired with a compact, truthful terminal-style public activity snapshot.
The initial generative pencil-sketch preview was superseded by this clarification
and is not used in the profile. The final assets are deterministic SVGs rendered
from the actual photograph's sampled luminance.

`avatar_print()` in `scripts/build_profile.py` generates eight assets: light/dark,
desktop/mobile, each with animated and static versions. `picture` chooses the
correct variant. The 64 dot rows print once in 2.955 seconds. The exact reviewed
`AVATAR_STYLE` uses opacity only and is enabled only for
`prefers-reduced-motion: no-preference`. Reduced-motion users receive a static SVG;
all rows remain visible when animation is disabled or complete. Never add infinite
loops, arbitrary styles, scripts, external SVG resources, fonts, or SMIL elements.

The terminal panel shows actual contributions, active days, and refresh date from
`data/contributions.json`. These are a dated public snapshot, not live monitoring,
production health, uptime, SLA compliance, or model-evaluation metrics. Source and
pattern-data links remain available below the panel.

To update the portrait, obtain an owner-approved source, resample to 64x64
luminance levels, update the JSON provenance, and rebuild. The checked-in pattern
keeps daily builds dependency-free and avoids repeated photo downloads.
The validator accepts only the named local avatar SVGs, bounds their size to
350 KB, checks allowed SVG elements, and accepts only the exact print CSS.
No raster photo or generated pencil image is needed by README visitors.

## Add a project — one JSON entry

Edit `data/additional-projects.json` and append:

```json
{
  "id": "new-project",
  "name": "Project name",
  "url": "https://github.com/iamdpsingh/YOUR-REPOSITORY",
  "summary": "A factual description of what it does.",
  "period": "Dated observation period, if supplied",
  "stack": ["Python", "SQL"],
  "highlights": ["One carefully scoped result or implemented capability."],
  "sources": ["https://github.com/iamdpsingh/YOUR-REPOSITORY"]
}
```

Replace the example values with real data. IDs are unique lowercase hyphenated
slugs. URL must be HTTPS. Use an application link if no repository was supplied.
Optional `card_title` supplies a short display title; `name` remains the full
project name in the evidence document. Keep the visible summary to one or two
sentences so cards match the existing projects. `button` changes the button text;
`emoji` chooses the heading icon;
`badges` chooses which stack labels get small badges. The builder creates badge
URLs itself; do not enter arbitrary HTML or image URLs in project data.

Optional evidence entries retain detailed claim boundaries:

```json
{
  "id": "P1",
  "status": "IMPLEMENTED",
  "claim": "Exactly what was built or measured.",
  "scope": "What this does and does not establish, including date and open gates."
}
```

Put these objects in the project's `evidence` list. The builder creates a compact
README card and a full section in `docs/PROJECT_EVIDENCE.md`. Dates, highlights,
full stack, and the evidence link sit inside the card's native expandable
"Project details & evidence" section. The collapsed card shows just its short
title, summary, tech badges, and action button, matching the older project cards.
Add more cards freely: they are arranged in pairs, with an empty final cell when
there is an odd number. Original project cards remain in the template; they are
not removed to make room for additions.

Then run:

```sh
python3 scripts/build_profile.py
python3 scripts/validate_profile.py
python3 -m unittest discover -s tests -v
git diff --check
```

When JSON reaches `main`, the refresh workflow builds and publishes it
automatically. The old `data/projects.json` and `data/portrait.txt` are retained
as records of the previous experiment and are not rendering inputs. Do not edit
them expecting the restored profile to change.

## Evidence rules for these additions

The owner supplied six Rolewisp claims and five Immune System claims. Their
OBSERVED, IMPLEMENTED, and REPORTED labels are retained with the complete limits.
These are dated project records, not newly rerun audits.

- Rolewisp's 71/78 (91.0%) is native platform coverage with seven unmet targets.
  It is not project completion or service reliability.
- 9,187 indexed jobs is the 21 November 2026 snapshot, with 130/142 sources having
  initial success. It is not a current count or sustained throughput result.
- Closure-policy, restore-drill, account-isolation, and final-cleanup test claims
  retain their open gates and revision boundaries. Do not sum different test runs.
- The Immune System uses six implemented responsibilities, heuristic diagnosis,
  controlled simulation scenarios, five domain job families, a weighted health
  indicator, and configured reporting schedules. Do not imply verified live LLM
  calls, production incident recovery, achieved SLAs, or measured delivery gains.

During this update the supplied Immune System source files were inspected to
confirm heuristic diagnosis, risk boundaries, and domain jobs. The Rolewisp
website could not be read by the web verification tool. Preserve its provided
URL without claiming current availability or independently verified live metrics.
The original older profile's claims are restored from its source; this addition
does not independently re-audit their historical benchmarks.

## Contribution summary and artwork

`scripts/refresh_activity.py` fetches only GitHub's public contribution numbers,
checks complete dates and total consistency, and writes `data/contributions.json`.
The builder inserts a dated count above the original activity artwork. The 3D,
snake, and gitartwork graphics are preserved snapshots, explicitly labeled as
such. Retired third-party artwork generators are not reinstated.

## Build and automation boundaries

`README.md` and `docs/PROJECT_EVIDENCE.md` are generated outputs. Edit the template
or additional-project JSON instead. The builder changes only the added-card,
date-badge, contribution-summary, and avatar-print marker blocks in the template.

`validate-profile.yml` builds and checks using read-only repository access.
`refresh-profile.yml` runs daily at 03:20 UTC, manually, or after template/project/
builder changes. Its read-only render job fetches numeric GitHub data and passes
generated Markdown, evidence documentation, contribution JSON, and avatar SVGs to an
isolated trusted-main publishing job. Its script stages only those generated files,
uses the built-in token only for the push, and does not persist checkout credentials.
A concurrent update causes a safe push rejection instead of a force-push.

Actions remain pinned to verified full commit SHAs. The restored external images
are fetched by the profile viewer; no downloaded generator or arbitrary SVG code
runs with repository write access. The validator permits the reviewed original
image hosts, native HTML subset, and two original inline style strings; active
content and unknown hosts are rejected. These are guardrails, not a universal
sanitizer or a security audit of external image services and project applications.

## Review and AI handoff

Inspect the added pair of project cards in the original visual layout, check both
project URLs, verify the evidence links and limits, confirm existing project cards
remain, and run the checks. Large historical grids and hosted image failures are
properties of the restored source design, not reasons to silently redesign it.

> Read AGENTS.md and this guide. Preserve the original pre-chat layout. Add or
> update projects through data/additional-projects.json, retain every relevant
> date and evidence limit, build the README, run checks, and review the new cards.
> Keep automation permissions and action pins hardened. Do not redesign the profile.
