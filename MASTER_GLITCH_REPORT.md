# BambooForest — Master Glitch Hunt Report

**Date:** June 5, 2026
**Method:** 2 Hermes agents (deep code read) + 3 Claude agents (static analysis)
**Source files examined:** All 25 .py files (~12,000+ lines)
**Total bugs found: ~77+** (8 CRITICAL · 27 MAJOR · 20 MINOR · 22+ TINY/LOW)

---

## EXECUTIVE SUMMARY — Top 10 Bugs to Fix First

| Rank | Bug | Severity | Area | Fix Effort | Gameplay Impact |
|------|-----|----------|------|------------|-----------------|
| 1 | **Reverse Gravity Landing (L18)** breaks Y-collision — player can't stand on ceilings | CRITICAL | Physics | ~15 lines | Level 18's signature mechanic is unplayable |
| 2 | **ForgeHammer (L15)** deals triple damage (60 HP/hit = half your HP) | CRITICAL | Physics | ~3 lines | Instant death in 2 hits |
| 3 | **VoidEater (L17)** deals double damage (40 HP/hit) | CRITICAL | Physics | ~3 lines | Players die in 3 hits instead of 6 |
| 4 | **Pause Encyclopedia Cards** overflow screen — first column unclickable | CRITICAL | Visual/UI | ~1 line | Can't access enemy info |
| 5 | **Title Screen Gallery** overflows vertically — half the characters invisible | CRITICAL | Visual/UI | ~5 lines | Can't select 12/24 characters |
| 6 | **Rising Lava (L15)** bypasses invincibility frames + re-triggers death sound | CRITICAL | Biome | ~3 lines | Inconsistent with rest of game |
| 7 | **High Scores Never Save in Browser** (WASM filesystem is in-memory only) | CRITICAL | Web | ~30 lines | Web players lose scores on refresh |
| 8 | **Wind Zones (L6)** push rect directly, bypassing wall collision | CRITICAL | Physics | ~3 lines | Can be pushed through walls |
| 9 | **PhaseWraith (L17)** teleport feature is completely dead code | CRITICAL | Biome | ~20 lines | Missing intended mechanic |
| 10 | **AshBat (L4)** can be kited off-screen (snapshot targeting) | CRITICAL | Biome | ~5 lines | Enemy becomes harmless |

---

## BUGS BY CATEGORY

### ⚫ Physics & Collision (Hermes 1) — 19 bugs
Reports: `PHYSICS_BUGS_REPORT.md`

**3 CRITICAL:**
- C1: Reverse gravity (L18) Y-collision broken — player bounces off ceilings instead of landing
- C2: VoidEater (L17) double-damage via both custom check and standard collision loop
- C3: ForgeHammer (L15) triple-damage: 40 (custom) + 20 (standard loop) = 60 HP

**6 MAJOR:**
- M1: RisingLava wave ±2px oscillation creates inconsistent kill zone
- M2: Wind zones bypass ice physics system (direct rect.x modification)
- M3: Teleport chain can fire multiple portals same frame
- M4: MushroomSpring side-collision triggers bounce (AABB + centery check)
- M5: Moving platforms lose riders on vertical ascent
- M6: HomingSpecter phases through walls (no collision detection)

**7 MINOR · 3 TINY**

### ⚫ Biome & Level Design (Hermes 2) — ~25 bugs
Reports: `BIOME_LEVEL_DESIGN_BUGS_REPORT.md`

**6 CRITICAL:**
- C1: Reverse gravity (same as Physics C1)
- C2: Wind pushes rect directly (same as Physics M2)
- C3: AshBat off-screen kiting (snapshot targeting)
- C4: GravityDrone fragile `__class__.__name__` string check
- C5: PhaseWraith teleport dead code
- C6: Rising lava bypasses i-frames

**6 MAJOR:**
- M1: Updraft uses `max()` instead of `min()` — barely works
- M2: Geyser collision rect switches between dormant/erupting
- M3: Crumbling platform detection tolerance too wide
- M4: BrineShard grows during natural ice drift
- M5: Mushroom+crumbling may create dead end (L14)
- M6: Lava first pause below all platforms

**Other:** L13 dark arena + boss = compounding softlock risk; Level 9 is near-identical reskin of Level 7

### ⚫ Rendering & Visual (Claude 1) — 20 bugs
Reports: `VISUAL_BUGS_REPORT.md`

**2 CRITICAL:**
- C1: Encyclopedia cards (5 cols × 180px = 900 > 800 screen) — first column off-screen
- C2: Title gallery (6 rows × 95px = 610 > 540 screen) — bottom 12 characters invisible

**5 MAJOR:**
- M1: Rotated sprite (attack lean, victory dance, trench fall) desyncs rect from image
- M2: Rain streaks in TidalBackground render fully opaque (no SRCALPHA)
- M3: Soul orbs in VoidBackground same issue
- M4: All 3 power-up timers active simultaneously overflow screen right edge
- M5: Cave darkness overlay allocates dead surface every frame (memory waste)

**8 MINOR · 5 TINY**

### ⚫ Web Build Parity (Claude 2) — 14 bugs
Reports: `WEB_PARITY_BUGS_REPORT.md`

**1 CRITICAL (gameplay-breaking):**
- C1: High scores never persist — Pyodide filesystem is in-memory, resets on refresh

**2 HIGH (CI/deploy):**
- H1: CI uses bare `pip` instead of workspace-required `uv pip`
- H2: `favicon.png` copy step can silently break CI

**8 MEDIUM (content divergence):**
- Pickup names forest-themed (web) vs action-named (root)
- Glide/dash pickup positions stripped from root levels — desktop almost never gets glide
- Glide/dash animation states missing from root sprites
- Power-up item art completely diverged (bamboo leaf vs feather)
- Darkness mechanic older in web
- DustDevil sprite 44×72 (web) vs 64×110 (root)
- DarkWall static (web) vs 4-frame animated (root)
- GitHub deploy pipeline issues

### ⚫ Edge Cases & State Machine (Claude 3) — 14+ bugs
Reports: `EDGE_CASE_BUGS_REPORT.md`

**8 MAJOR:**
- M1: `save_high_score()` false positive — value-based `in` check instead of identity or rank
- M2: `AudioManager.play()` mutates shared Sound volume mid-play (click/pop)
- M3: Rising lava re-triggers death sound every frame on dead player
- M4: `_has_glide_permanent` is dead code — never set to True
- M5: Tutorial timers decremented but never used to control hint display
- M6: `ScreenShake.update()` called twice per frame (double RNG)
- M7: No `ACTIVEEVENT` handler — game doesn't auto-pause on alt-tab
- M8: Combo multiplier off-by-one — first bamboo gives 2× instead of 1×

**6+ MINOR:** font allocation every frame, dead player can attack, title screen Enter during transition, etc.

---

## FILES CREATED

| File | Size | Description |
|------|------|-------------|
| `PHYSICS_BUGS_REPORT.md` | 19 KB | Full physics & collision audit |
| `BIOME_LEVEL_DESIGN_BUGS_REPORT.md` | 23 KB | Biome, level & boss audit |
| `VISUAL_BUGS_REPORT.md` | 16.5 KB | Rendering & UI audit |
| `WEB_PARITY_BUGS_REPORT.md` | 10.4 KB | Web build & WASM audit |
| `EDGE_CASE_BUGS_REPORT.md` | 16 KB | State machine & edge cases |
| **`MASTER_GLITCH_REPORT.md`** | **this file** | Combined summary |

---

## QUICK FIX ESTIMATES

**Top 10 bugs can be fixed in ~70 lines of targeted changes across 5 files:**
- `sprites.py`: reverse gravity fix (~15 lines)
- `game.py`: double-damage skip for VoidEater/ForgeHammer (~8 lines), lava i-frame check (~3 lines), wind velocity impulse (~3 lines)
- `ui.py`: column/layout overflow fixes (~6 lines)
- `save.py` / `web/save.py`: WASM localStorage bridge (~30 lines)
- `biomes.py`: AshBat target clamping (~5 lines)

Want me to start fixing? I can hit all 10 in one pass.
