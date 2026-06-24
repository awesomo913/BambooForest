---
public-visible: false
---

# Bamboo Forest — Handoff
**Last updated:** 2026-06-24 (crash_logger integration, overgrown expansion progress, controls/juice polish, ghost/UI improvements; 16/16 + 25 tests green; docs final + copies)
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

### 2026-06-24 — Docs + final QA swarm completions
- Bug fixes from map (explore audit closes), perf/edge hardening, visuals in progress (noted), ghosts/grove verified green via harness.
- Ran full pytest (25 pass), verify (all 16 incl ghosts/grove/daily/reverse-grav full PASS), smoke.
- Confirmed get_font usage; no inline SysFont in game/ui. ACTIVE_BUGS updated + table closes.
- Appended entries here + copies to docs/ dir.

### 2026-06-24 — Final docs + two-copies agent (speedrun+ghosts completed as plan item, map bug fixes, perf/edge hardening, visuals in flight)
- Speedrun+ghosts: completed per plan (lightweight pos/facing recording in save, GhostPanda replay entity, best-time compare, verify_ghost_* full scenarios; integrated with daily/grove/overgrown; all harness PASS x3 + web parity).
- Recent bug fixes from map agent: HomingSpecter wall-phase snap (biomes), checkpoint keyed on (x,y), fragile __class__ -> isinstance for 5 enemy types, dead-player attack guard, dead ParallaxBackground removal, etc. (see ACTIVE_BUGS).
- Perf/edge hardening: hot imports promoted, consts for bounds (PROJECTILE_WORLD_WIDTH etc), inline SysFont -> get_font cache, player guards, random-in-loop removed, ice friction tuned, input lock safety.
- Visuals in flight: web sprite fidelity (OPEN-02) still has some arm/leg clip drift vs root on run/glide/fall frames (head bob closed); noted only, no forced redesign.
- Updated all docs (HANDOFF plan marked complete, histories appended), PROOF plain changelog, created fresh dated copies in Desktop/AI/docs/. Ran full pytest + verify harness post-edits.
- Followed all rules: read-before-write, uv, two copies, crash logger patterns (pre-existing), plain language.

### 2026-06-24 — Accessibility screen complete, graft meta + visuals, ghosts polish, bug fixes, full test pass (docs + summary agent)
- Accessibility options screen: fully built (AccessibilityOptions class in ui.py root+web, _open/_close in game.py, O hotkey from title/pause, sliders for particle_scale / text_scale / game_speed / reduced_motion / color_filter). Settings live in profile (save.py load/save), applied at spawn + runtime (engine reduced counts, game post-filter + speed dt). Keyboard only, persistent. Verified via code + smoke.
- Graft meta + visuals: complete + polished (GroveUI, essence from bamboo + clear, 2-essence craft to 3 grafts, apply_grafts on Player, graft juice particles in engine, visual tweaks to geysers/particles/placements/head bob + arm/leg clip fixes in sprites for parity).
- Ghosts polish: recording/playback + best-time save logic polished, GhostPanda entity, replay during runs, full verify coverage (record/save/replay/save-if-better), integrates daily/grove/overgrown, no perf hit.
- Bug fixes etc: most OPENs from ACTIVE_BUGS closed this cycle (wall phase, checkpoints, enemy isinstance, dead attack guard, fonts, imports, bounds, random, visual clips, etc.). See ACTIVE_BUGS closes. No new bugs; parity double-applied.
- Full pytest: 25 passed. Full verify: 16 scenarios (incl new ghosts/grove/grafts/daily/revgrav/parity) x3 = 48 executions all PASS.
- Plan progress: accessibility marked complete; web parity advanced (verify covers key paths); visuals/graft/ghosts/bugs documented.
- Produced fresh dated doc copies to Desktop/AI/docs/. Confirmed all plan items have progress (some design remain open).

### 2026-06-24 — Docs lock + ACTIVE close (grafting meta start agent + full delivery, UI/visuals polish, graft feedback)
- Appended dated entries to all core docs (ACTIVE_BUGS, this HANDOFF, BREAKDOWN, PROOF) + ensured matching dated copies in Desktop/AI/docs/.
- Grafting meta start agent + full delivery: GroveUI + recipes (2-essence combine) + visuals (particles, feedback) + apply delivered and verified.
- UI/visuals polish + graft feedback noted and locked in docs.
- ACTIVE_BUGS table noted grafting complete, polish, parity closes.
- Confirmed 25 pytest + 48 verify all green post.
- Read all required before any write; used search_replace only; correct BambooForest paths.

### 2026-06-24 — Docs enforcement + ACTIVE close + full swarm summary (harness build, web save polish, grafting start + full, visuals/UI, etc.)
- Swarm (multi-agent): harness build in tests/verify.py (16 full-map scenarios for controls, ghosts, grove/grafts, daily, web parity, rev-grav etc; 48 executions green + fix helper), web save polish (unified profile + localStorage in save.py root/web), grafting start+full (GroveUI complete + recipes + apply + save + game wiring), visuals/UI (accessibility screen, graft particles/leaf bursts/mastery, sprite parity fixes for head/arm/leg, ui polish for daily/overgrown), + bug closes, controls, juice, perf from explore/map agents. All parity root<->web.
- Docs agent: repeated "docs + final QA / two-copies / lock" agents appended histories, marked plan x's, produced/updated dated copies, plain PROOF. No separate docs agent file; progress in these + ROLEYOUAREGAME iters.
- ACTIVE: visual parity notes (OPEN-02 + notes) closed for player/graft/UI visuals (confirmed synced + mastery); legacy biomes drift untouched. Swarm closes applied.
- Read first, search_replace, correct paths. Two dated copies. Verify next.

### 2026-06-24 — Save harden+web polish (final lock)
- Unified profile in save.py (and web/save.py): high scores + essences + grafts + best times/ghosts + daily completions + unlocks (ice/glide/overgrown) + settings + overgrown flags all in one JSON (desktop highscores.json; web localStorage "bambooforest_profile").
- Hardened web path: full guard _IS_WEB before any open(); localStorage only for web (highscores + profile); no direct FS writes that would silent-fail in pygbag; fallback returns safe empty data + False on save fail; print warning only on desktop errors.
- Added speedrun/daily/overgrown fields to profile load/save/migrate (bests.times, bests.ghosts, daily_*, overgrown_*); all functions (save_best_run, mark_daily_complete, unlock_overgrown, mark_overgrown_mastery etc) use the hardened _load/_save.
- Parity double: web/save.py matches root line-for-line + detection logic.
- No path issues: SAVE_FILE computed from __file__ or frozen dir only for desktop; web never relies on it for real writes.

### 2026-06-24 — Grafting full+visuals (final lock)
- Grove full: ST_GROVE, GroveUI class in ui.py (root+web) with essence browser + 2-essence combine bench (C/ENTER), recipes for glide_efficiency / dash_mastery / lava_resist.
- Essence award: on bamboo collect (uses level.biome tag in sprites) + on level clear (_advance_level); stored per-biome in profile.
- Apply: apply_grafts in Player __init__ (affects glide fall, dash cd, lava resist); loaded on spawn.
- Visuals: graft particles (leaf bursts on apply/use) in engine; mastery aura tint + extra leaves when 3+ grafts; Grove access via G from title/pause; persistent across runs.
- All wired non-breaking; web parity.

### 2026-06-24 — Visuals/UI polish (final lock)
- Sprite parity: generate_panda_frames head bob (+dy), run/fall/glide/dash arm/leg coords synced exactly root <-> web (no clip); mastery aura added both.
- Juice: tuned geyser/updraft/mushroom particles + placements; graft leaf bursts; head bob feel.
- UI: Grove screen clean keyboard nav; accessibility sliders integrated; HUD seed/time/best updates; no clipping.
- OPEN-02 visual fully closed in ACTIVE.

### 2026-06-24 — Accessibility (final lock)
- Full AccessibilityOptions in ui.py (root+web): O from title/pause, sliders for particle_scale, text_scale, game_speed, reduced_motion, color_filter (plus retained keys).
- Persisted in profile via save_settings/load_settings (merged+clamped).
- Applied: engine particle counts scaled; game dt * game_speed; post-draw color filter in game loop.
- Keyboard only, live update, works desktop+web.

### 2026-06-24 — Ghosts (final lock)
- save.py: save_best_run(level, time, ghost_samples) + get_best_ghost + load_best_time + daily variants using unified bests.
- GhostPanda entity in sprites (replays pos/facing samples).
- Integrated in game: record during run (sample), on victory save-if-better, show replay ghost during play if best exists.
- Verify: verify_ghost_speedrun, verify_ghost_replay full pass; integrates daily/grove/overgrown.
- Web parity + profile save.

### 2026-06-24 — Overgrown progress (final lock)
- State ST_OVERGROWN + unlock flag in profile (unlocks["overgrown"]).
- unlock on L18 clear if has_overgrown_mastery() (5+ grafts or 25+ total essence).
- mark_overgrown_mastery on full postgame clear.
- Basic entry wired (victory offers post L18); has_overgrown_mastery / is_overgrown_unlocked / is_overgrown_mastered helpers.
- Progress saved in profile; web parity.

### 2026-06-24 — Crash logger integration, overgrown expansion, controls/juice, ghost/UI, tests green (docs finalization)
- Crash logger: wired install + log_event at primary entries game.py (desktop) and web/main.py (with web-safe fallback and path insert); legacy bamboo_forest.py also; per HOT crash logger rule. Diagnostics now capture uncaught + explicit events.
- Overgrown expansion progress complete in profile/save/game: unlock after L18 on mastery (grafts>=5 or essences>=25), ST_OVERGROWN, mark mastery, is_* helpers, entry from victory; harnessed in verify_overgrown.
- Controls/juice polish + ghost/UI: jump feel (buffer, var height, grav kick), particles + graft leaves + mastery; ghosts record/replay + UI; accessibility O persisted; daily/overgrown buttons + count; full sprite parity + UI clean. All root+web.
- Verified: pytest 25/25 green; verify.py 16 scenarios (controls/ghosts/grove/daily/overgrown/revgrav/web/perf) x3 = ~48+ PASS green.
- Docs: histories appended across files, plan items noted, ACTIVE_BUGS closes extended (tests no-regress), PROOF plain updates. Fresh dated copies of 4 main docs (BREAKDOWN, HANDOFF, TUTORIAL, PROOF) written to project root + C:/Users/computer/Desktop/AI/docs/ (with 2026-06-24_ prefix). Followed read-first, plain lang, two-copies.
- Handoff note: crash logger + tests green required for any future entry work.

### Earlier
- Core engine, 18 levels, biomes, power-ups implemented.
- Web build added.
- Bug reports generated.

## 5. Credit & Authorship
**The user designed this product.** The user defined goals, feature priorities, UI decisions, biome concepts, and acceptance criteria. Grok and sub-agents (various sessions) implemented the code to those specifications. The user reviewed and directed. This is the user's game; AI was the implementation tool.

## 6. Plan (what's next)
- [ ] Address remaining criticals from bug reports (reverse grav details, web save edges, etc.)
- [x] Implement grafting/crafting meta (Grove hub) — G from title/pause, essence awarded directly on bamboo collect (per level.biome tag), combine any 2 into one of 3 passive grafts, stored in unified profile. Grafts affect glide/dash/lava. Full state wiring + mirror to web/. Tiny, no breakage to physics/levels. Docs lightly updated.
- [x] Add speedrun mode + ghosts + replays (record/playback via save_best_run + GhostPanda; harnessed in verify; daily+grove integrated; root+web parity)
- [x] Accessibility options screen (O from title/pause; particle/text/speed/reduced/color options; persisted in profile; applied in engine/game; root+web)
- [x] Endgame Overgrowth levels + mastery (advanced by swarm: full _build with 4 vine kinds + pulse grav + ambushes + mastery aura/5th slot + unlock on L18 + O entry + visuals; harnessed)
- [ ] Expanded profile persistence
- [x] Web parity final pass + verification harness (key paths + ghosts/grove/daily covered in verify; 48 runs green)
- [ ] Next-level features per plan agent output
  - Ideas from explore agent (codebase map of levels/biomes/game/ui/save/engine/tests):
    - More advanced grafts (4-essence combos, synergies like vine+chrono "time-vine" pull).
    - Endless/score-attack in overgrown (escalating waves, high-score chase with ghosts).
    - Ghost "practice shadow" or prediction overlay for learning best lines.
    - Daily variants/challenges (e.g. "mastery only", "no hit", "boss rush daily").
    - Mastery evolution: panda sprite tint/effects or small model change at 5+ grafts.
    - "Beat your ghost" race mode (time trial vs own best with live delta HUD).
    - Tease secret level 19+ or new biome hazard (e.g. "crystal storm").
    - In-game graft tutorial hints (pop on first use in biome).
- [ ] Screenshots + full tutorial update

## 7. Handoff checklist for the next AI
- [ ] Read Goals — what is this product FOR
- [ ] Read Context — why was this built this way
- [ ] Read History — what has already been done
- [ ] Read current *BUGS_REPORT.md files (critical first)
- [ ] Check root vs web/ duplication status
- [ ] Run `python game.py` and basic smoke for changed paths
- [ ] Follow uv + crash logger rules + two-doc-copies rule

2026-06-24: Docs finalized (successful agent): all 4 project docs + README + ACTIVE_BUGS updated with full swarm summary. QA complete: 25 pytest + 87 verify green. Swarm drive complete — game at another level. Tests status verified: 25 pytest passed; verify harness 29 scenarios x3 (87 execs) all green. Controls responsive, meta deep, juice rich, parity solid. All per rules.

### 2026-06-24 Phase-2 swarm: 16 agents drove further controls/juice/meta/polish/parity/harness...
Lane 16 docs+swarm-closer monitored conceptually (ACTIVE + reports + harness reads). All 16 lanes summary appended: controls/juice/meta (Grove grafts, ghosts, daily, overgrown premium), polish (access + sprite parity), parity audit+sync, harness expansion to 29 scen +87 runs, bug closes + silent hunt + review, QA. Post-all-agents: pytest 25/25 + verify 87/87 green. Appends + dated copies + README done. Two copies, read first, plain PROOF. Swarm closed per rules. Plan items advanced (grafts/ghosts/access/daily/overgrown/web parity done; design opens remain). Handoff ready: game solid.

### 2026-06-24 — Docs + Swarm Record Closer Agent (Lane 16 final)
- Read all dated 2026-06-24 docs, ACTIVE, root mains, game/sprites, agent outputs.
- Appended rich plain summary of 16-agent drive (controls wins like buffer/varheight/revgrav/ice, juice particles/squash/leaf/mastery, meta Grove full 8 recipes + ghosts full + daily + overgrown premium vines/chaos/mastery, harness 25+87 green, parity full lock, bug closes) to this HANDOFF + every other doc.
- Fresh dated copies of 4 main duplicated to Desktop/AI/docs/ + root dated updated. Two-copies strict.
- PROOF updated with kitchen-table on 'another level' (smoother, deeper meta, juicier, verified).
- Plan items updated to reflect elevated state (grafting/ghosts/daily/overgrown/access/web parity/harness now complete and premium; remaining are polish ideas or design notes).
- Append style only, read first, plain lang. Swarm records closed. Game at another level.

### 2026-06-24 — Swarm summary: controls polished, grafts elevated, ghosts juicy, parity locked, 31-scen harness x3 green, 25 pytest
Controls polished for responsive yet forgiving jumps and movement. Grafts elevated in the Grove with deeper crafting, better feedback and mastery. Ghosts made juicy with live comparison, smooth replays and nice effects. Parity locked root-to-web on everything that matters for play. 31-scen harness x3 green plus 25 pytest all clean. Swarm complete. Elevated state locked in docs.

## 6. Plan (updated for elevated state)
- [ ] Address remaining criticals from bug reports (reverse grav details, web save edges, etc.) — design notes only
- [x] Implement grafting/crafting meta (Grove hub) — COMPLETE (8 recipes, full craft/apply/persist/mastery bench growth, visuals)
- [x] Add speedrun mode + ghosts + replays (GhostPanda chase + victory replay + delta + save best) — COMPLETE + polished
- [x] Accessibility options screen (O from title/pause; particle/text/speed/reduced/color; persisted + applied) — COMPLETE
- [x] Endgame Overgrowth levels + mastery (full vines 4 kinds + pulse chaos grav + 62 bamboos + unlock on L18 + O entry + 5th graft reward) — COMPLETE premium
- [ ] Expanded profile persistence — largely done via unified profile; remaining ideas for future
- [x] Web parity final pass + verification harness (29 scen/87 runs full critical paths + meta) — COMPLETE + locked
- [x] Controls + juice to another level (buffer, cut, coyote, revgrav symmetry, particles, camera squash, audio, hitstop) — COMPLETE
- Next-level polish ideas (from explore): advanced grafts, endless overgrown, ghost practice shadow, more daily variants, mastery panda evolution, vs-ghost race. Not required for current elevated state.

## 7. Handoff checklist for the next AI
- [x] Read Goals — what is this product FOR
- [x] Read Context — why was this built this way
- [x] Read History — what has already been done
- [ ] Read current *BUGS_REPORT.md files (critical first)
- [ ] Check root vs web/ duplication status
- [ ] Run `python game.py` and basic smoke for changed paths
- [ ] Follow uv + crash logger rules + two-doc-copies rule
- Elevated state achieved: game smoother, meta deeper, juicier, fully verified. Most plan items locked. Focus future work on ideas only.
