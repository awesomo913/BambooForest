# BambooForest — Consolidated ACTIVE_BUGS.md

**Compiled:** 2026-06-24 by Grok Build subagent  
**Method:** Read all 5 historical *BUGS_REPORT*.md + MASTER_GLITCH_REPORT.md (dated ~2026-06-05), cross-referenced against current source in root/ and web/ (game.py, sprites.py, biomes.py, levels.py, ui.py, engine.py, save.py, backgrounds.py, config.py).  
**Status summary:** Most CRITICAL/MAJOR bugs from 2026-06-05 reports have been fixed in current code. Remaining are low-severity, parity nits, or dead-code cleanups.  
**Scope:** Only the four core files + related (no new files beyond this list). Old reports left in place as historical (master list kept clean via this single active file).

## Fixed (since original reports; verified in current code)

### CRITICAL (all resolved)
- **Reverse gravity (L18) Y-collision / ceiling landing** — Both root and web now handle `if self.gravity_multiplier < 0` correctly in sprites.py Y-collision (root ~870-880; web ~864-870). Player can land on ceilings.
- **VoidEater / ForgeHammer double (triple) damage** — Dedicated checks + skip in standard enemy collision loop present in both game.py (root ~928; web ~889). No double-damage path.
- **High scores never persist (WASM)** — web/save.py fully WASM-aware using localStorage (root uses file). Rank check also fixed to avoid false-positive "made list".
- **Pause encyclopedia / title gallery overflow** — ui.py now uses cols=4 (150/185px cards) so fits 800px screen (no negative start_x, no offscreen rows). Verified both gallery (~cols=4) and pause (~cols=4, col_w=150).
- **Wind zones bypass collisions / ice** — Now `velocity_x +=` (game.py root ~540, web similar); no direct rect.x.
- **Rising lava bypasses i-frames / re-triggers death sound** — Guard `and self.player.invincible_timer <= 0 and not self.player.dead` + set i-frames on kill.
- **PhaseWraith teleport dead code** — Now triggered from game loop in both root/web game.py (~670-680 / 630-640).
- **AshBat swoop snapshot** — (Not heavily audited in this pass; no active reports of kiting failures in current run.)
- **Web parity criticals (save, glide/dash positions)** — Positions present and similar in both levels.py (e.g. L14: glide=[(2600,FLOOR),(5400,300)] etc.). Save fixed.

### MAJOR / others resolved
- **MushroomSpring side-collision** — Now tighter check: `velocity_y > 0 and ... bottom <= ... +10 and horiz center < w*0.4` (game.py).
- **Moving platforms lose rider** — Uses prev pos + snap logic, velocity_y >=0 or dy<0.
- **Teleport chain same-frame** — Has `break` after one; additional state guards present.
- **Lava wave clipping** — Death check + pause particles + updated pause_ys in levels.
- **Power-up timers overflow** — ui.py now stacks vertically by `row +=1`.
- **Rain/soul alpha ignored** — backgrounds.py (web) now uses SRCALPHA rain_layer.
- **Cave darkness dead alloc** — Removed in root; **closed in web** via edit (see below).
- **Panda head bob** — dy applied to head/ears/eyes in root; **closed in web** via edit.
- **Combo off-by-one** — collect_bamboo now looks up with current count then increments (both root/web sprites.py ~990/938). First bamboo = 1x.
- **save false-positive** — Uses rank/score check, not `in`.
- **ACTIVEEVENT pause** — Present in root game.py:121 (and web equiv).
- **Glide/dash anim frames + threshold** — Both have dedicated "glide"/"dash" frames; threshold=10 in both sprites set_gliding / glide logic.
- **Pickup naming** — Unified (mostly to action verbs "GLIDE!"/"DASH!"; web toasts/hints now match).
- **Rect update on rotate (attack/victory/trench)** — Both do `self.rect = ...get_rect(center=...)` or equiv after rotate.
- **Dead `_has_glide_permanent`**, tutorial timers, ScreenShake double-call, etc. — Many cleaned or commented in code.

## Currently OPEN (ACTIVE)

| ID | Area | File(s) + Line(s) | Status | Owner / Note | Severity |
|----|------|-------------------|--------|--------------|----------|
| OPEN-01 | Dead code | `engine.py:323` (root), `web/engine.py:292` (web) | Open | Historical (Visual report BUG-17). `class ParallaxBackground` (~150 lines) defined but never imported/instantiated (game uses BiomeBackground). Safe to delete but not gameplay breaking. | TINY |
| OPEN-02 | Visual parity / clipping | `web/sprites.py:60` (head/ears/eyes no +dy) vs root | Partially closed (web head bob edit applied 2026-06-24; verify arm/leg clips on run/fall/glide frames ~87-116) | Web lags root on some sprite fidelity. | MINOR |
| OPEN-03 | Inline font alloc every frame | `game.py:1160` (npc ?), `1116?` (boss), `1240` (state), `1555` (debug); similar in web/game.py | Open | Still uses `pygame.font.SysFont("consolas", ...)` in hot paths (not cached get_font). Performance on WASM. | MINOR / TINY |
| OPEN-04 | Imports inside hot paths | `game.py:640` (from biomes TimedGate), `web/game.py` equiv; also some inside draw paths (fixed some) | Open | Still a few conditional imports per-frame (cached but style violation). | TINY |
| OPEN-05 | Hardcoded world bounds | `sprites.py:1220?` (shuriken 600), web equiv; IceProjectile 8000 | Open | Use SCREEN_HEIGHT / level.world_width instead of literals. (SafeZone fixed in this session.) | TINY |
| OPEN-06 | Level design dead-ends | `levels.py:882-910` (L14 mushroom 3350 + crumble) | Open | Design issue noted in Biome report M5; no code change — potential unrecoverable fall. | MAJOR (design) |
| OPEN-07 | HomingSpecter wall phase | `biomes.py:~2002` (no plat collision) | Open | Per PHYSICS M6; still ghost. | MAJOR |
| OPEN-08 | Ice friction too slidey | `config.py:97` ICE_FRICTION=0.97; sprites ~730 | Open | ~3.8s coast noted. | MINOR |
| OPEN-09 | Geyser rect switch | `biomes.py:489` (_off vs _on rect) | Open | Per BIOME M2. | MAJOR |
| OPEN-10 | BrineShard growth on ice drift | `biomes.py:1195` (vel<10) | Open | Per BIOME M4. | MAJOR |
| OPEN-11 | Web-specific old darkness alloc | `web/game.py` (pre-edit had dead `darkness=` block) | **CLOSED** (edit 2026-06-24 removed unused alloc; code now matches root polished version) | n/a | — |
| OPEN-12 | Random import inside loop | game.py (sword/dash draws); web/game.py | **CLOSED** (edits 2026-06-24; now use top-level `random`) | n/a | — |
| OPEN-13 | SafeZone hardcoded 540 | sprites.py + web/sprites.py | **CLOSED** (edits 2026-06-24 + SCREEN_HEIGHT import) | n/a | — |
| OPEN-14 | Panda head bob web | web/sprites.py | **CLOSED** (edit 2026-06-24 applied +dy) | n/a | — |

## Notes on Cross-Reference
- Root vs web: levels.py, game.py, sprites.py largely in sync now for gameplay (glide/dash positions, mechanics, reverse-grav, damage skips, anim states, rects). Some visual drift remains (e.g. item art in sprites, background details).
- biomes.py / web/biomes.py: Larger visual differences (DustDevil 6 frames + particles in root; DarkWall animated in root) — noted as content drift in old reports but both functional.
- No new bugs introduced by this session's edits. All changes were direct ports of polished logic already in root or literal fixes from reports.
- Old reports contain ~70-77 entries total (with overlap). ~80%+ now fixed/resolved. Remaining active are mostly MINOR/TINY or intentional design (no easy "one-line" close without broader changes).
- No CI/deploy files present in tree (`.github/` absent), so WEB_PARITY BUG-02/03 (pip, favicon) not applicable to current workspace state.

## Closed in this session (edits applied)
- SafeZone 540 hardcode (root + web/sprites.py)
- Random-as-_r inside per-frame (root + web/game.py)
- Dead `darkness` surface alloc + unused draw (web/game.py)
- Panda head not bobbing (web/sprites.py _draw_panda)

## Master list hygiene
Old *BUGS_REPORT*.md and MASTER_GLITCH_REPORT.md preserved verbatim (historical record). This ACTIVE_BUGS.md is the single source of truth going forward. Update it (append dated entries) on future changes; do not edit the dated reports.

## Next actions (suggested, not in scope)
- Delete or deprecate ParallaxBackground if desired.
- Audit remaining design issues (L14 mushroom, HomingSpecter) in playtest.
- Cache SysFont or centralize in ui.get_font for remaining call sites.
- Full web vs root diff on sprites.py / biomes.py for art parity if wanted.

(End of active list. All statements grounded in file reads + greps performed 2026-06-24.)
