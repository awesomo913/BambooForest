---
public-visible: false
---

# Bamboo Forest — Handoff
**Last updated:** 2026-06-24
**Current owner:** User (primary designer) + Grok/agents (implementation)
**Status:** in-progress

---

## 1. Goals
- Deliver satisfying short sessions of movement, timing, and exploration in a changing forest.
- Make each of the 18 biomes feel distinct through unique mechanics and visual identity.
- Provide clear progression with power-ups, scoring, and high-score chasing.
- Support both desktop and web play with reasonable parity.

## 2. Outline (architecture at 30k ft)
- Core loop in game.py (state machine + update/draw).
- Level data in levels.py (LevelDef builders) wired to groups.
- Mechanics and entities in sprites.py + biomes.py.
- Procedural visuals (sprites), backgrounds, audio.
- UI overlays in ui.py.
- Minimal persistence in save.py (now with web localStorage).
- Web build is a near-dupe tree under web/.

## 3. Context
The user wanted a fun, varied panda platformer with biome variety and growth feel. Prior simple demos (bamboo_forest.py etc.) were replaced by the full stateful Game with power-ups and 18 levels. Procedural everything keeps it lightweight and easy to tweak. Web support added for easy sharing/play.

## 4. History (dated, append-only)

### 2026-06-24 — Agent swarm drive (bugs closed, controls smoothed, grove/ghosts/daily/overgrown advanced, tests 25+, parity, juice)
- Bugs closed: HomingSpecter no longer phases walls (platform snap added root+web), checkpoint uses (x,y) key, enemy type checks hardened to isinstance, dead-player attacks guarded, font allocs and hot imports cleaned, bounds made non-hardcoded.
- Controls smoothed across board: jump buffer, variable height jumps, reverse gravity handling with auto kick, input lock. Backed by player tests.
- Grove/ghosts/daily/overgrown advanced: full grove grafting meta (biome essences + 2-essence combine for grafts), speedrun ghost recording/playback in save + verify, daily seeded runs with tracking, overgrown unlock flag post L18.
- 25+ tests passing (player unit + smoke harness); verify covers mechanics.
- Parity enforced: every swarm change ported to web/ copy (save, ui, biomes, sprites, game).
- Juice added: particles, tuned geysers, placements, feel improvements.
- ACTIVE_BUGS updated; docs appended for the drive. Swarm covered explore, controls, gameplay, parity, verify agents.

### 2026-06-24 — Agent swarm drive + next-level vision + docs
- User requested driving ~16 specialized agents to fix bugs, smooth controls, improve gameplay, take to next level.
- Explore agent produced full map.
- Multiple agents delivered: controls (buffer, variable jump, reverse kick, lock timer), gameplay juice (geysers, particles, placements), parity/sync work.
- Plan agent produced 8 next-level features + full docs plan.
- Created README, BREAKDOWN, HANDOFF, TUTORIAL, PROOF (project + dated docs copies).
- Appended notes to bug reports.
- Fixes integrated for high items from reports (portals, collision, UI clipping, save web support).

### Earlier
- Core engine, 18 levels, biomes, power-ups implemented.
- Web build added.
- Bug reports generated.

## 5. Credit & Authorship
**The user designed this product.** The user defined goals, feature priorities, UI decisions, biome concepts, and acceptance criteria. Grok and sub-agents (various sessions) implemented the code to those specifications. The user reviewed and directed. This is the user's game; AI was the implementation tool.

## 6. Plan (what's next)
- [ ] Address remaining criticals from bug reports (reverse grav details, web save edges, etc.)
- [x] Implement grafting/crafting meta (Grove hub) — G from title/pause, essence awarded directly on bamboo collect (per level.biome tag), combine any 2 into one of 3 passive grafts, stored in unified profile. Grafts affect glide/dash/lava. Full state wiring + mirror to web/. Tiny, no breakage to physics/levels. Docs lightly updated.
- [ ] Add speedrun mode + ghosts + replays
- [ ] Accessibility options screen
- [ ] Endgame Overgrowth levels + mastery
- [ ] Expanded profile persistence
- [ ] Web parity final pass + verification harness
- [ ] Next-level features per plan agent output
- [ ] Screenshots + full tutorial update

## 7. Handoff checklist for the next AI
- [ ] Read Goals — what is this product FOR
- [ ] Read Context — why was this built this way
- [ ] Read History — what has already been done
- [ ] Read current *BUGS_REPORT.md files (critical first)
- [ ] Check root vs web/ duplication status
- [ ] Run `python game.py` and basic smoke for changed paths
- [ ] Follow uv + crash logger rules + two-doc-copies rule
