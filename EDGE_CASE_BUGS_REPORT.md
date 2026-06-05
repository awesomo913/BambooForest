# BambooForest — Edge Cases & State Machine Glitch Hunt
**Agent 3 report — 2026-06-05**
Files read: `game.py`, `web/game.py`, `sprites.py`, `web/sprites.py`, `save.py`, `web/save.py`, `audio.py`, `web/audio.py`, `engine.py`, `levels.py`, `config.py`

---

## MAJOR Bugs

### M-1 · `save_high_score` can return a false-positive "made the list"
**Files:** `save.py:34`, `web/save.py:34`

```python
return entry in scores   # uses dict __eq__, not identity
```

After `scores = scores[:MAX_SCORES]`, the new `entry` dict is checked with `in`, which compares by value (not object identity). If any existing top-5 entry happens to have the same `{"score": X, "level": Y}` values as the new one, the check returns `True` even though the new run was sliced out. Result: victory screen shows "HIGH SCORE!" badge for a run that didn't actually make the leaderboard.

**Fix:** compare object identity or check whether the slice kept the entry by rank, e.g.:
```python
# option: compare before slicing
return len(scores) < MAX_SCORES or entry["score"] >= scores[-1]["score"]
```

---

### M-2 · `AudioManager.play()` mutates shared Sound volume — affects all concurrent instances
**Files:** `audio.py:210-213`, `web/audio.py:228-233`

```python
sound.set_volume(_BASE_VOLUME * 0.7)   # ← changes volume on the Sound object
...
sound.play()
```

`pygame.mixer.Sound.set_volume()` applies to the Sound object, not to a specific playback channel. If "collect" fires at t=0 and again at t=0.06s (just past the 0.05s rate limit), the second call changes the volume of the still-playing first instance mid-play, causing an audible click or volume pop.

**Fix:** use the Channel returned by `sound.play()`:
```python
ch = sound.play()
if ch:
    ch.set_volume(_BASE_VOLUME * 0.7 if elapsed < 0.2 else _BASE_VOLUME)
```

---

### M-3 · Rising lava re-triggers death sound on an already-dead player every frame
**File:** `game.py:563-571`

```python
if (self.player.rect.bottom > self.level.rising_lava.rect.top + 4
        and self.player.invincible_timer <= 0):        # no dead-player guard
    self.player.health = 0
    self.player.dead = True
    self.audio.play("death")                           # fires repeatedly
    self.shake.trigger(12, 0.4)
```

Once the player dies from lava, `death_anim` starts and `player.dead = True`. The lava check has no `and not self.player.dead` guard. Because `player.invincible_timer` is never set by this code path, the condition stays True every frame. The 0.5s rate-limit on "death" means the sound fires ~twice during the 0.5s death animation, producing an unintended double-death sound.

**Fix:** add `and not self.player.dead` to the lava kill condition (line 566).

The `outro_active` path is safe because `player.invincible_timer = 999.0` is set at goal touch (line 922), which blocks the lava check via `invincible_timer <= 0`. Only the non-outro normal-death path is affected.

---

### M-4 · `_has_glide_permanent` is dead code with a misleading comment
**File:** `game.py:93-94`

```python
# Glide persists across levels once collected
self._has_glide_permanent: bool = False
```

This field is initialized to `False` and **never set to `True`** anywhere in `game.py` or `web/game.py`. In `_load_level` and `_respawn_at_checkpoint`, the comment explicitly says "Glide + Dash are per-level timed pickups (not permanent)" — the opposite of the field name's implication.

The field adds confusion and any future developer who finds it will assume glide persistence should be wired. Either remove it, or wire it up to the glide pickup collection (lines 696-706) if persistence is actually intended.

---

### M-5 · Tutorial timers set and decremented but never used to control hint display
**File:** `game.py:88-98, 983-985, 1176-1185`

```python
# In __init__:
self._weapon_tutorial_timer: float = 0.0
self._glide_tutorial_timer:  float = 0.0
self._ice_tutorial_timer:    float = 0.0

# In _update_gameplay:
if self._weapon_tutorial_timer < 999 and self._weapon_tutorial_timer > 0:
    self._weapon_tutorial_timer -= effective_dt     # decremented but...
```

```python
# In _draw():
if (self.player.has_bamboo_weapon and not self._weapon_used):
    self._draw_weapon_hint()                         # ...never checked here
```

All three tutorial hint displays are gated only on the `_*_used` bool flags. The timers are set to `999.0` on pickup (a sentinel for "show this") and decremented, but their value is **never read** to control visibility. The `_used` flag is the sole display gate.

Effect: the hints show permanently until the player uses the ability, regardless of timer value. The 999-sentinel and timer-decrement logic are dead code. Remove the timers or wire them as a timeout to auto-dismiss the hint.

---

### M-6 · `ScreenShake.update()` in `_update_gameplay` discards its return value — rendering shake computed separately in `_draw`
**Files:** `game.py:989, 1018`

```python
# _update_gameplay — advances timer, return value thrown away:
self.shake.update(effective_dt)           # line 989

# _draw — uses return value for rendering:
shake_off = self.shake.update(0)          # line 1018
```

`ScreenShake.update()` calls `random.randint` on every invocation when the timer is active. The first call in `_update_gameplay` generates random offsets that are discarded; the second call in `_draw` generates the offsets actually used for rendering.

Result: 2× the RNG calls needed per active-shake frame. The timer is also advanced once and then called with `dt=0`, meaning the draw call always sees the post-advance timer state. This is functionally correct but semantically confusing and wasteful.

**Fix:** split responsibilities — advance timer in update (no return needed), sample offset only in draw:
```python
# _update_gameplay:
self.shake.tick(effective_dt)          # new: just advances timer

# _draw:
shake_off = self.shake.get_offset()    # new: samples current offset once
```

---

### M-7 · No `pygame.ACTIVEEVENT` handler — game doesn't auto-pause on focus loss
**File:** `game.py:121-145` (and `web/game.py` equivalently)

`_handle_events()` handles `QUIT`, `KEYDOWN`, `KEYUP`, `MOUSEBUTTONDOWN` but not `pygame.ACTIVEEVENT`. When the player alt-tabs or the window loses focus, the game keeps running at full speed. The player returns to find their character dead or in an unexpected position. The pause-on-focus-loss behavior that most players expect is absent.

**Fix:**
```python
if event.type == pygame.ACTIVEEVENT:
    if hasattr(event, 'gain') and not event.gain and self.state == ST_PLAYING:
        self.state = ST_PAUSED
```

---

### M-8 · Combo: `COMBO_MULTIPLIERS[0] = 1` is dead code — first bamboo always gives 2×
**File:** `sprites.py:882-887`, `config.py:48`

```python
def collect_bamboo(self) -> int:
    self.combo_count = min(self.combo_count + 1, len(COMBO_MULTIPLIERS) - 1)
    self.combo_timer = COMBO_WINDOW
    mult = COMBO_MULTIPLIERS[min(self.combo_count, len(COMBO_MULTIPLIERS) - 1)]
```

`combo_count` starts at 0. After `min(0 + 1, 3) = 1`, the multiplier index is 1. So the FIRST bamboo of a fresh combo gives `COMBO_MULTIPLIERS[1] = 2×`. `COMBO_MULTIPLIERS[0] = 1` is never reached by design. This means:

| Bamboos in window | Intended | Actual |
|---|---|---|
| 1st | 1× | 2× |
| 2nd | 2× | 3× |
| 3rd | 3× | 4× |
| 4th+ | 4× | 4× |

Either the intent is 1-2-3-4× (first should be 1×) in which case the increment should happen AFTER the lookup, or `COMBO_MULTIPLIERS[0]` should be removed and the array treated as 1-indexed. Neither is currently correct.

**Fix (increment after lookup):**
```python
mult = COMBO_MULTIPLIERS[min(self.combo_count, len(COMBO_MULTIPLIERS) - 1)]
self.combo_count = min(self.combo_count + 1, len(COMBO_MULTIPLIERS) - 1)
```

---

## MINOR Bugs

### m-1 · `pygame.font.SysFont()` allocated every rendered frame
**File:** `game.py:1073, 1145, 1161, 1454`

Four call sites create a new font object every frame:
- NPC "?" bubble: `pygame.font.SysFont("consolas", 18, bold=True)` (line 1073)
- Boss HP "BOSS" label: `pygame.font.SysFont("consolas", 12, bold=True)` (line 1145)
- Boss state indicator: `pygame.font.SysFont("consolas", 16, bold=True)` (line 1161)
- Debug overlay: `pygame.font.SysFont("consolas", 14, bold=True)` (line 1454)

`SysFont` performs a font lookup and cache check on every call. On slower hardware (especially the web/WASM target), this causes perceptible frame drops when a boss is alive or debug mode is on. Cache these as `Game.__init__` attributes.

---

### m-2 · Dead player can start an attack via mouse click during death animation
**File:** `game.py:141-145`, `sprites.py:896-904`

```python
elif event.button == 1 and self.state == ST_PLAYING:
    if self.player and self.player.attack():     # no dead check here
```

`Player.attack()` has no `self.dead` guard:
```python
def attack(self) -> bool:
    if (self.has_bamboo_weapon and not self.is_attacking
            and self.attack_cooldown <= 0 and not self.is_dashing):
        self.is_attacking = True
        ...
```

A mouse click during the death animation (still `ST_PLAYING`) sets `is_attacking = True`. Because `Player.update()` returns early when dead, `attack_timer` never counts down. The `is_attacking` flag stays `True` until the player object is replaced by `_respawn_at_checkpoint`. This also causes the sword arc to render on the dead player.

**Fix:** add `or self.dead` to the attack guard condition, or check `self.player.dead` in the event handler.

---

### m-3 · Checkpoint identity is keyed only on `spawn_x` — two CPs at the same X both restore
**File:** `game.py:308-317`

```python
activated_xs = set()
for cp in self.level.checkpoints:
    if cp.activated:
        activated_xs.add(cp.spawn_x)       # x-only deduplication
...
for cp in self.level.checkpoints:
    if cp.spawn_x in activated_xs:
        cp.activate()                       # any CP at that X gets restored
```

If two checkpoints share the same X position (e.g., one on a platform and one on the floor directly below), touching one restores both on the next respawn. Use `(spawn_x, spawn_y)` as the key instead.

---

### m-4 · `_outro_anchor_x` not declared in `__init__` — relies on `hasattr` guard
**File:** `game.py:962, 970-971, 976-977`

```python
self._outro_anchor_x = self.player.rect.x    # set mid-method, not in __init__
...
if hasattr(self, '_outro_anchor_x'):
    self.player.rect.x = self._outro_anchor_x
```

The `hasattr` guard works but the field should be declared as `self._outro_anchor_x: int = 0` in `__init__` alongside the other outro state (`_outro_active`, `_outro_timer`, `_outro_speed`). The current approach leaves the attribute absent between `__init__` and first outro, which breaks static analysis and type checkers.

---

### m-5 · NPC "?" bubble animates during pause (uses wall-clock time)
**File:** `game.py:1061-1062`

```python
t_ms = pygame.time.get_ticks()
bounce = math.sin(t_ms / 200.0) * 5
```

`pygame.time.get_ticks()` advances even when the game is paused. The NPC indicator keeps bouncing while the pause overlay is visible. Use `effective_dt`-driven accumulator instead for consistency with other animations.

---

## TINY Issues

### t-1 · `import random as _r` inside per-frame render loop
**File:** `game.py:1291`

```python
for _ in range(3):
    import random as _r      # executed on every impact sparkle, every frame
    px = tip_x + _r.randint(-4, 4)
```

Python's import cache makes this essentially free, but it's an antipattern. Move the import to the top of the file alongside the other stdlib imports.

---

### t-2 · Three config imports and one biome import inside the gameplay hot path
**Files:** `game.py:577, 695, 945`

```python
from biomes import TimedGate                                # line 577 — executed every frame with timed gates
from config import GLIDE_DURATION_SEC, DASH_DURATION_SEC   # line 695 — every gameplay frame
from config import TRENCH_DEATH_Y                           # line 945 — every gameplay frame
```

These are cached by Python after first import, so runtime cost is one dict lookup per call. Still: move to top-level imports for clarity and to avoid confusing future readers who might assume these are conditional imports.

---

### t-3 · `BambooShuriken` kill threshold hardcodes `600` instead of `SCREEN_HEIGHT + margin`
**File:** `sprites.py:1220`

```python
if self.lifetime <= 0 or self.pos_y > 600:
    self.kill()
```

`SCREEN_HEIGHT = 540`. The margin of 60px is reasonable but if `SCREEN_HEIGHT` ever changes, this breaks. Use `SCREEN_HEIGHT + 60` or `FLOOR_Y + 200`.

---

### t-4 · `IceProjectile` kill threshold hardcodes `8000` for world right boundary
**File:** `sprites.py:1283`

```python
if self.lifetime <= 0 or self.pos_x < -50 or self.pos_x > 8000:
    self.kill()
```

Maximum level width is 7500px (`LEVEL_WIDTHS` max in `config.py:179`). The 8000 cap is fine for current levels but is not tied to `LevelState.world_width`. Pass world width to the projectile constructor or rely solely on `lifetime` (already 1.5s × 800px/s = 1200px range, well within any level).

---

### t-5 · Redundant `player.score` assignment after `_load_level` in level transition
**File:** `game.py:369-373`

```python
self._total_score = self._carry_score      # line 370
self._load_level(next_num)                 # sets player.score = self._total_score internally (line 283)
self.player.score = self._carry_score      # line 372 — same value, redundant
self.player.health = self._carry_health
```

Since `_load_level` already does `self.player.score = self._total_score` and `_total_score == _carry_score` at this point, line 372 is a no-op. Not harmful, just confusing.

---

## State Machine Coverage Summary

| Transition | Handled? | Notes |
|---|---|---|
| ST_MENU → ST_PLAYING | ✓ | via RETURN key |
| ST_PLAYING → ST_PAUSED | ✓ | via ESC |
| ST_PAUSED → ST_PLAYING | ✓ | via ESC |
| ST_PAUSED → ST_MENU | ✓ | via Q |
| ST_PLAYING → ST_LEVEL_TRANS | ✓ | via goal touch + outro complete |
| ST_LEVEL_TRANS → ST_PLAYING | ✓ | via transition animation complete |
| ST_PLAYING → ST_GAME_OVER | ✓ | lives = 0 after death |
| ST_PLAYING → ST_VICTORY | ✓ | last level completed |
| ST_GAME_OVER → ST_MENU | ✓ | via RETURN |
| ST_VICTORY → ST_MENU | ✓ | via RETURN |
| Any → pause on focus loss | ✗ | **M-7** above |
| ST_LEVEL_TRANS — key input | silent | no handler branch — intentional skip |

No softlock paths found. All states have at least one exit path.

---

## Death & Respawn Checklist

| Check | Status |
|---|---|
| `lives` decremented correctly | ✓ |
| `_total_score` captured before respawn | ✓ |
| Checkpoint `activated` state preserved across respawn | ✓ |
| `_jump_pressed` cleared on respawn | ✓ |
| `combo_count` / `combo_timer` reset (new Player) | ✓ |
| `input_locked` cleared by `reset_state()` | ✓ |
| `invincible_timer` starts at 0 on respawn | ✓ |
| `is_gliding` / `is_dashing` cleared by `reset_state()` | ✓ |
| `pending_throws` / `pending_ice_casts` cleared | ✓ |
| `ice_cast_cooldown` cleared | ✓ |
| Weapon tutorial re-shown if weapon not collected on respawn | ✓ |
| `_outro_active` reset on level load / respawn | ✓ |
| Lava kill double-fires death sound on dead player | ✗ | **M-3** |
| Dead player can attack via mouse click | ✗ | **m-2** |

---

## Persistence Across Levels Checklist

| Ability | Persists? | Mechanism |
|---|---|---|
| Double jump | ✓ | Re-granted in `_load_level` if `level_num >= DOUBLE_JUMP_LEVEL` |
| Ice magic | ✓ | `_has_ice_magic_permanent` checked in `_load_level` + `_respawn` |
| Glide | ✗ (per-level) | Must re-collect each level (per-design, contradicts `_has_glide_permanent` comment) |
| Dash | ✗ (per-level) | Must re-collect each level |
| Score | ✓ | `_total_score` / `_carry_score` carry over |
| Health | ✓ (carry) | `_carry_health` on advance, full HP on respawn |
| `_has_glide_permanent` field | never set | **M-4** — dead code |
