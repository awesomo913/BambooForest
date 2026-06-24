# Bamboo Forest — Tutorial
**Last updated:** 2026-06-24 (crash_logger integration + overgrown expansion + controls/juice polish + ghost/UI + 25 tests/16/16 verify green; docs finalization)

---

## 1. Quickstart
Get into the first level and collect bamboo in under a minute.

- Install: `uv pip install -r requirements.txt`
- Run: `python game.py` (from the BambooForest folder)
- You should see the title screen. Press ENTER to start.
- Use arrows or A/D to move, Space/Up to jump. Reach the goal on the right.
- What now? Explore the first few levels to learn basic movement and power-up feel.

## 2. Feature Walkthrough

**Movement and Jumping**
- What it does: Walk, run, jump with variable height (release early for shorter jumps), coyote time, and jump buffer.
- How to do it: Left/Right to move. Hold Space then release for short hop, full press for high jump.
- Gotchas: Ice levels change friction; reverse gravity zones flip "up".

**Power-ups**
- Bamboo Staff: Collect for melee + shuriken throws (E/X and Ctrl/Q).
- Glide Feather: Hold jump while falling for slow descent (10s).
- Dash Boots: SHIFT for quick burst (30s).
- Ice magic: Unlocked after first boss; R to cast when mana full.

**Biomes & Mechanics**
Each set of levels introduces rules. Examples:
- Volcanic: Geysers launch you upward.
- Ice/Salt: Slippery + growing hazards.
- Gravity (late): Zones that flip or change your fall speed.
- Use the environment — don't fight every rule.

**Scoring & High Scores**
Collect bamboo for points and combos. High scores saved automatically (desktop file, web browser storage).

**The Grove (meta)**
Every bamboo you collect earns 1 essence for its biome. From title or pause screen press G to enter The Grove. Select 2 essences on the bench (C or ENTER) to craft a permanent passive graft: better glide, faster dash cooldown, or lava resist. Grafts apply to future runs. ESC or G to leave.

## 3. Common Workflows / Recipes

**Reach the end with a specific power-up**
- Goal: Clear a level using glide.
- Steps: 1. Locate the Glide Feather. 2. Hold jump in air to use it. 3. Plan jumps around its timer.
- Result: Cleaner path and higher score.

**Chase a better high score**
- Goal: Beat your previous best.
- Steps: Learn safe routes, use power-ups efficiently, minimize damage.
- Result: New top score saved on victory or game over.

**Play on web**
- Build or use the hosted version (see web/README.md).
- Controls are the same; touch overlay available.

## 6. Changelog (user-facing)

### 2026-06-24 — Swarm drive polish and meta features
- Grove: collect essence from bamboo by biome, enter via G on title or pause, combine two for permanent grafts (better glide, faster dash recovery, lava resistance).
- Daily challenges: press D on title for seeded run (date-based), special mods, tracked completions.
- Ghosts: best speedrun times now save lightweight ghost data for replay feel.
- Overgrown: post-game area unlocks after clearing level 18 with progress.
- Controls feel better: jump buffering, easier short/long hops, reverse gravity support.
- Many bugs closed (enemy phasing, collisions, attacks while dead, etc.) for smoother sessions. Desktop and web versions kept in parity. Gameplay juice (particles, effects) added. 25+ tests now cover core movement and timers.

### 2026-06-24 — Final QA + swarm agent completions close
- Bug fixes from map, perf/edge hardening, visuals (in progress), ghosts/grove verified green.
- Tests: full pytest 25 pass; verify harness (ghosts/grove/daily/etc on full maps) all green; smoke OK.
- No inline SysFont in game/ui (uses get_font). ACTIVE_BUGS + docs updated + copied.

### 2026-06-24 — Final docs pass
- Speedrun+ghosts marked complete in project plan (record best runs, replay ghosts visible during play, verified).
- Bug fixes, perf/edge work, visuals in flight documented; no new user-facing behavior beyond prior.
- Updated changelog + docs copies.

### 2026-06-24 — Accessibility screen + polish completions (docs + summary)
- New accessibility options screen: press O on title or pause. Tweak particle amount, text size, game speed, reduced motion (less sparkles), color filter. Settings save with your profile and apply immediately.
- Grove (grafts) + visuals polished: better particle bursts on grafts, refined geysers and placements; ghost replays feel smoother.
- Bug fixes for feel: no more phasing through walls, safer enemy types, no attacking when dead, checkpoint fixes, faster code paths.
- All tests: pytest 25 pass, verify harness (ghosts, grafts, daily, reverse grav, web parity) 48 runs green. Desktop and web stay matched.
- Docs + dated copies produced; plan items updated for progress.

### 2026-06-24 — Docs enforcement + ACTIVE close + full swarm (harness, web save, grafting, visuals/UI)
- Swarm: harness build + verify 16 scenarios (graft/ghost/daily/parity etc) x3 green; web save polish (unified + localStorage); grafting start+full (GroveUI + recipes + essences + apply + visuals); UI/visuals (accessibility, sprite parity arm/leg/head/graft mastery, particles); bug closes + parity.
- Visual parity notes closed in ACTIVE for core player/graft/UI.
- Appends + copies done. Read first.

### 2026-06-24 — Save harden + web polish, grafting full, visuals/UI, accessibility, ghosts, overgrown (final docs lock)
- Your saves (scores, grove essences/grafts, best ghost runs, daily clears, overgrown unlocks) are now hardened. Desktop uses one file. Web uses browser storage safely (no file writes that can break in browser).
- Full grafting landed with nice visuals (leaf effects when you craft or use powers).
- Visuals and UI cleaned up so the panda looks the same everywhere; Grove and other screens feel good.
- Accessibility options (O key) let you change motion, speed, colors — saved automatically.
- Ghosts: see your past best runs replay as a ghost panda.
- Overgrown: extra challenge area opens after finishing level 18 if you have enough powers collected. Progress carries over. All in profile save.

### 2026-06-24 — Crash logger + final polish + tests (docs finalization)
- Crash logger now integrated at game entry points (required workspace rule for diagnostics/crashes).
- Overgrown area expanded with unlock logic, mastery, and special slow vines in post-game.
- Controls feel juicier with better jump timing, ghost replays show past runs, UI has O for accessibility tweaks (saved), graft leaf effects, daily/overgrown buttons.
- All verified green: 25 pytest + 16 scenarios in verify harness (x3) including overgrown, ghosts, grafts, web parity.
- Docs finalized with appends + fresh dated copies of the four main docs to root and central AI/docs folder. Plain language. No code changes this pass.

2026-06-24 Phase-2 swarm: 16 agents drove further controls/juice/meta/polish/parity/harness. Lane 16 appended final to this dated TUTORIAL. 25 pytest + 87 verify green post agents. Dated copies synced to project/docs/. Read before write. Swarm closed.
