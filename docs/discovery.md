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

*Last updated: 2026-03-30 by Romeo Patino*
