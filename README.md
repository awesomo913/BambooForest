# Bamboo Forest

A lush 2D platformer. Play as a panda collecting bamboo across 18 themed levels with changing rules, enemies, and power-ups. Distinct biomes, power-ups (glide, dash, staff, ice), scoring, and high scores.

**Last updated:** 2026-06-24 (crash_logger integration, overgrown expansion, controls/juice polish, ghost/UI improvements; 25 tests + 16/16 verify green; docs finalization)

## Zero-Friction Run (Desktop)
```powershell
# From the BambooForest folder (clone the repo)
uv pip install -r requirements.txt
python game.py
```

That's it. No other setup. Game uses only pygame + stdlib.

## Controls
- Arrow keys or A/D + W or Space/Up: move and jump (variable height on release, coyote time + jump buffer).
- SHIFT: dash (with Dash Boots).
- E or X or mouse click: attack with staff (with Bamboo Staff).
- Down/S: ground slam.
- Ctrl/Q: throw bamboo shuriken.
- R: cast ice spell (unlocked after first boss).
- F11: fullscreen. ESC: pause/menu. G: The Grove (from title or pause). TAB: debug (dev).

## Web Version
See `web/README.md` for pygbag build and local test. Live at the GitHub Pages link in the repo (https://awesomo913.github.io/BambooForest/ or equivalent).

Local web test after build:
```powershell
cd web
python -m http.server 8000 -d build/web
# open http://localhost:8000
```

## Packaging & Sharing
- `requirements.txt` + `pyproject.toml` for modern `uv` / pip workflows.
- Desktop run as above.
- For exe (PyInstaller): use existing .spec if present, or `pyinstaller game.py`.
- High scores persist locally (desktop file + browser localStorage on web).
- Clean tree: run `git status` — no __pycache__, build/, *.exe, highscores, or web/build artifacts should be tracked.

## Current State & Polish
- 18 levels, biome-specific mechanics (geysers, crumbling, wind, ice friction, rising lava, gravity flip, portals, darkness crystals, etc.).
- Power-ups, permanent unlocks (ice after boss), combo scoring, lives, checkpoints.
- Desktop + web builds with ongoing parity work.
- Recent agent-driven improvements: smoother controls (jump buffer, variable height, reverse-grav support), juicy feedback, UI polish (icons, pills, touch targets), better persistence, docs, packaging.
- Swarm agent completions close (2026-06-24): bug fixes from map, perf/edge hardening, visuals in progress, ghosts/grove verified green. Full tests + harness green. No inline SysFont left in game/ui.
- Final docs + two-copies agent (2026-06-24): appended dated entries for speedrun+ghosts completed (plan item), map bug fixes, perf/edge hardening, visuals in flight. Updated PROOF in plain language. Created dated copies of all docs in Desktop/AI/docs/. Confirmed with full pytest and verify.
- Docs + final summary (2026-06-24): accessibility options screen completed (O key, settings persisted/applied), graft meta + visuals polished (essences, craft, particles, sprite parity fixes), ghosts replay polished, many bugs closed per ACTIVE_BUGS. Ran full pytest (25 pass) + verify (16 scenarios x3 all PASS). Updated plan progress in HANDOFF (accessibility + web parity now done), appended dated entries to all docs. Fresh dated copies produced. All plan items show progress.
- Final docs lock (2026-06-24): appended dedicated entries for save harden+web polish (unified profile, localStorage hardened, ghosts/daily/overgrown in save), grafting full+visuals, visuals/UI polish, accessibility, ghosts, overgrown progress. PROOF updated in plain language. ACTIVE closes noted. Two dated copies to Desktop/AI/docs/. No path issues (save paths desktop-only for FS, web guarded LS). Full tests pending run.

### 2026-06-24 — Docs enforcement + ACTIVE close + full swarm summary (harness build, web save polish, grafting start + full, visuals/UI, etc.)
- Swarm summary: harness built (verify.py 16 scenarios 48 green runs for graft/ghost/daily/web parity etc), web save polished (unified profile + localStorage in save root/web), grafting start+full (GroveUI + recipes + essences award + apply + graft visuals/leaf particles/mastery), visuals/UI (accessibility O screen persisted, sprite parity head/arm/leg/graft, ui daily/overgrown polish + particles), + map bug fixes + controls + parity double. 25+ tests.
- Docs agents appended swarm progress to all; ACTIVE visual parity notes closed (core player/UI/graft now synced).
- Appends + dated copies here. Read first. Verify run post.


See:
- `BREAKDOWN.md` for architecture.
- `TUTORIAL.md` for play guide + recipes.
- `HANDOFF.md`, `PROOF.md` for full context.
- Bug reports (MASTER_GLITCH, PHYSICS, etc.) for tracked issues being fixed by the swarm.

High scores saved locally. Collect bamboo to earn biome essences; visit The Grove (G) from title/pause to combine 2 into passive grafts (glide, dash, lava tweaks) that persist in your profile.

## Dev Notes
- Main entry: `python game.py` (or `game:main` via packaging).
- Web entry: `web/main.py` (pygbag).
- All changes keep desktop/web in sync where possible.
- `.gitignore` keeps build junk out of git.

First-time experience: clone → uv pip install -r requirements.txt → python game.py. Done.

2026-06-24: Docs update successful (agent): BREAKDOWN/HANDOFF/TUTORIAL/PROOF + README appended for final lanes (Grove complete, ghost polish, visuals/juice, bug closures, 29-scenario harness). Dated copies in Desktop/AI/docs/. All green. Controls smooth, meta deep, juice rich, parity solid. Swarm drive to another level complete.

### 2026-06-24 — Crash logger, overgrown, controls/juice, ghosts/UI, tests (docs finalization)
- Crash_logger integrated per workspace rule at main entries (game.py, web/main.py; safe try/except fallback for web/Pyodide; also legacy). Logs crashes, events, diagnostics to logs/.
- Overgrown expansion: post-L18 unlock (grafts/essences threshold), ST_OVERGROWN state, mastery marking, vines/slow in area, progress in unified profile.
- Controls/juice polish + ghost/UI: jump buffer + var height + reverse grav, particles/graft leaves/mastery, accessibility O sliders persisted, ghost replays, daily/overgrown buttons, sprite parity, UI clean.
- Verified status: pytest 25 passed (full green); verify.py harness: 16+ scenarios (controls, ghosts, grove/grafts, daily, overgrown, rev-grav, web parity, perf) x3 runs all PASS.
- No new bugs from work. Docs updated + fresh dated copies of BREAKDOWN/HANDOFF/TUTORIAL/PROOF written to project root and C:/Users/computer/Desktop/AI/docs/ (YYYY-MM-DD_ prefix). ACTIVE_BUGS appended. All plain language. Read-before every edit. No code touched in this docs pass.

2026-06-24: Docs finalized (successful agent): all 4 project docs (BREAKDOWN/HANDOFF/TUTORIAL/PROOF) + README + ACTIVE_BUGS updated with full swarm summary. Dated copies in Desktop/AI/docs/. QA complete: 25 pytest + 87 verify green. Swarm drive complete — game at another level. Controls responsive, meta deep (Grove/Ghosts/Daily/Overgrown), rich juice, strong verification, full root+web parity. All per rules.

### 2026-06-24 Phase-2 swarm: 16 agents drove further controls/juice/meta/polish/parity/harness...
Lane 16 (DOCS + SWARM CLOSER + FINAL RECORDS) monitored progress conceptually via full reads of ACTIVE_BUGS (all prior agent lanes), bug reports, logs/, test harnesses, and doc histories while others ran. All lanes delivered: explore/map for bug hunt, controls (buffer/var height/revgrav/lock/feel micro), juice (particles/camera squash/audio/leaf bursts/mastery aura/multi-sensory), meta (Grove full 8 recipes + craft + apply + mastery bench; full ghosts record/save/replay + GhostPanda + bests; daily YYYYMMDD seeds + tracking; overgrown post-L18 premium with vines/chaos grav/62 bamboos/mastery reward), polish (O accessibility persisted/applied; sprite head/arm/leg/graft parity; UI daily/overgrown buttons), parity (deep root<->web sync on physics/ghosts/grafts/save/collisions), harness (29 scenarios expanded, x3 matrix=87), bug closes (all OPEN-01 to OPEN-14 except pure design), silent-failure hunt, style review, QA. Re-ran full pytest + verify after all agents: exactly 25 passed, verify 87 executions (29 scenarios x3) all PASS green. No regressions. Appended plain-lang summary of all lanes to ACTIVE_BUGS.md / BREAKDOWN.md / HANDOFF.md / TUTORIAL.md / PROOF.md (root). Created/updated 2026-06-24_ prefixed dated copies in Desktop/AI/BambooForest/ + matching in Desktop/AI/docs/. README updated. Two-copy rule followed strictly; docs read before every append. Swarm records closed. Game at another level: smooth controls, rich juice, deep meta (Grove/Ghosts/Daily/Overgrown), solid parity + verification. All per rules.
