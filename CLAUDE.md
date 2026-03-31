# Power Atlas — CLAUDE.md

## Project Overview

Power distribution visualization for CoreWeave data centers.
Multi-site tool: CSV upload for quick floor plans, live Jira/NetBox/RPP overlay for configured sites.

**Repo:** `rchairez/VO201-power-distribution`
**Primary site:** VO201 (ORD3) — DH1 Albatross, DH2 Phoenix
**Discovery doc:** `docs/discovery.md` — full architecture planning, integration research, meeting notes

## Architecture

- Vanilla JS (no framework) — keep it accessible to both devs
- ECharts for power flow visualizations (Sankey, gauges, heatmaps)
- Jira integration via jira.js library (replacing raw fetch + CORS proxy)
- NetBox integration via API proxy (token in .env, never in code)
- Data files: `src/data/{site}-{datahall}.json`
- Demos/prototypes: `demos/`

## Data Schemas

### Cabinet JSON format
```json
{
  "id": "R12",
  "row": 12,
  "cab": 3,
  "type": "compute|network|infra|special",
  "rppA": "AS01-2",
  "rppB": "BQ37-1",
  "phaseA": "2A",
  "phaseB": "1B"
}
```

### RPP naming convention
- Format: `{panel-id}-{suffix}` (e.g., `AS01-2`, `BQ37-1`)
- Suffix `-1` or `-2` = redundant feed pair
- Phase mapping via `PHASE_MAP`: values are `"1A"`, `"1B"`, `"2A"`, `"2B"`
- Floor PDU = RPP name without the suffix (e.g., `AS01-2` → floor PDU `AS01`)

### Jira integration
- `customfield_10207` = location (rack reference, format: `US-VO201.DH{n}.R{num}`)
- `customfield_10192` = hostname
- **SDA** project = dedicated clients (Albatross / DH1)
- **DO** project = standard DC Ops (Phoenix / DH2, and general)
- Ticket routing is customer-driven, not location-driven

### Site structure
- **Pods:** A1 (rows 1-12), A2 (rows 13-28), B1 (rows 29-42), B2 (rows 43-56)
- **Phases:** 1A, 1B, 2A, 2B — each RPP maps to exactly one phase
- **Rows:** 1-56 in DH1, each row has cabinets numbered sequentially

## File Ownership

Explicit ownership prevents merge conflicts. Check with the owner before editing their files.

### Romeo owns
- `src/components/floor-plan.js` — Blueprint Map parser integration
- `src/services/` — API clients (Jira, NetBox)
- `docs/` — architecture docs, discovery, meeting notes
- `demos/` — prototypes and demo visualizations
- `vite.config.js`, `package.json` — build config
- `.gitignore`, `.env.example` — project setup

### Robert owns
- `src/data/` — all site JSON data (he has the domain knowledge)
- `src/components/detail-panel.js` — rack detail view
- `src/components/rpp-panel.js` — RPP sidebar
- RPP/power mapping data — only Robert has facilities contacts
- `start-power-atlas.sh` — local dev startup

### Shared (coordinate before editing)
- `CLAUDE.md` — discuss changes, don't edit unilaterally
- `src/styles/` — CSS changes affect everything, test both themes
- `src/main.js` — entry point
- `index.html` — app shell

## Branch Strategy

- `main` = stable, deployable — **no direct pushes**
- `romeo-branch` = Romeo's work
- `robert-branch` = Robert's work
- Feature branches off `main` for specific features
- PRs required to merge into `main`

## Rules

### Code
- Never hardcode site-specific data in JS — put it in `src/data/*.json`
- Never commit API tokens or credentials — use `.env` (gitignored)
- CSS changes must work in both light and dark themes
- New libraries need agreement from both devs before adding
- Keep it vanilla JS — no React, Vue, or framework dependencies

### Data
- RPP data changes go through Robert (he validates with facilities)
- Floor plan layout data comes from CSV overheads or facilities PDFs
- Jira custom field IDs may vary by project — make them configurable, not hardcoded

### Security
- `.env` is gitignored — never commit it
- NetBox tokens, Jira credentials = env vars only
- If you see a token in code, remove it and rotate the token immediately

### Collaboration
- Check file ownership before editing someone else's files
- If you're unsure who owns a file, ask in the PR
- Update this CLAUDE.md when conventions change — it's the living architecture doc
