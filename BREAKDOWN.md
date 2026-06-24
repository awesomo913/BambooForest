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

### Earlier sessions
- Core 18-level platformer with biomes, powerups, bosses.
- Web build support.
- Initial bug reports generated.
