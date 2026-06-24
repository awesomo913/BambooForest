# Bamboo Forest — Tutorial
**Last updated:** 2026-06-24 (swarm drive)

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
