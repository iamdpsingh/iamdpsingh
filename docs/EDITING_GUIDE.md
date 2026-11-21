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

## Focused engineering additions

The owner supplied further creative ideas. The additions deliberately preserve the
restored header, technology grids, and compact project cards:

- A local static project DAG shows three factual paths: job sources through Python /
  PostgreSQL to Rolewisp; fleet telemetry through Pub/Sub / Dataflow to fleet
  analytics; pipeline signals through Python / PySpark to the Immune System.
  It describes selected project architecture, not an executing orchestrator.
- An expandable SQL bio is a runnable, self-contained SELECT with a matching
  Markdown result table. It is an illustration, not a query against a real profile DB.
- `data/capabilities.json` describes documented capabilities. Its explicit
  `callable_mcp_server: false` must remain unless an actual server is separately
  implemented and verified. Do not add aspirational tools as proven skills.

`engineering_profile()` in the builder generates four tiny SVG assets: light/dark
and desktop/mobile. Native `picture` selects the variant; actual project links
remain outside the image because SVG image nodes cannot act as website buttons.
No scripts, external SVG resources, fonts, or animation are added. The image
validator accepts exactly these local filenames and validates their SVG content.

The original current theme remains; the new light variant uses neutral paper/ink
and the dark variant follows the charcoal/orange identity. Edit the path definitions
in the builder and rerun it to update the diagram. Edit the capability JSON to
update the expandable manifest. The diagram is not a runtime health monitor.

Do not invent token usage, latency, eval pass rates, SLA compliance, or claim that
coding activity proves production uptime. Such telemetry would require an actual
project measurement source, units, and timestamps. A staged agent demonstration
must not be presented as a real private thought trace. No such trace is added here.

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
date-badge, contribution-summary, and engineering-profile marker blocks in the template.

`validate-profile.yml` builds and checks using read-only repository access.
`refresh-profile.yml` runs daily at 03:20 UTC, manually, or after template/project/
builder changes. Its read-only render job fetches numeric GitHub data and passes
only generated Markdown, evidence documentation, and contribution JSON, and the four generated DAG assets to an
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
