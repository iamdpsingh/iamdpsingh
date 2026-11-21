# Profile editing guide

This document is the handoff for any AI tool or human editor. Read `AGENTS.md`
first, then the complete `README.md`. No framework, build step, package manager,
API key, or network access is needed to edit or validate this profile.

## Repository map

- `README.md`: public GitHub profile and source of truth for visible content.
- `assets/profile-banner.svg`: original static vector hero, editable as XML.
- `assets/project-*.svg`: three original project covers.
- `assets/link-*.svg`: local Portfolio, LinkedIn, and Email button graphics.
- `assets/toolkit.svg`: compact visual overview of the main technology groups.
- `scripts/validate_profile.py`: offline structural and content guardrails.
- `tests/test_validate_profile.py`: security regression tests.
- `.github/workflows/validate-profile.yml`: read-only checks on pushes and PRs.
- `.github/dependabot.yml`: monthly GitHub Actions update proposals.
- `AGENTS.md`: concise instructions discoverable by AI coding agents.
- `assets/stats.svg`, `assets/streak.svg`, `assets/top-langs.svg`,
  `profile-3d-contrib/`, `gitartwork.svg`, `.github/profile-3d-settings.json`:
  preserved legacy snapshots/configuration. Not displayed or refreshed.

## Visual direction

The concept is a **data control room**: a website-style portfolio inside GitHub,
with an oversized typographic hero, warm red/orange light, layered data geometry,
original project covers, and compact contact buttons. This richer presentation
restores the visual energy of the earlier profile while using only local artwork.
All illustrations are original editable SVG primitives, not remote widgets.

Keep the existing palette:

| Purpose | Color |
| --- | --- |
| Banner background | `#050505` |
| Red accent | `#EF4444` |
| Orange accent | `#F97316` |
| Primary text on banner | `#FFFFFF` |
| Secondary text on banner | `#B7B7BF` |
| Subtle rules | `#252525` |

GitHub controls the surrounding page background, link colors, and typography.
The banner retains the dark theme in both GitHub light and dark modes; the rest
uses native Markdown for readability in either mode. Do not try to override the
GitHub canvas with inline styles. Never add a stylesheet, script, iframe, or app
framework to make a profile README behave like a website.

Keep one hero, three selected projects with covers, and three main sections (selected work,
toolkit, background). Use native `details`/`summary` for secondary material.
Avoid layout tables, full-width Unicode headings, badge walls, repeated calls to
action, counters, animated separators, and competing activity widgets. Tables
are appropriate for actual data such as this palette.

The hero uses a `1080 × 420` viewBox and `width="100%"` in the README. It is static
and uses installed system font fallbacks. The banner's small labels are secondary;
all essential identity, project details, and contact links must remain real text
below the image so they stay readable at narrow widths and with screen readers.

## Typical edits

### Change profile copy or contact details

Edit `README.md` directly. The name, existing contact destinations, education,
and historical role come from the original repository. Verify new claims with
the owner before changing them. Keep dates explicit. Never infer ongoing
employment or availability from the current date.

### Add or feature a project

Add a concise link and description to the expandable project list. To feature it,
replace one of the three selected projects instead of increasing the count.
Describe the system's purpose and add a plain-text technology flow. Prefer the
repository as the durable destination; a demo can be a secondary link.

There is no fixed limit on the expandable catalog. The original ten linked
software/data projects are retained across the three featured entries and the
catalog, alongside three individually listed hardware projects. Keep earlier
entries when adding new work unless the owner asks to remove them.

To add another project, find `Explore previous projects` in `README.md` and
insert a bullet under the relevant group, before `</details>`:

```markdown
- **[Project name](https://github.com/iamdpsingh/REPOSITORY-NAME)** — one sentence explaining what it does and the main technologies.
```

Replace both placeholders with the real project details; do not publish the
example as an entry. For hardware work without a supplied repository URL, use a
bold project name and description instead of inventing a link. No script or
workflow update is necessary when adding a project.

Do not add performance figures, production-readiness claims, or merged/open-source
contribution claims without supporting repository evidence. The earlier profile
contained numerical claims without benchmark context; the redesign describes
capabilities instead. The Databricks dataset remains explicitly synthetic.

### Edit the artwork

Edit the local SVG directly. Keep its title, namespace, viewBox,
contrast, and text margins. Use SVG primitives, local gradients, and system fonts.
Do not use embedded HTML, external images/fonts, animation, event handlers,
links, DTDs, or entities. Update the README alt text if the meaning changes.
Preview wide and narrow layouts before delivery. The three project covers use
`1080 × 240` viewBoxes, the toolkit uses `1080 × 220`, and the contact graphics use
`168 × 48` (displayed at `110 × 32` to fit three across on mobile). Contact button
SVGs are images wrapped in ordinary HTML links; do not draw fake controls with no
link. Keep the alt text equal to the visible label. Artwork is static by design.

The validator's `PROFILE_ARTWORK` set explicitly lists the eight reviewed assets.
Keep one hero and avoid duplicate images. Changing the number of featured
projects or adding artwork requires a deliberate design and validation update.
Adding ordinary entries to the expandable catalog needs only a Markdown edit.

### Run checks

From the repository root:

```sh
python3 scripts/validate_profile.py
python3 -m unittest discover -s tests -v
git diff --check
```

The validator intentionally accepts a small Markdown/HTML/SVG subset. Use inline
Markdown links, reviewed local SVG images with meaningful alt text, and the native
HTML elements already present. It checks local path containment (including
symlinks), permitted link schemes, basic structure, and active SVG constructs.
It is a regression guard, not a general-purpose sanitizer or security audit.
It does not fetch external URLs, prove destination trust, validate project claims,
or inspect archived assets. Review any changes to these checks manually.

Preview the Markdown using a GitHub-compatible renderer. Check that project and
contact links are usable, disclosure sections open with keyboard controls, the
banner does not clip, and narrow screens need no horizontal scroll. A local
preview cannot guarantee GitHub's exact final rendering; check it after publishing.

## Security model and changes

There is no application server, login, database, or deployed runtime here.
The relevant surfaces are public profile content, SVG assets, external links,
and GitHub Actions. The redesign removes third-party image services and tracking
pixels from the visible profile. All rendered artwork is checked-in source.

The old daily README updater downloaded third-party SVGs and automatically
changed availability. It and all four generator/update workflows were removed.
The replacement workflow only validates; it requests `contents: read`, disables
checkout credential persistence, has a five-minute timeout, and cannot publish
changes. The checkout action is pinned to the verified v6.1.0 commit;
Dependabot proposes maintenance updates for review. No personal access token is
needed. Generated contribution snapshots remain untouched for reference.

These choices follow [GitHub's secure use guidance](https://docs.github.com/en/actions/reference/security/secure-use).
Do not restore write-enabled generators merely to display activity artwork.
If the owner requests automation later, document its exact data source,
permissions, output path, dependency pins, and failure behavior first.

Never put credentials in Markdown, SVG, scripts, or workflow files. `.gitignore`
excludes local environment files and common local artifacts, but does not remove
anything already in Git history. This work does not change repository settings,
branch protection, historical commits, existing secrets, or hosted demo security.
Those require their own access and review. A public email remains public.

## Ready-to-use AI handoff

> Read AGENTS.md and docs/EDITING_GUIDE.md, then inspect the entire README and
> local banner. Make the requested edit while preserving the dark/red/orange
> data-control-room identity and minimal layout. Keep factual claims grounded
> in the owner's supplied information. Use native GitHub Markdown and static
> local SVG only. Run the validator, regression tests, and diff whitespace check;
> inspect the rendered result if layout changes. Report changed files and any
> checks you could not run. Do not publish without an explicit request.
