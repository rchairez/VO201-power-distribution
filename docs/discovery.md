# Power Atlas — Backend Discovery

**Date:** 2026-03-30
**Participants:** Romeo Patino (architecture), Robert Chairez (creator)
**Status:** Pre-build discovery — 20 backend questions completed

---

## Product Vision

### Two-Mode App
- **Quick mode** — Upload a CSV overhead sheet, get an instant interactive floor plan (Blueprint Map parser pipeline)
- **Full mode** — Pre-configured site with live Jira tickets, NetBox devices, and RPP power mapping layered on top

### Multi-Site
- Not VO201-only. Any CW data center, once facilities data is provided.
- CSV parser bootstraps a new site fast. Admin enriches it with power data and integration config. Once configured, that site is "full mode" permanently.

### The Pitch (for leadership / facilities meeting)
> "When power goes down at a site, nobody knows the blast radius — which racks are affected, which customers are impacted. This tool shows it in seconds. VO201 already has redundancy problems and frequent power issues. This is operational tooling, not a side project."

---

## Data Layer — What We Know

### Floor Plan Layout (static config)
- **Source today:** Robert's knowledge, hardcoded into HTML files
- **Format going forward:** JSON config files per site
- **Change frequency:** Mostly stable, rare expansions every few years
- **Onboarding new sites:** CSV overhead upload via Blueprint Map parser, then manual enrichment
- **Decision:** This is a config problem, not a data problem. JSON files in the repo, edited when needed.

### RPP / Power Mapping (manual entry — the hard part)
- **Source today:** Robert got this from building facilities team / NOC at VO201
- **Not in NetBox, not in SPLAT, not in Jira** — tribal knowledge
- **For other sites:** Need facilities to share RPP blueprints (likely PDF format)
- **Onboarding flow:** Get PDF from facilities -> human reads it -> enters data into the tool
- **Blocker:** Requires meeting with leadership to request facilities access/data
- **This is the most valuable data in the app.** Without it, it's a floor plan viewer. With it, it's a power distribution tool.

### Jira Tickets (live API)
- **DH1 (Albatross):** SDA project — dedicated/special client with their own Jira project
- **DH2 (Phoenix):** DO project — standard DC Ops tickets
- **Routing is customer-driven, not location-driven.** If a new dedicated client gets a data hall, that's a new Jira project.
- **Custom fields used:** `customfield_10207` (location), `customfield_10192` (hostname) — need to verify if CW-standard or project-specific
- **Backend needs:** Configurable Jira project + field mapping per site

### NetBox Devices (live API)
- **Only DH2 (Phoenix) uses NetBox today.** DH1 (Albatross) does not.
- **Unknown why** — could be client restriction (Albatross is dedicated) or Robert just didn't get to it
- **Need to ask Robert**

---

## Ownership & Deployment

### Current State
- Runs on Robert's laptop via `python3 -m http.server 8080`
- Two CORS proxies (Jira on 8098, NetBox on 8099) — localhost only
- GitHub Pages deployment exists but Jira/NetBox integration is broken there (no proxy)

### Proposed
- **New shared repo** in CW GitHub org (Romeo has access, Robert doesn't yet)
- **GitHub Pages** (CW private repo) for frontend — works without a server
- **Server space** TBD for centralized Jira/NetBox proxy — not a blocker to start
- **Romeo brings:** CW org access, Blueprint Map parser, architecture expertise
- **Robert brings:** Domain knowledge, power data, facilities relationships

### Repo Strategy
- Blueprint Map stays Romeo's standalone tool
- Power Atlas stays Robert's standalone tool
- Merged product = new third repo, jointly owned
- Robert needs to be okay with this — discuss tomorrow

---

## Notes for Robert (action items)

### Urgent
- [ ] **NetBox token exposed** — `netbox-proxy.py` line 16 has a hardcoded API token (`e7413999d0...`) committed to GitHub. Rotate immediately and move to `.env`.

### Questions to Ask Robert
- [ ] Why doesn't DH1 (Albatross) use NetBox integration?
- [ ] Are Jira custom fields (`customfield_10207`, `customfield_10192`) CW-standard or project-specific?
- [ ] Is he okay with a new shared repo in the CW org vs keeping everything in his personal repo?
- [ ] Did he use cutsheets/overhead CSVs or pure memory for the floor plan data?
- [ ] Can he set up the facilities meeting for RPP blueprints?
- [ ] The old files (`data-hall-power.html`, `data-hall-2-power.html`, `jira-test.html`, `jira-validate.html`) — still used or safe to archive?

### Facilities Meeting Prep
- **Ask:** RPP blueprints for all CW sites (or start with VO201 + 1-2 others)
- **Format:** Whatever they have — PDF, drawings, spreadsheets
- **Angle:** VO201 has power redundancy issues. This tool maps blast radius when an RPP goes down. Leadership has said "let us know what you need" — this is what we need.
- **Proof of concept:** Demo the working VO201 Power Atlas

---

## Architecture Decisions (pending)

These depend on answers from the Robert meeting:

| Decision | Options | Depends On |
|----------|---------|------------|
| Framework | Vite + Vanilla JS vs. static HTML | Robert's comfort with `npm install` |
| Data storage | JSON files vs. lightweight DB | How often power data changes |
| Jira integration | Per-site config vs. hardcoded projects | Whether custom fields are CW-standard |
| Auth | None (VPN-only) vs. basic login | Who the audience is (team vs. company) |
| Frontend merge | Blueprint Map as module vs. rewrite | Repo ownership decision |

---

## Research — GitHub Templates Reviewed

| Repo | Stars | Relevance |
|------|-------|-----------|
| NetBox | 20,123 | Data model reference for racks/power/devices |
| Tabler | 40,887 | Dashboard UI shell (sidebar + panels) |
| gridstack.js | 8,833 | Drag-and-drop grid if needed later |
| Rackula | 1,112 | Rack layout designer — closest visual match |
| netbox-topology-views | 1,021 | vis.js infrastructure maps |
| Volt Dashboard | 2,681 | Vanilla JS + Bootstrap 5 admin template |
| openDCIM | 344 | Floor plan grid with power capacity tracking |

**Decision:** Vite + Vanilla JS recommended (no framework). Final call after Robert meeting.

---

## Timeline Sketch

1. **Now:** Discovery (done), Robert meeting prep
2. **After meeting:** Finalize architecture, repo structure, ownership
3. **Phase 1:** Extract data to JSON, shared CSS/JS, kill duplication
4. **Phase 2:** Blueprint Map parser integration (CSV -> floor plan)
5. **Phase 3:** Multi-site config system, Jira/NetBox per-site setup
6. **Phase 4:** Facilities meeting -> onboard RPP data for additional sites
7. **Phase 5:** Deploy to CW org, onboard other DCTs

---

## Open Source Integration Research

47 GitHub repos evaluated across data center visualization, JS libraries, and infrastructure monitoring. Filtered to 16 worth integrating, ranked by value.

### Tier 1: Integrate Now (replace hand-rolled code)

| Library | Stars | What it replaces | Why |
|---------|-------|-----------------|-----|
| **[PapaParse](https://github.com/mholt/PapaParse)** | 12,500 | Custom CSV parsing | Battle-tested CSV parser. Handles quoted fields, streaming, Web Workers for large files. Drop-in for Blueprint Map integration. |
| **[Panzoom](https://github.com/timmywil/panzoom)** | 1,900 | Robert's hand-rolled zoom/pan | 3KB, zero deps, focal-point zoom, touch support. Works on any DOM/SVG element. |
| **[jira.js](https://github.com/MrRefactoring/jira.js)** | 474 | Raw fetch calls + jira-proxy.py | TypeScript Jira Cloud API client. Full type defs, pagination, tree-shakable. Kills the CORS proxy. |
| **[Apache ECharts](https://github.com/apache/echarts)** | 62,000 | Nothing (new capability) | Sankey diagrams for power flow (utility -> transformer -> PDU -> rack). Gauge charts for live load. Heatmaps for power density. **The ECharts Sankey diagram is the demo weapon. Show leadership power flowing from utility to rack in a live interactive chart — that's the "wow" that opens doors to facilities data.** |

### Tier 2: Integrate When Multi-Site

| Library | Stars | Role |
|---------|-------|------|
| **[vis-network](https://github.com/visjs/vis-network)** | 3,500 | Electrical distribution topology graph — click through the power chain visually |
| **[drawthe.net](https://github.com/cidrblock/drawthe.net)** | 1,000 | YAML-to-SVG diagram generation — define power topology in YAML, auto-render |
| **[Uptime Kuma](https://github.com/louislam/uptime-kuma)** | 84,700 | Health monitoring for power infrastructure endpoints (UPS, PDU mgmt, BMS) |
| **[pynetbox](https://github.com/netbox-community/pynetbox)** | ~500 | Python NetBox client — replaces hardcoded proxy, proper auth and pagination |

### Tier 3: Future / Nice-to-Have

| Library | Stars | Role |
|---------|-------|------|
| **[PDF.js](https://github.com/mozilla/pdf.js)** | 49,000 | Render facilities electrical PDFs in-browser with interactive annotations |
| **[NUT](https://github.com/networkupstools/nut)** | 2,000 | Real-time SNMP polling from PDUs/UPS — live wattage per circuit |
| **[poweriq-grafana](https://github.com/r4yfx/poweriq-grafana)** | 30 | Per-rack kW polling scripts — steal the collection pattern |
| **[LibreDWG](https://github.com/LibreDWG/libredwg)** | 305 | Parse AutoCAD DWG files if facilities sends drawings in DWG format |
| **[netbox-floorplan-plugin](https://github.com/netbox-community/netbox-floorplan-plugin)** | 109 | Pull rack positions from NetBox instead of hardcoding — if CW adopts it |
| **[Fabric.js](https://github.com/fabricjs/fabric.js)** / **[Konva.js](https://github.com/konvajs/konva)** | 29K / 11K | Drag-and-drop floor plan editor — only if we want an admin UI for building layouts |
| **[GElectrical](https://github.com/manuvarkey/GElectrical)** | 103 | Circuit analysis — load balancing, voltage drop. Power engineering, not just visualization. |

### What We're Skipping (and why)

| Skipped | Reason |
|---------|--------|
| Grafana (embed) | Too heavy to embed — better as a separate tool sharing data sources |
| Socket.IO | No real-time sensor data yet — premature |
| Ralph CMDB | Overlaps with NetBox, CW already uses NetBox |
| GridStack / Muuri | Dashboard widget layout — not needed until many widgets exist |
| Leaflet (indoor) | Cool for indoor mapping but current grid approach works fine |
| D3.js (raw) | Too low-level — ECharts gives you more out of the box |

### Phase 1 Integration Plan

Start with 4 libraries that replace hand-rolled code with maintained alternatives:

1. **PapaParse** — CSV parsing (Blueprint Map integration path)
2. **Panzoom** — zoom/pan (replace custom implementation, 3KB)
3. **jira.js** — Jira API (kill the proxy script, typed client)
4. **ECharts** — power flow Sankey + gauges (the wow factor for facilities pitch)

Everything else comes after multi-site architecture is settled.

---

## Demo: ECharts Sankey Power Flow

**Built:** 2026-03-30 — working prototype using real DH1 Albatross data.

**Local URL:** `file:///Users/rpatino/VO201-power-distribution/demos/sankey-power-flow.html`

**Repo path:** `demos/sankey-power-flow.html` (on `romeo-branch`)

**What it shows:**
- **Full Flow view** — Utility Feed → UPS Bus 1/2 → Phase 1A/1B/2A/2B → 16 Floor PDUs → 4 Pods → Rack Groups
- **By Phase view** — Each phase fanning out to its PDUs and downstream racks
- **By Pod view** — DH1 Albatross → 4 pods (A1/A2/B1/B2) → phases per pod → racks

**Uses real data from Robert's code:**
- 123 RPP names from `PHASE_MAP`
- Real phase assignments (1A, 1B, 2A, 2B)
- 56 floor PDUs extracted from RPP naming
- 4 pods (A1: rows 1-12, A2: rows 13-28, B1: rows 29-42, B2: rows 43-56)
- 832 compute nodes

**Interactive features:**
- Hover any link → highlights the full upstream/downstream path
- Click any node → detail panel shows blast radius (total downstream units affected if that node fails)
- Click "Phase 2A" → see exactly how many racks go dark
- 3 toggle views (Full Flow / By Phase / By Pod)
- Draggable nodes

**Why this matters for the facilities meeting:**
The ECharts Sankey diagram is the demo weapon. Show leadership power flowing from utility to rack in a live interactive chart — that's the "wow" that opens doors to facilities data. Start the demo by clicking a Phase node and showing the blast radius number. "If this phase goes down, X racks are affected — and we can show this for every site if facilities shares their RPP blueprints."

---

## Notes for Robert Meeting (2026-03-31)

### Agenda
1. **Demo the Sankey** — open `file:///Users/rpatino/VO201-power-distribution/demos/sankey-power-flow.html`, show all 3 views, click blast radius
2. **Discuss the merge** — Romeo's Blueprint Map (CSV parser) + Robert's Power Atlas (live data overlays) = new shared product
3. **Facilities meeting plan** — pitch: "VO201 has power redundancy issues. We built a blast radius tool. We need RPP blueprints to roll it out."
4. **Repo ownership** — new shared repo in CW GitHub org? Romeo has org access, Robert doesn't yet.
5. **Vibe coding workflow** — Robert is vibe coding the whole app. Discuss getting him on Claude Code so we can collaborate more efficiently. Benefits:
   - **Claude Code** — Robert can describe what he wants and get working code. Same tool Romeo uses. Shared CLAUDE.md in the repo means both devs get the same context/rules.
   - **Shared CLAUDE.md** — put project conventions, data schemas, and RPP naming rules in the repo's `CLAUDE.md`. Both Romeo and Robert's Claude sessions auto-load it. No more tribal knowledge stuck in one person's head.
   - **GitHub Copilot** — if Robert uses VS Code, Copilot autocompletes in-context. Lower barrier than Claude Code but less powerful.
   - **Cursor** — VS Code fork with AI built in. Good middle ground — visual editor + AI chat side panel. Robert might prefer this if he's more visual.
   - **v0.dev** (Vercel) — paste a description, get a React component. Good for quick UI prototyping but locks you into React.
   - **Recommendation:** Get Robert on **Claude Code** + a shared `CLAUDE.md` in the repo. That way both of you vibe code with the same project context, and the CLAUDE.md becomes the living architecture doc.
6. **Open questions** — see "Questions to Ask Robert" section above

### Action Items for Robert (before meeting if possible)
- [ ] Rotate the exposed NetBox token in `netbox-proxy.py`
- [ ] Check if Jira custom fields (`10207`, `10192`) are CW-standard
- [ ] Think about whether a new shared repo works for him

### What Romeo Brings to the Table
- Blueprint Map parser (site-agnostic CSV → floor plan)
- CW GitHub org access
- Architecture plan (this doc)
- ECharts Sankey demo (already built with Robert's real data)

### What Robert Brings to the Table
- Working Power Atlas prototype (Jira + NetBox integration)
- VO201 tribal knowledge (RPP mappings, facilities contacts)
- Relationship with leadership for facilities data request

---

## Shared CLAUDE.md — Vibe Coding Together Without Conflicts

### What is it
A `CLAUDE.md` file in the repo root that Claude Code auto-loads every session. Both Romeo and Robert get the same project context, conventions, and rules — so their AI sessions produce consistent, compatible code instead of conflicting approaches.

### Why it matters
Right now Robert's app has duplicated CSS, inconsistent patterns between DH1 and DH2, and tribal knowledge baked into code. That's what happens when one person vibe codes alone. Two people vibe coding without shared context doubles the problem. A shared CLAUDE.md is the single source of truth that keeps both devs (and their AI) aligned.

### Recommended contents for Power Atlas CLAUDE.md

```markdown
# Power Atlas — CLAUDE.md

## Project Overview
Power distribution visualization for CoreWeave data centers.
Multi-site tool: CSV upload for quick floor plans, live Jira/NetBox/RPP overlay for configured sites.

## Architecture
- Vanilla JS (no framework) — keep it accessible to both devs
- ECharts for power flow visualizations (Sankey, gauges, heatmaps)
- Jira integration via jira.js library
- NetBox integration via API proxy
- Data files: src/data/{site}-{datahall}.json

## Data Schemas
### Cabinet JSON format
{ id, row, cab, type: "compute"|"network"|"infra"|"special", rppA, rppB, phaseA, phaseB }

### RPP naming convention
Format: {panel-id}-{suffix} (e.g., AS01-2, BQ37-1)
Suffix -1 or -2 = redundant feed pair
Phase mapping in PHASE_MAP: "1A", "1B", "2A", "2B"

### Jira custom fields
- customfield_10207 = location (rack reference, format: US-VO201.DH1.R{num})
- customfield_10192 = hostname
- SDA project = dedicated clients (Albatross)
- DO project = standard DC Ops

## File Ownership (conflict avoidance)
Romeo owns:
- src/components/floor-plan.js (Blueprint Map parser integration)
- src/services/ (API clients)
- docs/
- demos/
- vite.config.js, package.json

Robert owns:
- src/data/ (all site JSON data — he has the domain knowledge)
- src/components/detail-panel.js (rack detail view)
- src/components/rpp-panel.js (RPP sidebar)
- RPP/power mapping data (only Robert has facilities contacts)

Shared (coordinate before editing):
- CLAUDE.md (discuss changes first)
- src/styles/ (CSS changes affect everything)
- src/main.js (entry point)
- index.html (app shell)

## Branch Strategy
- main = stable, deployable
- romeo-branch = Romeo's work
- robert-branch = Robert's work
- Feature branches off main for specific features
- PRs required to merge into main — no direct pushes

## Rules
- Never hardcode site-specific data in JS — put it in src/data/*.json
- Never commit API tokens or credentials — use .env (gitignored)
- RPP data changes go through Robert (he validates with facilities)
- New libraries need agreement from both devs before adding
- CSS changes must work in both light and dark themes
- Every new component needs a clear owner in the File Ownership section above
```

### Conflict avoidance strategy

| Problem | Solution |
|---------|----------|
| Both edit the same file | **File ownership** in CLAUDE.md — each dev owns specific files. Claude Code reads this and avoids touching the other person's files. |
| Inconsistent code style | **Rules section** — Claude follows these automatically. Both devs get the same patterns. |
| Data schema drift | **Data Schemas section** — one format, documented. Claude validates against it. |
| Merge conflicts on main | **Branch strategy** — each dev works on their own branch, PRs to merge. Never push directly to main. |
| One dev adds a library the other doesn't know about | **Rule: new libraries need agreement** — prevents dependency surprises. |
| RPP data changes without validation | **Rule: RPP changes go through Robert** — he's the domain expert with facilities contacts. |
| Stale CLAUDE.md | **Rule: discuss changes first** — CLAUDE.md is shared territory, both devs update it together. |

### How to pitch this to Robert
"Instead of explaining the project to Claude every session, we put the rules in a file and Claude reads them automatically. Your sessions and my sessions both follow the same playbook. If you add a new RPP naming convention, you update CLAUDE.md once and my Claude knows about it too. No more 'oh I didn't know you changed that.'"

---

## Additional Meeting Recommendations

### 1. Career angle — frame it right
This isn't a side project. Both Romeo and Robert are pursuing engineer titles at CW. Building an internal tool that leadership uses is exactly the kind of initiative that gets promoted. Frame it: "You built the prototype, I'm helping scale it. This goes on both our performance reviews. We both win."

### 2. Demo script for leadership (rehearse with Robert)
Don't wing the leadership demo. Three steps, 5 minutes:
- **Step 1:** Open Power Atlas → "This is what Robert built. Interactive floor plan with live Jira tickets overlaid on racks."
- **Step 2:** Open Sankey → "This is where it's going. Click a phase — see the blast radius. How many racks go dark."
- **Step 3:** The ask → "We need one thing from facilities: RPP blueprints. PDF is fine. We handle the rest."

Rehearse this before the real meeting. Robert demos his app (he built it, he should own that moment). Romeo demos the Sankey and the multi-site vision.

### 3. Communication cadence
We're at different sites. Decide:
- **How often do we sync?** Recommendation: weekly 15-min call. Low overhead, keeps momentum.
- **Where do we track work?** Recommendation: GitHub Issues on the repo. Simple, tied to the code.
- **How do we handle blockers?** Recommendation: text/Slack for urgent, GitHub Issues for async.
- **Where do we discuss design decisions?** Recommendation: PRs for code, `docs/` folder for architecture (like this doc).

### 4. Migration strategy — don't break what works
Robert's app works today. Worst thing we can do is rewrite it and break it. Agree on this order:
1. **Don't touch main** until new structure is proven on a branch
2. **Extract data first** — JSON files from the hardcoded HTML (lowest risk, highest value)
3. **One file at a time** — pull shared CSS into a file, test, merge. Then shared JS. Then kill iframes.
4. **Robert keeps his local workflow** until the Vite setup is proven
5. **Always keep a working version** — if the refactor breaks things, revert. Ship > perfect.

### 5. 30-day milestone plan
Set concrete targets so this doesn't become a "someday" project:

| Week | Milestone | Owner |
|------|-----------|-------|
| Week 1 (Apr 1-7) | Repo in CW org, CLAUDE.md merged, branches set up, NetBox token rotated | Romeo + Robert |
| Week 2 (Apr 8-14) | Data extracted to JSON files, shared CSS split out, dark mode via CSS variables | Romeo (code) + Robert (data validation) |
| Week 3 (Apr 15-21) | Sankey integrated into main app, Blueprint Map parser wired up (CSV upload) | Romeo |
| Week 4 (Apr 22-28) | Demo to leadership, request facilities meeting for RPP blueprints | Robert (lead) + Romeo (support) |

### 6. Fallback positions (if Robert pushes back)

| If Robert says no to... | Fallback |
|--------------------------|----------|
| New shared repo | Work on his repo — Romeo contributes via PRs from a fork |
| Claude Code | He keeps vibe coding his way, Romeo handles architecture and reviews PRs |
| Vite / build step | Keep `python3 -m http.server` — just extract data to JSON (still a huge win) |
| Merging with Blueprint Map | Keep them separate — just agree on shared data formats so they're compatible later |
| 30-day timeline | Agree on Week 1 only. Ship one thing, then plan the next. |

**The only non-negotiable:** Rotate that NetBox token. It's in a public repo.

### 7. Ask Robert what HE wants
Romeo has been planning the vision. Flip it. Ask Robert:
- "What do you wish this app could do that it can't?"
- "What's annoying about maintaining it?"
- "What would make your daily job easier?"
- "If you could show leadership one thing, what would it be?"

His answers might redirect the whole scope. **The tool should solve Robert's pain point first — everything else is bonus.**

---

## The Feature That Makes This Exceptional: Single-Point-of-Failure Detector

### The problem
VO201 has known power redundancy issues. Every rack is supposed to have two independent power feeds (A and B) on different RPPs, different phases, different UPS buses. But nobody is systematically checking whether that's actually true. When it's not — and a single RPP fails — racks that should survive go dark because both feeds were on the same failure domain.

### The feature
Scan every rack automatically and flag power redundancy problems:

| Health | Condition | What it means |
|--------|-----------|---------------|
| **RED** | Both A+B feeds on the same RPP | Single point of failure — one panel dies, rack goes completely dark |
| **ORANGE** | Both feeds on the same phase | Phase failure kills both feeds simultaneously |
| **YELLOW** | Both feeds on the same UPS bus | Bus failure kills both feeds |
| **GREEN** | Different RPP, different phase, different bus | Fully redundant — survives any single failure |

### Why it's realistic — the data already exists
Robert's code already has:
- `COMPUTE_NODES[]` with `rpp` and `phase` per node (A and B feeds)
- `PHASE_MAP` mapping every RPP to its phase (1A, 1B, 2A, 2B)
- UPS bus derivable from phase (1x = Bus 1, 2x = Bus 2)

No new data sources. No API calls. Pure client-side analysis of data Robert already hardcoded. This could be built in a single session.

### What it looks like in the app
- **Floor plan overlay** — racks glow red/orange/yellow/green based on redundancy health
- **Summary bar** — "47 racks RED / 12 ORANGE / 8 YELLOW / 765 GREEN"
- **Click a red rack** — detail panel shows: "Feed A: RPP AS01-2 (Phase 2A) / Feed B: RPP AS01-1 (Phase 2A) — SAME RPP, SAME PHASE"
- **Filter mode** — toggle to show only red racks, or only racks on a specific RPP
- **Export** — CSV of all flagged racks for a remediation ticket

### Why this is the killer feature
1. **Finds real problems** — not theoretical, actual miscabled or poorly planned racks that will fail
2. **Sells the facilities pitch** — "We found 47 racks with single points of failure at VO201. Give us the blueprints and we'll audit every site."
3. **No new data needed** — works today with Robert's existing data
4. **Operational value** — DCTs and NOC can use this during incidents to predict cascading failures
5. **Differentiator** — NetBox doesn't do this. No CW tool does this. This is net new.

### Implementation sketch
```javascript
function analyzeRedundancy(nodes) {
  const rackHealth = {};
  // Group nodes by rack (row + cab)
  const byRack = groupBy(nodes, n => n.row + '-' + n.cab);

  Object.entries(byRack).forEach(([rackId, rackNodes]) => {
    const rpps = [...new Set(rackNodes.map(n => n.rpp))];
    const phases = [...new Set(rackNodes.map(n => n.phase))];
    const buses = [...new Set(phases.map(p => p.charAt(0)))]; // '1' or '2'

    if (rpps.length === 1) {
      rackHealth[rackId] = { level: 'RED', reason: 'Both feeds on same RPP: ' + rpps[0] };
    } else if (phases.length === 1) {
      rackHealth[rackId] = { level: 'ORANGE', reason: 'Both feeds on same phase: ' + phases[0] };
    } else if (buses.length === 1) {
      rackHealth[rackId] = { level: 'YELLOW', reason: 'Both feeds on same UPS bus: ' + buses[0] };
    } else {
      rackHealth[rackId] = { level: 'GREEN', reason: 'Fully redundant' };
    }
  });
  return rackHealth;
}
```

### Add to meeting agenda
Tell Robert: "Your app already has the data to find single points of failure across the entire floor. We can light up every at-risk rack in red. That's the slide that gets facilities to hand over blueprints for every site."

---

## Meeting Checklist (print this or have it open)

- [ ] Open Sankey demo: `file:///Users/rpatino/VO201-power-distribution/demos/sankey-power-flow.html`
- [ ] Open Power Atlas: `file:///Users/rpatino/VO201-power-distribution/VO201-power-distribution.html`
- [ ] Have this doc open: `file:///Users/rpatino/VO201-power-distribution/docs/discovery.md`
- [ ] Topics to cover:
  - [ ] Demo Sankey (3 views + blast radius)
  - [ ] Merge discussion (Blueprint Map + Power Atlas)
  - [ ] Facilities meeting plan + pitch script
  - [ ] Repo ownership (new shared repo in CW org?)
  - [ ] Vibe coding workflow (Claude Code + shared CLAUDE.md)
  - [ ] CODEOWNERS / file ownership
  - [ ] Communication cadence (weekly sync + GitHub Issues)
  - [ ] Migration strategy (don't break what works)
  - [ ] 30-day milestones
  - [ ] Single-point-of-failure detector — the killer feature pitch
  - [ ] Ask Robert what he wants
- [ ] Action items to assign:
  - [ ] Robert: rotate NetBox token
  - [ ] Robert: check if Jira custom fields are CW-standard
  - [ ] Robert: schedule facilities meeting
  - [ ] Romeo: move repo to CW org (if agreed)
  - [ ] Romeo: set up branch protection + CODEOWNERS enforcement
  - [ ] Both: agree on Week 1 milestone

---

*Last updated: 2026-03-30 by Romeo Patino*
