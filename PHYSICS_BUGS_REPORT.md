# BambooForest — Physics & Collision Bug Report

**Scanned files:** web/sprites.py (1927 lines), web/game.py (1489 lines), web/levels.py (1192 lines), web/biomes.py (2264 lines), web/config.py (206 lines), web/engine.py, web/ui.py  
**Root equivalents** also inspected for divergence.

---

## Bug Count by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| MAJOR    | 6 |
| MINOR    | 7 |
| TINY     | 3 |
| **Total**|**19**|

---

## CRITICAL (3)

### C1. Reverse Gravity (Level 18) Breaks Y-Collision — Player Cannot Land on Ceilings

**File:** `web/sprites.py`, lines 826–839  
**Root cause:** The Y-collision branch uses `dy > 0 or (dy == 0 and self.velocity_y >= 0)` to detect "landing." In reverse gravity (`gravity_multiplier = -1.0`, line 134 of config.py), `velocity_y` goes negative as the player falls **upward**. Negative `dy` triggers the `elif dy < 0` branch (line 836), which snaps `self.rect.top = hit.rect.bottom` and zeroes velocity — treating ceiling contact as a head-bonk instead of landing.

**Impact:** Player falls through reverse-gravity zones and can never stand on ceilings. Platforms placed at y=180 in Level 18 (lines 1092–1094) are unreachable from below (reverse gravity zone 4100..5000, line 1130) — the player clips through or bounces off without ever sticking.

**Proposed fix:** After the collision loop, add a reverse-gravity landing check:

```python
# In sprites.py, after line 839, add:
if self.gravity_multiplier < 0:
    # In reverse gravity, "ground" is above; re-check collisions
    for hit in pygame.sprite.spritecollide(self, platforms, False):
        if dy < 0 and self.velocity_y <= 0:
            self.rect.top = hit.rect.bottom
            self.velocity_y = 0
            self.is_on_ground = True
            self.jumps_remaining = 2 if self.has_double_jump else 1
            self.coyote_timer = 0.12
```

---

### C2. Double-Damage on VoidEater Collision (Level 17)

**File:** `web/game.py`, lines 607–613 (dedicated VoidEater check) and lines 807–827 (standard enemy collision loop)  
**Root cause:** VoidEater is checked **twice**: once via `is_dangerous()` at line 607–613 (deals `PLAYER_DAMAGE`), and again in the standard `pygame.sprite.spritecollide` loop at line 807. In the standard loop, `is_stompable=False` causes the stomp check (line 813) to fail, falling to the `else` branch (line 822–827) which deals *another* `PLAYER_DAMAGE`. The player takes 40 damage when touching an open VoidEater instead of 20.

**Proposed fix:** Skip VoidEater in the standard collision loop:

```python
# At line 808, after the spritecollide call:
for enemy in pygame.sprite.spritecollide(
        self.player, self.level.enemies, False):
    if not getattr(enemy, "alive_flag", True):
        continue
    # Skip enemies that have their own collision handler
    if type(enemy).__name__ in ("VoidEater", "ForgeHammer"):
        continue
    stomp_rect = self.player.get_stomp_rect()
    ...
```

Alternatively, move the skips to a class attribute check like `has_custom_collision`.

---

### C3. ForgeHammer (Level 15) Deals Double-Damage via Standard Collision Loop

**File:** `web/game.py`, lines 597–604 (dedicated ForgeHammer check, `PLAYER_DAMAGE * 2`) and lines 807–827 (standard loop)  
**Root cause:** Same pattern as C2. ForgeHammer's `is_stompable = False` and `die()` is a no-op (`pass`). The standard enemy loop at line 807 also catches it. On the standard loop path: stomp check fails → `else` branch deals `PLAYER_DAMAGE` (20). Combined with the dedicated check at line 602 (`PLAYER_DAMAGE * 2` = 40), the player takes **60 damage** from a single ForgeHammer frame contact, which is half their HP.

**Proposed fix:** Same as C2 — skip ForgeHammer in the standard collision loop, or remove the double-check and handle all damage in the dedicated block.

---

## MAJOR (6)

### M1. RisingLava Death Check Has ±2px Wave Clipping Window

**File:** `web/biomes.py`, lines 1471–1473 (wave animation); `web/game.py`, lines 535–541 (death check)  
**Root cause:** The lava surface oscillates vertically by ±2px via `math.sin(self._wave_timer * 3) * 2` (line 1472). The death check at game.py line 536 uses `self.player.rect.bottom > self.level.rising_lava.rect.top + 4`. The +4 buffer is meant to prevent instant-kill on wave peaks, but the 2px wave + 4px buffer + 540-600+ FLOOR_Y means players can visually clip into lava while the +4 buffer prevents death (false negative), or the wave trough drops below the kill line and kills the player when they're visually above it (false positive).

**Proposed fix:** Move to a lava-overlap-percentage check instead of a y-comparison:

```python
# game.py line 536, replace with:
overlap = self.player.rect.bottom - self.level.rising_lava.rect.top
if overlap > max(3, self.player.rect.h * 0.3) and self.player.invincible_timer <= 0:
```

---

### M2. Wind Zone Pushes Bypass Ice Physics System (Levels 6, 8)

**File:** `web/game.py`, lines 460–465; `web/sprites.py`, lines 722–737  
**Root cause:** Wind zones directly modify `self.player.rect.x` (game.py line 462) and only clamp to world bounds. On ice levels (`friction_mode == "ice"`), the player's X velocity is managed by ICE_ACCEL/ICE_FRICTION. Wind pushes the rect directly, bypassing velocity, friction, and sub-pixel accumulator (`_sub_x`). This creates disjoint gameplay where wind on ice (e.g., Level 8 combined with any wind zone) supernaturally overrides the ice physics.

**Impact:** Player slides on ice and gets pushed by wind without velocity system interaction. Wind can push player through wall edges (no wall collision check after wind push — line 462–464 only clamps to world width, not platform boundaries).

**Proposed fix:** Apply wind as velocity impulse instead of direct rect push:

```python
# game.py lines 461-465, replace with:
if pygame.sprite.collide_rect(self.player, wz):
    push = wz.get_push() * effective_dt
    self.player.velocity_x += push
    # No direct rect.x modification
```

---

### M3. TeleportPortals Can Chain-Teleport Same Frame

**File:** `web/game.py`, lines 556–574; `web/biomes.py` TeleportPortal class  
**Root cause:** The teleport loop (line 556) iterates ALL portals. Each portal has a cooldown (config.py: `PORTAL_COOLDOWN_SEC = 2.0`), but the `portal.teleport()` and `target.teleport()` methods only set the *called portal pair's* cooldown. If the target portal's position overlaps with another portal's activation area, the player could trigger a second teleport in the same frame before the loop `break` at line 574. With Level 17's 4 portal pairs (levels.py lines 1062–1066), pairs 0-3 overlap in range.

**Proposed fix:** Add an `active` attribute to the player and gate on it:

```python
# game.py, before the portal loop:
if getattr(self.player, '_teleported_this_frame', False):
    self.player._teleported_this_frame = False
# At line 562-566, after teleport:
self.player._teleported_this_frame = True
# ... existing break statement
```

---

### M4. MushroomSpring (Level 14) Side-Collision Triggers Bounce

**File:** `web/game.py`, lines 504–516  
**Root cause:** The bounce check uses `pygame.sprite.collide_rect` (full AABB overlap) combined with `self.player.rect.bottom < mush.rect.centery + 10`. If the player side-swipes the mushroom cap horizontally while falling (velocity_y > 0 from normal gravity), the collide_rect triggers. The centery+10 check only requires the player's feet to be above the mushroom's midpoint, not actually on the top surface. This means a side-graze launches the player upward.

**Proposed fix:** Require the player's feet to be near the actual top surface:

```python
# game.py lines 507-508, replace with:
if (self.player.velocity_y > 0
    and mush.compress_timer <= 0
    and self.player.rect.bottom <= mush.rect.top + 6
    and abs(self.player.rect.centerx - mush.rect.centerx) < mush.rect.w * 0.4):
```

---

### M5. Moving Platforms Lose Player on Ascending Vertical Movement

**File:** `web/game.py`, lines 377–399  
**Root cause:** The "was_riding" check uses a 10px vertical tolerance (line 388: `-10 <= (feet_y - plat_top) <= 10`) and suppresses snap when `velocity_y < 0` (jumping up, line 393). However, if the player is standing on a vertical moving platform that moves upward, and the player jumps, the `velocity_y < 0` check prevents re-snapping. When the player lands again on the same rising platform, the 10px tolerance may be exceeded if the platform rose faster than the player fell.

**Impact:** Players on vertically-moving platforms (Level 14: line 879, Level 15: lines 927, 931) can fall through after a jump. The platform moves ~4.8 px per frame at 80 px/s × 0.0167s dt × 60 FPS, which can outpace the velocity snap tolerance over 2–3 frames.

**Proposed fix:** Use the platform's previous position to compute relative motion even when velocity_y < 0:

```python
# game.py line 393, change to:
if was_riding:
    dx = mp.rect.x - old_mx
    dy = mp.rect.y - old_my
    self.player.rect.x += dx
    # Always snap Y if player is on or near the platform surface
    if self.player.velocity_y >= 0 or dy < 0:
        self.player.rect.bottom = mp.rect.top
        self.player.velocity_y = 0
        self.player.is_on_ground = True
```

---

### M6. HomingSpecter (L14-L18) Phases Through Walls — Unavoidable

**File:** `web/biomes.py`, lines 2002–2032  
**Root cause:** HomingSpecter applies direct velocity toward the player with no collision detection against platforms or walls (line 2017–2018). It is a ghost that moves through any geometry. Combined with its speed multiplier when the player is gliding (`_chase_speed * 1.3` = 234 px/s), it becomes an unstoppable threat in Levels 14–18 (each has 2-3 HomingSpecters — levels.py lines 893-894, 948-950, 1048-1049, 1110-1112).

**Impact:** If the player is in a tunnel or enclosed area, the HomingSpecter can come through the ceiling and strike from any angle. There's no counterplay except killing it (stompable) before it enters geometry.

**Proposed fix:** Add wall collision to HomingSpecter:

```python
# biomes.py, after line 2022, add wall collision:
if platforms:
    self.rect.center = (int(self._px), int(self._py))
    for plat in platforms:
        if self.rect.colliderect(plat.rect):
            # Bounce off wall
            self._vx *= -0.5
            self._vy *= -0.5
            self._px += self._vx * dt * 2
            self._py += self._vy * dt * 2
    self.rect.center = (int(self._px), int(self._py) + bob)
```

---

## MINOR (7)

### m1. ChaserEnemy Loses Sub-Pixel Precision on X Movement

**File:** `web/sprites.py`, lines 1612–1617  
**Root cause:** Unlike `PatrolEnemy` which tracks a `pos_x` float then assigns `rect.x = _fl(pos_x)`, the `ChaserEnemy` directly assigns `self.rect.x += _fl(ENEMY_CHASE_SPEED * dt)`. Over 10 seconds of chasing at 180 px/s, the chaser drifts by up to ~3px from its intended position due to accumulated truncation.

**Proposed fix:** Add `_px` tracking to ChaserEnemy (same pattern as PatrolEnemy's `pos_x`).

---

### m2. Ice Friction Coasting Time Is Too Long (3.8s to Stop)

**File:** `web/sprites.py`, lines 730–737; `web/config.py`, line 97  
**Root cause:** `ICE_FRICTION = 0.97` per frame. Starting from `PLAYER_SPEED * 1.5 = 540 px/s`, the velocity decays exponentially:  
`540 × 0.97^(225) ≈ 0.5` → ~3.75 seconds at 60 FPS to reach the stop threshold (`abs(self.velocity_x) < 0.5`). This makes ice platforms feel unresponsive.

**Proposed fix:** Increase ICE_FRICTION to `0.985` (smoother slide, same time window perception) or reduce max_ice_v from `PLAYER_SPEED * 1.5` to `PLAYER_SPEED * 1.2`.

---

### m3. PoisonSpore Spawns Both Spores at Exact Same Position

**File:** `web/biomes.py`, lines 1389–1392  
**Root cause:** `SporePuffer.get_new_spores()` spawns two `PoisonSpore` at `(sx, sy)` with opposite drift. Both start at the exact same pixel position. While the drift separates them over time, in the first ~0.5 seconds they overlap, causing potential double-damage when `pygame.sprite.spritecollide` catches both overlapping sprites.

**Proposed fix:** Offset the spawns by ±5px in X:

```python
# biomes.py lines 1391-1392:
self.pending_spores.append(PoisonSpore(sx - 6, sy, -SPORE_DRIFT * 0.6))
self.pending_spores.append(PoisonSpore(sx + 6, sy, SPORE_DRIFT * 0.6))
```

---

### m4. BrineShard/DustDevil Invincibility Uses Fragile String Comparison

**File:** `web/game.py`, lines 720, 779  
**Root cause:** `type(enemy).__name__ in ("BrineShard", "DustDevil")` is hardcoded in three places (lines 720 and 779 for staff/shuriken). If classes are renamed, refactored, or subclasses created, these checks silently fail — the new class name won't match and the enemy becomes killable.

**Proposed fix:** Add a class attribute:

```python
# On BrineShard/DustDevil:
is_invincible: bool = True  # or a similar semantic flag

# game.py lines 720, 779:
if getattr(enemy, 'is_invincible', False):
    continue
```

---

### m5. PatrolEnemy Has No Return-to-Origin After Knockback

**File:** `web/sprites.py`, lines 1565–1584  
**Root cause:** PatrolEnemy tracks `pos_x` relative to `origin_x`, but gravity and collision are checked every frame (lines 1573–1580). If the enemy is knocked off its platform (from player collision knockback — though knockback is only applied to player, not enemies), or pushed by biome mechanics, it falls without any logic to return to its patrol position.

**Impact:** If a biome mechanic pushes a PatrolEnemy off a ledge (wind, geyser), it falls into a trench and is permanently removed from gameplay, reducing the level's challenge.

**Proposed fix:** Add vertical distance check — if enemy falls more than 200px below origin, respawn:

```python
# sprites.py, in PatrolEnemy.update, after line 1580:
if self.rect.top > 700:
    self.pos_x = self.origin_x
    self.rect.bottom = FLOOR_Y + 20  # respawn above floor
```

---

### m6. TidalCrab Falls and Soft-Respawns Without Gate Awareness (Level 16)

**File:** `web/biomes.py`, lines 1690–1693  
**Root cause:** When a TidalCrab falls through its vanished gate, it checks `self.rect.top > 600` and respawns at `_py = -40.0` (above the screen). It re-falls unconditionally. If the gate group that originally supported it is still intangible, the crab falls again and loops. This can create an infinite cycling visual glitch.

**Proposed fix:** Add respawn-count tracking or check gate phase:

```python
# biomes.py, before line 1691:
if self.rect.top > 600:
    self.fall_count = getattr(self, 'fall_count', 0) + 1
    if self.fall_count < 3:
        self._py = -40.0
        self.rect.y = -40
    else:
        # Teleport to nearest valid platform
        self._py = self.start_y - 30
        self._px = self.start_x
```

---

### m7. DarkWall Platform Add/Remove During Crystal Check Can Cause Physics Glitch

**File:** `web/biomes.py`, lines 2257–2264; `web/game.py`, lines 615–617  
**Root cause:** DarkWall removes itself from `self._platforms` (the `self.level.platforms` group) when a crystal is lit, and re-adds when unlit. The update at biomes.py line 2248 checks crystals. But game.py line 616 `dw.update(effective_dt)` runs AFTER the player's physics update (line 403). If a DarkWall is removed mid-frame, the player's collision with it during the physics update is inconsistent — the next frame the wall is gone but the player was already blocked.

**Proposed fix:** Update DarkWalls *before* player physics, or mark them for delayed removal:

```python
# game.py, move dark_wall.update() before player.update():
# Execute at line ~398 (before line 401):
for dw in self.level.dark_walls:
    dw.update(effective_dt)
```

---

## TINY (3)

### t1. RisingLava Frame-Rate Inconsistency

**File:** `web/config.py`, line 116: `LAVA_RISE_SPEED = 25.0`  
**Root cause:** At 60 FPS, `dt ≈ 0.0167`, lava rises at `25 × 0.0167 ≈ 0.417 px/sim-step`. At 30 FPS, `dt ≈ 0.033`, it rises at `25 × 0.033 ≈ 0.825 px/sim-step`. dt is clamped to max 0.05 (game.py line 98), but at very low FPS the lava rises nearly 50% faster, making the rush-pressure inconsistent across hardware.

**Proposed fix:** Normalize against target FPS: `LAVA_RISE_SPEED = 25.0 * (FPS / 60.0)` or better, `LAVA_RISE_SPEED = 1500.0` (per-second ÷ 60 for frame-independent movement).

---

### t2. DustDevil Checked in Shuriken Loop But Never Spawns in Levels 14-18

**File:** `web/game.py`, line 720  
**Root cause:** The shuriken check skips `"DustDevil"` but DustDevils don't appear in Levels 14-18. The check is dead code for the late-game. Similarly, `"BrineShard"` doesn't appear past Level 8. These checks inflate the skip list.

**Proposed fix:** Remove the per-enemy-type skip list and use the `is_invincible` class attribute pattern (see m4 fix).

---

### t3. FLOOR_Y = 490 but SafeZone Rect Pinned to y=540

**File:** `web/sprites.py`, line 1878: `self.rect = self.image.get_rect(bottomleft=(x, 540))`  
**Root cause:** The SafeZone rect's bottom is at y=540 (bottom of screen), using hardcoded `540` instead of `SCREEN_HEIGHT`. If SCREEN_HEIGHT ever changes, the safe zone will be misaligned from the floor.

**Proposed fix:** Use `SCREEN_HEIGHT`:

```python
self.rect = self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT))
```

---

## Top 5 Most Impactful Bugs (by gameplay severity)

| Rank | ID | Severity | Description | Fix Effort |
|------|----|----------|-------------|------------|
| **1** | **C1** | CRITICAL | Reverse gravity (Level 18) breaks Y-collision — player can't stand on ceilings. Level 18's signature mechanic is unplayable. | ~15 lines |
| **2** | **C2** | CRITICAL | VoidEater (Level 17) deals double damage (40 HP per hit, 1/3 of max HP). Players die in 3 hits instead of 6. | ~3 lines |
| **3** | **C3** | CRITICAL | ForgeHammer (Level 15) deals triple effective damage (60 HP = 1/2 max HP per hit). Game-ending in tight platform sections. | ~3 lines |
| **4** | **M1** | MAJOR | RisingLava (Level 15) death zone oscillates with wave animation, causing inconsistent kill zone. Players die unpredictably. | ~5 lines |
| **5** | **M3** | MAJOR | Teleport chain (Level 17) can trigger multiple teleports in one frame, teleporting player past intended destination. Breaks portal puzzle. | ~4 lines |

**Total fix lines for top 5:** ~30 lines of targeted changes across 3 files (sprites.py, game.py, biomes.py).

---

## Summary

- **19 bugs found** across 4 code files (sprites.py, game.py, biomes.py, config.py)
- **3 CRITICAL** — all involve incorrect collision handling (reverse gravity, double-damage on VoidEater and ForgeHammer)
- **6 MAJOR** — physics integration gaps (wind bypassing ice system, MushroomSpring side-collision, moving platform snap, HomingSpecter wall phasing, lava wave clipping, teleport chaining)
- **7 MINOR** — precision loss, incomplete invincibility checks, coasting feel, double-spawn overlaps, TidalCrab soft-respawn loops
- Top 5 bugs can be fixed with ~30 lines of targeted code changes
