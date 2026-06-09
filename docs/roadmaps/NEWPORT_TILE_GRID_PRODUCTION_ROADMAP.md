# Newport Tile Grid Production Roadmap

Milestone: `NTG-1 Newport Tile-Grid Foundational Map Production Gate`

Source authorization: Chris June 2026 directive — map the entire starting
village (1700s Newport, RI) as a square grid where every square carries a
semantic value (water, dock, road, grass, dirt, lot, building footprint,
prop anchor), crosswalk every atelier artwork to grid values, compose the
village from that single source of truth, and ship an itch.io-ready Godot
web ZIP at production quality.

Structured source:
`docs/roadmaps/NEWPORT_TILE_GRID_PRODUCTION_ROADMAP.json`

Predecessor milestone: `OVI-1` (G-14 through G-22, complete; PR #494/#495
merged). NTG-1 supersedes rect-based runtime placement with a true
tile-grid source of truth while preserving the G-19R measured blockout as
design input.

## North Star

Wayfarer's starting village must read as a lively 1700s colonial harbor
town at the craft bar of Tibia and Ragnarok Online: readable streets,
memorable districts, grounded buildings on believable lots, a waterfront
that works, and atelier-standard art everywhere a player can look. The
grid is not a debug structure — it is the authored skeleton that makes
seamless, cohesive composition possible.

## Engine Decision (Assessed This Milestone)

**Verdict: continue with Godot 4.x. Do not migrate.**

| Criterion | Godot 4.6 | Unity | Phaser/JS | GameMaker |
| --- | --- | --- | --- | --- |
| 2D tile-grid support | First-class (`TileMapLayer`, terrain autotiling, custom data layers, multi-tile scene tiles) | Adequate but heavier | Manual/code-driven | Good but paid license |
| HTML5 export for itch.io | Built-in, proven in this repo (G-21 hardened ZIP pipeline) | Large/slow web builds | Native web | Built-in, paid |
| Cost/licensing | Free, MIT | Runtime-fee history, account churn | Free | Subscription |
| Existing investment | ~495 merged PRs, validators, capture tooling, atelier pipeline | Zero | Zero | Zero |

Godot's `TileMapLayer` + TileSet terrain system is purpose-built for exactly
the square-value architecture Chris described, and the existing browser
packaging (`tools/package_itch_web.sh`) already produces itch-compatible
ZIPs with root `index.html`. Migration would discard a working pipeline for
no capability gain. Re-assess only if a hard blocker appears (none known).

## Core Architecture (Locked for NTG)

1. **One grid, one truth.** A single authored grid file
   (`data/world_layout/newport_master_grid_v1.json` + human-reviewable CSV
   and color-coded PNG preview) assigns every square a semantic tile ID.
   Godot scenes are generated/validated from it; no layout may be invented
   directly in the editor.
2. **Tile = character footprint.** One grid square equals one standing
   character, Tibia-style. Recommended authoring size: 64 px per square at
   current art resolution. The G-19R rule "primary avenue fits 10–15
   characters shoulder to shoulder" therefore means 10–15 squares of road
   width, reconciled against the existing 360 px avenue target in NTG-0.
3. **Crosswalk manifest.** Every atelier asset maps to one or more semantic
   tile IDs via `data/world_layout/newport_art_crosswalk_v1.json`:
   ground/terrain art → terrain tile IDs; buildings → multi-square
   footprints (width × depth in squares, door squares, collision squares,
   draw anchor); props → prop-anchor squares with function tags.
4. **Multi-square buildings are first-class.** Buildings declare footprints
   sized believably against road width and character scale (e.g., tavern
   6×5 squares, rowhouse 3×4, church 8×10). No building may exist without a
   lot in the grid.
5. **Layer order is fixed:** water/landform → terrain ground → roads/docks
   → lots/buildings → props → NPC stations. Per AGENTS.md, structure before
   decoration; props never hide ground problems.

## Phase Sequence

| Phase | Title | Required Result |
| --- | --- | --- |
| NTG-0 | Source Reconciliation + Grid Spec Lock | Reconcile Chris's local `wayfarer_newport` working copy with this repo (Chris pushes or confirms GitHub is current); lock tile size, map dimensions in squares, semantic tile taxonomy, and avenue-width reconciliation with G-19R. Produces the grid specification document and validator. |
| NTG-1 | Master Grid Authoring | Author the full Newport grid from the G-19R measured blockout: every square assigned (water, shoreline, wharf/dock, road hierarchy tiers, alley, grass, dirt, yard, lot, civic space, blocked). Deliver JSON + CSV + color-coded PNG preview for Chris-readable review. Validator fails orphan squares, unreachable roads, and lotless building zones. |
| NTG-2 | Art-to-Grid Crosswalk + Gap Analysis | Map all existing atelier assets (235 PNGs in `art_pipeline/`) to tile IDs and building footprints with provenance intact. Produce a gap list of missing art (terrain transitions, building sizes, props) as the art production queue. No placeholder may enter the crosswalk. |
| NTG-3 | Terrain TileMap Implementation | Build the Godot TileSet with terrain autotiling for seamless ground transitions (grass/dirt/cobble/sand/water edges) and generate `TileMapLayer` ground from the master grid. Screenshot proof must show zero patchwork seams. |
| NTG-4 | Building Footprint Placement | Place all buildings from the crosswalk footprint registry onto their grid lots: correct multi-square sizing vs roads and characters, door squares on street frontage, collision from footprint data, Y-sorted depth so characters walk believably in front/behind. |
| NTG-5 | Props + Street Furniture Layer | Place function-first props (market stalls, barrels, signage, lampposts, rigging) on prop-anchor squares only. Per durable rules: no random scatter, no clutter hiding layout problems. |
| NTG-6 | Walkability + NPC Route Validation | Derive the collision/navigation map from the grid; prove every road, alley, dock, and civic space is walkable, every door reachable, and NPC stations/routes valid against the grid. Automated path checks + runtime proof. |
| NTG-7 | Cohesion + Atelier Visual QA | Full-town screenshot sweep against the Newport Review Bar (harbor read, waterfront avenue, uphill roads, back street, district legibility, unified ground language). Agent Council review; target 8.5+/10. Screenshot contradiction fails the phase. |
| NTG-8 | itch.io Production Build Gate | Export web build, package via `tools/package_itch_web.sh` (root `index.html`, versioned ZIP), capture browser canvas proof with clean console, run the regression gate, and assemble the Chris review package. Hard stop for Chris review. |

## Autonomous Production Loop

Each phase follows the established loop: preflight → focused branch →
implement → validate → screenshot/runtime proof → Agent Council →
fix-or-pass → PR → merge when green per the standing autonomous merge
authorization → ledger update → next phase. NTG-0 requires one Chris
input (local-folder reconciliation, below) before the runway starts;
NTG-8 is the formal Chris review milestone.

## Per-Phase Evidence Requirements

- Updated execution ledger row with branch, PR, commit, status, evidence.
- Validators added/passing (`validate_ntg*` scripts, repo convention).
- Screenshot proof with HUD/debug disabled for all visual phases.
- Atelier provenance maintained for every asset entering the crosswalk.
- Agent Council report with an allowed final verdict.

## Hard Dependencies / Chris Inputs

1. **Local working copy (blocking NTG-0):** The directory
   `C:\Users\Chris\Documents\Wayfarer v2\Projects\wayfarer_newport` on
   Chris's PC is not visible to the remote agent. If it contains art or
   layout work newer than this repository, it must be pushed to GitHub
   (any branch) or confirmed as already represented here before grid
   authoring begins. Working from stale sources would silently discard
   that work.
2. **Tile size confirmation (NTG-0):** Recommended 64 px/square with
   character = 1 square footprint. Chris may override at spec lock; the
   choice cascades into every footprint in the crosswalk.

## Ledger

Execution ledger:
`docs/reports/NEWPORT_TILE_GRID_EXECUTION_LEDGER.md` (created at NTG-0).
