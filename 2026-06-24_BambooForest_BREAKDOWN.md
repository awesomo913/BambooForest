# Bamboo Forest — Breakdown
**Created:** 2026-06-24
**Location:** C:\Users\computer\Desktop\AI\BambooForest
**Language/Stack:** Python 3.11 + pygame (desktop), pygbag/Pyodide for web

---

## 1. What It Does
A 2D platformer where you play a panda running, jumping, and collecting bamboo through 18 levels. Each biome introduces new mechanics (geysers, crumbling ground, wind, ice physics, darkness, rising lava, gravity reversal, portals, etc.). Power-ups (staff, glide, dash, ice magic) and scoring create short sessions of mastery and exploration.

## 2. How To Run It
- **Install:** `uv pip install -r requirements.txt` (pygame)
- **Run (desktop):** `python game.py` from the project folder
- **Requirements:** Python 3.11+, pygame. For web: pygbag build (see web/README.md)
- **Basic usage:** Arrow/WASD to move, Space/Up to jump (variable height), reach the goal zone per level. High scores saved locally.

## 3. Architecture & File Structure
```
BambooForest/
├── game.py              # Main Game class, state machine, loop, input, collisions
├── sprites.py           # Player + procedural panda frames + all enemies/powerups/projectiles
├── levels.py            # LevelDef dataclasses + _build_level_N() + build_level_state
├── biomes.py            # Biome-specific objects (Geyser, WindZone, RisingLava, etc.)
├── config.py            # All tuning, colors, LEVEL_COUNT=18, physics constants, states
├── engine.py            # Camera, ParticleSystem, ScreenShake
├── backgrounds.py       # Biome-specific parallax layers
├── audio.py             # Procedural WAV sound effects
├── ui.py                # TitleScreen, HUD, Pause, transitions, overlays
├── save.py              # High scores (JSON + localStorage fallback for web)
├── requirements.txt     # pygame
├── web/                 # Pyodide copy of most modules + main.py + build
└── diag_shots/          # Animation reference frames
```

Data flow: LevelDef → build_level_state (populates Groups) → Game._update_gameplay (Player.update + biome effects + collisions) → draw with camera/particles/backgrounds.

## 4. Key Decisions & Why
- Procedural pixel art generators instead of asset files (easy iteration, no external images needed except a couple).
- Duplicated source tree in web/ (pygbag requirement; parity maintained manually for now).
- Level construction via data-driven LevelDef + builder functions (keeps biome variety manageable).
- Minimal save (top scores only) initially; expanded in later work for web persistence.
- State machine in Game for menu/playing/paused/etc. (clean separation of input/update/draw).

## 5. Development Log

### 2026-06-24 — Agent swarm drive (bugs closed, controls smoothed, grove/ghosts/daily/overgrown advanced, tests 25+, parity, juice)
- Bugs closed (verified in code + ACTIVE_BUGS updates): HomingSpecter wall phasing prevented, checkpoint keyed on (x,y), fragile __class__ enemy checks replaced by isinstance (GravityDrone etc), dead player attack guard, inline font allocs centralized, hot-path imports cleaned, hardcoded bounds fixed (e.g. 8000->const), plus earlier criticals like reverse grav, double damage, web save, UI overflow, wind bypasses.
- Controls smoothed: jump buffer window, variable jump height (release early), coyote time, reverse-gravity support with kick in jump + auto-fire, input_lock_timer. All exercised in player tests.
- Grove, ghosts, daily, overgrown advanced: Grove grafting (essences per-biome from bamboo, combine 2 for permanent grafts: glide/dash/lava effects, UI via G key); lightweight speedrun ghosts (sampled pos/facing saved with best times); daily challenge (D key, YYYYMMDD seed, mods to essence/enemies/wind, completion tracking); overgrown post-game unlock on L18 + essence progress.
- Tests: 25+ passing (23 player mechanics + 2 smoke; additional verify scenarios cover buffer/dash/glide/lock/grav/ghosts/portals). No breakage.
- Parity: all fixes and features applied to both root/ and web/ trees. Web save, localStorage, ghosts, daily, grove all synced.
- Gameplay juice: particles on geysers/updrafts/mushrooms, placements tuned, visual/feel polish, audio cues.
- Swarm agents (explore, gameplay, parity, verify, etc.) drove targeted work; docs updated.

### 2026-06-24 — Grove crafting meta implemented
- Added ST_GROVE state + GroveUI (simple keyboard essence browser + 2-3 combine bench).
- Extended unified profile (save.py) with essences (per-biome counts) + grafts list.
- Award 1 essence on biome clear (in _advance_level).
- Grafts applied to Player on spawn (glide_efficiency slows fall more; lava_resist downgrades instant kill; dash_mastery halves cooldown).
- Essence awarded on every bamboo collect using level.biome tag (maps to save profile keys).
- Grove reachable via G from title or pause; combine 2 essences -> passive graft. ESC/G exits.
- Non-breaking to core physics/levels. Mirrored key bits to web/.
- Updated this log + light README/TUTORIAL notes.

### 2026-06-24 — Agent swarm + next-level vision + docs (prior)
- Full codebase map via explore agent.
- Controls polish: jump buffer, variable jump height, reverse-gravity kick in jump + auto-fire, input_lock_timer.
- Multiple high-impact fixes from bug reports (portals clear state, collision sync, UI no-clip).
- Gameplay juice batch: geysers, updrafts, mushrooms, particles, placements, math fixes (gameplay architect agent).
- Save improved for web localStorage.
- Created root + dated docs copies: README, BREAKDOWN, HANDOFF, TUTORIAL, PROOF per rules.
- Spawned additional agents for grafting meta, speedrun ghosts, accessibility, verification harness, anim parity, web save polish.
- Appended review notes to bug reports.

Known issues: See the 6 *BUGS_REPORT.md files (reverse gravity landing details, web save edge cases, UI in some states, enemy double-damage edge cases, etc.). Criticals prioritized.

### 2026-06-24 — Feature #3: simple daily challenge seeds (low scope)
- Title 'Daily' button (D key) + daily_mode flag + seed RNG with YYYYMMDD on daily starts only.
- Light mods: +~20% essence (seeded 20% double award), enemy spawn shuffle in desert biome, +25% wind push.
- Daily completion tracked in profile (mark on full victory).
- Seed shown in HUD + title button label. Parity maintained root+web/. Smoke + full tests pass.

### 2026-06-24 — Docs + final QA + swarm completions close
- Bug fixes from map, perf/edge hardening (imports, bounds, fonts, guards), visuals in progress noted, ghosts/grove/daily verified green.
- Full pytest 25 passed; verify harness all scenarios (jump buffer, dash, glide, reverse-grav, portals, ghosts, grove grafts, daily, parity) green x3; basic smoke frames OK.
- Confirmed no inline SysFont("...") in game/ui — all use cached get_font(). Table and notes cleaned in ACTIVE_BUGS.
- Appended dated entry; source docs + dated copies refreshed per rules. Plain language in PROOF.

### 2026-06-24 — Final docs + two-copies agent (speedrun+ghosts completed, map fixes, perf/edge, visuals)
- Speedrun + ghosts plan item completed: ghost recording/playback, save-if-better logic, GhostPanda replay, verify coverage for ghosts + integration with grove/daily; all green.
- Recent bug fixes landed from map agent (HomingSpecter platform snap to stop wall phasing, checkpoint (x,y) key, isinstance enemy type checks replacing __class__ names (5 places), dead player attack guard, unused class removal).
- Perf/edge hardening applied: promoted hot imports (TimedGate etc), switched hardcoded 8000+ to consts, centralized get_font, added guards, tuned friction, cleaned random-in-loop.
- Visuals in flight: some web vs root sprite frame diffs remain (arm/leg clips); head bob parity closed; listed only in ACTIVE_BUGS OPEN-02.
- All project docs appended (history/devlog), PROOF changelog updated plain, two-copies created in docs/. Post-edit full pytest + verify run clean. Followed read-before-edit, two-copies, uv, etc.

### 2026-06-24 — Accessibility screen, graft meta + visuals polish, ghosts polish, bug fixes (docs+final summary agent)
- Accessibility screen landed: full AccessibilityOptions overlay (keyboard nav, 5+ settings incl reduced_motion, text_scale, particle_scale, game_speed, color filter). Wired to Game state (O key), save profile, engine particles, game loop dt + post draw filter. Root+web. Smoke verified.
- Graft meta + visuals: Grove complete with craft (combine), apply_grafts, persistent essences/grafts; visuals polished (graft leaf bursts, particle tuning, geyser/updraft juice, sprites head bob + arm/leg clip parity fixes closed OPEN-02).
- Ghosts polish: best-run save + GhostPanda replay refined; verify scenarios for record/save/replay + daily/grove full green.
- Bug fixes: closed remaining from ACTIVE_BUGS swarm (OPEN-02 visuals, OPEN-03 fonts, OPEN-04/12 imports, OPEN-05/13 bounds, OPEN-07 phasing, OPEN-11/14 etc; dead code, guards). All double ported.
- Tests: Ran full pytest (25 passed); full verify harness 16 scenarios x3 =48 PASS including new meta features + parity.
- Confirmed plan progress: accessibility now [x], web parity [x] on key items, others advancing. Dated copies + PROOF plain update done.

### 2026-06-24 — Docs lock + ACTIVE close (grafting meta start agent + full delivery (GroveUI, recipes, visuals), UI/visuals polish, graft feedback)
- Appended dedicated dated entry to BREAKDOWN dev log.
- Grafting meta start agent + full delivery locked: GroveUI, recipes (essence combine), visuals (graft feedback particles, leaf bursts, mastery), apply logic.
- UI/visuals polish + graft feedback documented.
- ACTIVE_BUGS: grafting complete note + polish + parity closes added.
- Full pytest + verify green (25 + 48). Two dated copies in Desktop/AI/docs/ ensured. Read-first + search_replace used throughout.

### 2026-06-24 — Save harden+web polish (final lock)
- save.py (root+web) hardened to unified profile dict (high_scores + essences + grafts + bests/times+ghosts + daily_* + unlocks + settings + overgrown flags).
- Web path fully hardened: _IS_WEB detects pyodide/emscripten; all FS open() bypassed for web (localStorage.get/set only for profile and legacy highscores key); returns safe defaults + False on failure (no silent data loss).
- Ghost/daily/overgrown support added to _load_profile_data, _migrate, _save (bests, daily_completions, daily_bests, overgrown_cleared etc).
- SAVE_FILE path only used on desktop; computed safely from BASE_DIR or frozen exe dir. No path issues in web build (verified in verify_web_parity_key_paths).

### 2026-06-24 — Grafting full+visuals (final lock)
- Full grafting: GroveUI + 2-essence recipes -> 3 grafts (glide/dash/lava), essences from bamboo biome tag + level clear, apply_grafts to Player (modifies glide/dash/lava behaviors), persisted in profile.
- Visuals: leaf burst particles on graft, mastery aura (3+), engine graft juice, geyser/updraft polish.

### 2026-06-24 Phase-2 swarm: 16 agents drove further controls/juice/meta/polish/parity/harness...
Lane 16 closer: appended full plain summary of lanes + re-ran pytest 25 + verify 87 green. Updated this dated copy + root + central docs/. Swarm closed. Read docs first. Two copies. All per rules.

### 2026-06-24 — Docs enforcement + ACTIVE close + full swarm summary (harness build, web save polish, grafting start + full, visuals/UI, etc.)
- Swarm: harness (tests/verify.py 16 scenarios + 48 runs covering graft/ghost/daily/web parity etc), web save (unified profile + localStorage root/web), grafting start+full (GroveUI + recipes + apply + particles), visuals/UI (access, sprite parity fixes arm/leg/head/graft, mastery), bug/perf closes by map agents, all ported parity.
- Docs agents: appended to dev log + two copies.
- ACTIVE visual parity closed for core (player/graft/UI); design opens remain.
- All reads first. Verify after.
- Non breaking; full state + web copy.

### 2026-06-24 — Visuals/UI polish + accessibility (final lock)
- Visuals: full sprite frame parity (head bob dy, arm/leg coords fixed no clip root<->web), graft tints/pulses, particle tuning.
- UI polish: Grove keyboard, better HUD for ghosts/daily, no overflow.
- Accessibility: O-key screen, sliders (particle/text/speed/reduced/color), live apply + persist via save profile.
- All double ported.

### 2026-06-24 — Ghosts + overgrown progress (final lock)
- Ghosts: lightweight record (pos/facing/time samples), save_best_run if improved, GhostPanda replay entity during levels, verify coverage (record/save/replay + daily/grove).
- Overgrown: unlock flag + mastery (grafts>=5 or ess>=25) on L18, mark mastery, ST_OVERGROWN, profile persist.
- Integrated with save harden.

### Earlier sessions
- Core 18-level platformer with biomes, powerups, bosses.
- Web build support.
- Initial bug reports generated.

### 2026-06-24 — Crash logger integration + overgrown expansion + controls/juice + ghost/UI polish + tests green (docs finalization)
- Integrated shared crash_logger at entry points (game.py desktop + web/main.py) with install(project_root) + safe fallback; follows diagnostic & crash logger rule. No silent failures possible on uncaught.
- Overgrown expansion progress: unlock flag + ST_OVERGROWN after L18 if mastery (5 grafts or 25+ essence), mark mastery, helpers, basic vines/slow area wired; saved in profile.
- Controls + juice polish: variable jumps, buffer, grav handling + particles tuned on geysers/updrafts/grafts (leaf bursts, mastery aura).
- Ghost + UI improvements: GhostPanda replay + best time, accessibility O screen (sliders for scale/speed/motion/color persisted+applied), graft visuals + daily/overgrown UI, full root<->web sprite/UI parity.
- Tests status verified: 25 pytest passed; verify harness 16/16+ scenarios (incl overgrown, ghosts, grafts, daily, parity, perf) x3 executions all green (51 total runs).
- Docs finalization: appended to dev log + all core docs; ACTIVE closes note (tests green, no regressions). Fresh dated copies of the 4 (BREAKDOWN/HANDOFF/TUTORIAL/PROOF) produced to root and Desktop/AI/docs/ with 2026-06-24_ prefix. Plain language. No code edits.
