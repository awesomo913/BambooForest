# BambooForest — Visual & UI Bug Report

**Agent:** Rendering & Visual Glitch Hunter  
**Files inspected:** `web/sprites.py`, `web/backgrounds.py`, `web/engine.py`, `web/ui.py`, `web/game.py`  
**Total bugs found:** 20 (2 CRITICAL · 5 MAJOR · 8 MINOR · 5 TINY)

---

## CRITICAL

---

### BUG-01 · Pause encyclopedia cards overflow screen horizontally
**File:** `web/ui.py:722`  
**Severity:** CRITICAL  

```python
cols = 5
col_w = 180
start_x = (SCREEN_WIDTH - cols * col_w) // 2
# (800 - 5*180) // 2  =  (800 - 900) // 2  =  -50
```

5 columns × 180 px = **900 px**, which exceeds `SCREEN_WIDTH = 800`. `start_x = -50`. The entire first column of enemy cards is clipped 50 px off the left edge and is **unclickable** (mouse events at negative x are never in any card rect). Visual: left column appears sliced; name tags and sprites are cut off.

**Fix:** Drop to 4 columns or reduce `col_w` to ≤ 155 px so `4 × 155 + 3 × gap ≤ 800`.

---

### BUG-02 · Title screen gallery overflows screen vertically (bottom half unclickable)
**File:** `web/ui.py:562–593`  
**Severity:** CRITICAL  

```python
rows = (len(_CHARACTERS) + cols - 1) // cols  # len=24 → 6 rows
total_h = rows * card_h + (rows - 1) * gap_y   # 6*95 + 5*8 = 610
start_y = btn_y + btn_h + 14                   # ≈230
# start_y + total_h ≈ 230 + 610 = 840 > SCREEN_HEIGHT (540)
```

The gallery is **300 px taller than the screen**. Rows 4–6 (12 of 24 characters) are completely off-screen and unclickable. The "Press ENTER" prompt at `SCREEN_HEIGHT - 62 = 478` is obscured by visible card rows. 

**Fix:** Either add a scrollable panel, reduce `card_h` and `gap_y`, or limit the gallery to 2 rows and paginate.

---

## MAJOR

---

### BUG-03 · Rotated sprite image and physics rect desynced (attack lean, victory dance, trench fall)
**File:** `web/sprites.py:1064, 1078, 1113–1114`  
**Severity:** MAJOR  

`pygame.transform.rotate()` returns a **larger** surface (bounding box of the rotation). In all three cases below, `self.image` is replaced with the rotated surface but **`self.rect` is never updated**:

```python
# trench fall (line 1064)
self.image = pygame.transform.rotate(frame, angle)  # rect NOT updated

# victory dance (line 1078)
self.image = pygame.transform.rotate(frame, angle)  # rect NOT updated

# attack lean (line 1113)
frame = pygame.transform.rotate(frame, lean)
self.image = frame …                                 # rect NOT updated
```

Because `_draw()` blits at `sprite.rect.move(cam_x, cam_y)` (the old top-left corner), the rotated panda renders shifted **up and left** relative to its physics hitbox. At 15° (victory dance peak) this is ~8 px in each axis; at 6° (attack lean) ~3 px. The player visually "floats" off their collision box.

**Fix:**
```python
new_image = pygame.transform.rotate(frame, angle)
self.image = new_image
# update ONLY visual position, keep physics rect center stable
self.rect = new_image.get_rect(center=self.rect.center)
```

---

### BUG-04 · Rain streaks in TidalBackground render fully opaque (alpha ignored)
**File:** `web/backgrounds.py:567–569`  
**Severity:** MAJOR  

```python
surf = pygame.Surface((self.w, SCREEN_HEIGHT))   # no SRCALPHA!
…
pygame.draw.line(surf, (180, 200, 220, 100),      # 4-tuple with alpha
                 (sx, sy), (sx - 2, sy + 8), 1)
```

`surf` is a plain (non-SRCALPHA) surface. When a 4-element color tuple is passed to `pygame.draw.*` on a non-alpha surface, **the alpha component is silently discarded**. All 50 rain streaks render as solid `(180, 200, 220)` grey lines instead of the intended 39%-opacity translucent streaks. The rain looks like harsh opaque scratches instead of misty precipitation.

**Fix:** Create a temporary SRCALPHA surface for the rain layer and composite it:
```python
rain_layer = pygame.Surface((self.w, SCREEN_HEIGHT), pygame.SRCALPHA)
rain_layer.fill((0, 0, 0, 0))
for _ in range(50):
    pygame.draw.line(rain_layer, (180, 200, 220, 100), …)
surf.blit(rain_layer, (0, 0))
```

---

### BUG-05 · VoidBackground soul orbs render fully opaque (alpha ignored)
**File:** `web/backgrounds.py:903–904`  
**Severity:** MAJOR  

```python
surf = pygame.Surface((self.w, SCREEN_HEIGHT))   # no SRCALPHA
…
pygame.draw.circle(surf, (*col, 100), (ox, oy), 4)   # alpha ignored
```

Same root cause as BUG-04. The 50 soul-orb halos (`alpha=100`, should be 39% opacity) render as fully-opaque circles. The "drifting soul" motif loses its ghostly translucency and instead looks like solid colored dots.

**Fix:** Same pattern — draw orbs on an SRCALPHA temporary surface, then blit onto `surf`.

---

### BUG-06 · Power-up countdown timers overflow screen right edge
**File:** `web/ui.py:205–223`  
**Severity:** MAJOR  

```python
pwr_x = SCREEN_WIDTH - 100  # = 700
if player.glide_time_remaining > 0:
    draw_text(…, f"GLIDE {gt}s", 11, …, pwr_x + 14, …)
    pwr_x += 75              # pwr_x → 775
if player.dash_time_remaining > 0:
    draw_text(…, f"DASH {dt_}s", 11, …, pwr_x, …)
    pwr_x += 60              # pwr_x → 835
if player.has_bamboo_weapon:
    draw_text(…, f"SWORD {wt}s", 11, …, pwr_x, …)  # centered at 835
```

When all three power-ups are active simultaneously:
- DASH text centered at x=775 → right edge ≈ 800 (barely on screen)
- SWORD text centered at x=835 → mostly **35 px off-screen** (screen is 800 wide)

The sword timer is completely invisible when dash and glide are also active.

**Fix:** Lay out power-up indicators vertically (stacked rows) instead of horizontally, or start from the right and flow left.

---

### BUG-07 · Cave darkness overlay allocates dead surface every frame
**File:** `web/game.py:1062–1074`  
**Severity:** MAJOR (performance: ~3 allocations/frame in cave level)  

```python
if self.level.is_dark:
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))   # allocated
    darkness.fill((0, 0, 0))
    pygame.draw.circle(darkness, (0, 0, 0), (px, py), DARK_RADIUS)
    for crystal in self.level.crystals:
        if crystal.is_lit():
            pygame.draw.circle(darkness, (0, 0, 0), (cx, cy), CRYSTAL_RADIUS)
    darkness.set_colorkey((0, 0, 0))
    # 'darkness' is NEVER blitted — dead code
    # real overlay starts here:
    dark_overlay = pygame.Surface(…, pygame.SRCALPHA)
    …
```

The `darkness` surface is created, filled, and drawn on but **never used**. The actual overlay is `dark_overlay`. At 60 FPS this wastes one 800×540 surface allocation + two `draw.circle` calls every frame during the cave level.

**Fix:** Delete lines 1062–1074 (the `darkness` variable block entirely). The `dark_overlay` logic below is correct and self-sufficient.

---

## MINOR

---

### BUG-08 · Panda head does not bob during idle animation
**File:** `web/sprites.py:38–75, 80–83`  
**Severity:** MINOR  

`_draw_panda()` accepts `body_dy` which shifts the body ellipse, belly, arms, and legs. But the head, ears, eye patches, eyes, nose, and mouth are all drawn at **absolute positions** (e.g., `pygame.draw.circle(surf, …, (w // 2, 12), 11)`) without applying `dy`. The idle animation bobs the body by 1 px between frame 0 and frame 1, but the head stays stationary — the panda's head "floats" disconnected from the torso.

**Fix:** Apply `dy` offset to all head-drawing calls inside `_draw_panda`.

---

### BUG-09 · Panda arm and leg tips clip at sprite boundaries (3 frames)
**File:** `web/sprites.py:87–116`  
**Severity:** MINOR  

Several frame definitions place limbs outside the 36×44 surface:

| Frame | Offending rect | Clip |
|-------|---------------|------|
| run[0] | `arm_r=(29,22,7,12)` | x=29+7=36 = exact right edge |
| fall | `arm_l=(-1,16,8,12)` | x=-1, loses 1px of left arm |
| glide | `arm_l=(-4,14,10,8)` | x=-4, loses 4px of left arm |

`pygame.draw.rect` silently clips these — no crash — but the panda's arm tips are slightly truncated in run, fall, and glide poses.

**Fix:** Widen the surface by 4–6 px and adjust reference x coordinates, or shift limb positions inward.

---

### BUG-10 · Shadow Panther tail tip clipped (half the circle off-surface)
**File:** `web/sprites.py:448`  
**Severity:** MINOR  

```python
pygame.draw.circle(surf, body_c, (44, 6 + dy), 2)
```

`surf` is 44 px wide (x range 0–43). Drawing a radius-2 circle centered at x=44 means the **entire circle is off the right edge** — the tail tip is invisible. The visual is a hard-clipped tail stub instead of a rounded tip.

**Fix:** Shift to `(41, 6 + dy)` or widen the surface to 48 px.

---

### BUG-11 · Platform tiles visually differ between level loads (unseeded random)
**File:** `web/sprites.py:152–196`  
**Severity:** MINOR  

`generate_platform_tile()` uses `random.randint()` without seeding for wood grain shade, moss tufts, and bamboo cross-section positions. On every respawn `build_level_state()` is called and all platforms are rebuilt, so each respawn generates **visually different** wood grain and moss patterns. This is inconsistent with players expecting stable level visuals after death.

**Fix:** Seed with a deterministic value per platform: `random.seed(hash((x, y, width, height)))` at the top of `generate_platform_tile`, then `random.seed()` at the end to restore global state.

---

### BUG-12 · Mana "READY" indicator dot is outside the mana bar
**File:** `web/ui.py:165–170`  
**Severity:** MINOR  

```python
pygame.draw.rect(screen, col, (48, 40, mana_w, 10))  # bar ends at x=48+150=198
…
pygame.draw.circle(screen, …, (207, 45), 3)           # dot at x=207, 9px past bar end
```

The pulsing "READY" dot is drawn 9 pixels to the right of where the full mana bar ends (x=198). It floats in space next to the HUD backing rather than on the bar.

**Fix:** Change to `(48 + 150 - 4, 45)` to anchor the dot at the right end of the bar.

---

### BUG-13 · MutantLairBackground cloud blobs may render incorrectly on non-alpha sky
**File:** `web/backgrounds.py:756–759`  
**Severity:** MINOR  

```python
surf = pygame.Surface((self.w, SCREEN_HEIGHT))   # no SRCALPHA
…
for r, a in [(cr, 40), (cr-10, 60), (cr-20, 90)]:
    cloud = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
    pygame.draw.circle(cloud, (*col, a), (r, r), r)
    surf.blit(cloud, (cx - r, cy - r))           # blit alpha-cloud → non-alpha surf
```

Blitting a per-pixel-alpha (SRCALPHA) surface onto a non-alpha surface does composite correctly **before** the `.convert()` call in `_BaseBackground.__init__`. However, `.convert()` converts to display format and **strips per-pixel alpha** from the already-composited result — meaning the clouds are composited correctly but any subsequent alpha assumptions are gone. This is generally fine, but it means cloud edges are rendered at lower quality than intended, with harsher edges because the intermediate blends are quantized to the display format.

**Fix:** Build the entire biome surface as SRCALPHA, composite everything, then convert at the end.

---

### BUG-14 · Boss HP bar and state label can clip off-screen
**File:** `web/game.py:1095–1128`  
**Severity:** MINOR  

```python
bx = boss.rect.centerx + cam_x - bar_w // 2
by = boss.rect.top + cam_y - 16
# "BOSS" label at (bx, by - 14)
# State label at (boss.rect.centerx + cam_x, by - 30 + bob)
```

If the boss is near the top of the viewport (e.g., jumping), `by` can be negative or `by - 30` strongly negative — the "!!! ATTACK !!!" label goes off the top edge and becomes invisible. If the boss is near the left edge, `bx` can be negative and the entire HP bar + label are partially or fully off-screen.

**Fix:** Clamp `bx = max(2, min(bx, SCREEN_WIDTH - bar_w - 2))` and `by = max(30, by)`.

---

### BUG-15 · All NPC "?" bubbles bob in identical phase
**File:** `web/game.py:1031–1046`  
**Severity:** MINOR  

```python
t_ms = pygame.time.get_ticks()
bounce = math.sin(t_ms / 200.0) * 5
for npc in self.level.npcs:
    sy = npc.rect.top + cam_y - 26 + bounce  # same bounce for all
```

All NPCs share `bounce`, so their "?" indicators bob up and down in perfect lockstep. For levels with multiple NPCs this looks mechanical. Should use a per-NPC phase offset (e.g., `npc.rect.x * 0.01`).

---

## TINY

---

### BUG-16 · `import random` inside draw methods (style + minor perf)
**File:** `web/game.py:1211, 1309`  
**Severity:** TINY  

```python
def _draw_dash_trail(self, cam_x, cam_y):
    …
    import random as _r   # line 1211
    
def _draw_sword_arc(self, cam_x, cam_y):
    …
    import random as _r   # line 1309
```

Python caches imports after the first call, so no correctness bug, but the `import` statement is called every frame at 60 FPS inside hot draw paths. Move both to the module top-level.

---

### BUG-17 · `ParallaxBackground` class in engine.py is completely unused
**File:** `web/engine.py:213–363`  
**Severity:** TINY  

The game uses `BiomeBackground` from `backgrounds.py`. `ParallaxBackground` in `engine.py` (150 lines, separate `_build_sky()`, `_build_combined()`) is dead code — never imported or instantiated by `game.py`. Creates maintenance confusion about which background system is active.

**Fix:** Delete `ParallaxBackground` from `engine.py`.

---

### BUG-18 · LevelTransition screen is solid black before text fades in (jarring cut)
**File:** `web/ui.py:843`  
**Severity:** TINY  

```python
screen.fill(COL_BLACK)
t = self.timer / self.duration
alpha = int(255 * (1 - abs(t - 0.5) * 2))  # 0 at t=0
text.set_alpha(alpha)
```

On the very first frame of a level transition the screen fills black and the text alpha is 0, resulting in a pure black frame before the fade-in starts. Because `_draw()` draws nothing else during `ST_LEVEL_TRANS`, this creates a single-frame hard black flash every time a level ends.

**Fix:** Set a minimum alpha of ~20 or delay `screen.fill` until alpha > 10.

---

### BUG-19 · Debug mode new-frame font allocations (no cache) 
**File:** `web/game.py:1044, 1106, 1122, 1397, 1472`  
**Severity:** TINY  

Multiple draw helpers call `pygame.font.SysFont("consolas", …)` **every frame** rather than using the `get_font()` cache from `ui.py`. Examples: NPC "?" bubble (line 1044), boss HP label (line 1106), boss state label (line 1122), NPC dialog name (line 1397), debug overlay (line 1472). Each `SysFont` call can trigger a font lookup. In debug mode or cave level (dark overlay + crystals), these stack up.

**Fix:** Replace inline `pygame.font.SysFont(…)` calls with `get_font(size, bold)` throughout `game.py`.

---

### BUG-20 · Victory screen's pulsing "NEW HIGH SCORE!" alpha is gated on score check, not on screen entry
**File:** `web/ui.py:817–823`  
**Severity:** TINY  

```python
if is_high_score:
    alpha = int(128 + 127 * math.sin(self.timer * 5))
    surf = font.render("NEW HIGH SCORE!", True, COL_GOLD)
    surf.set_alpha(alpha)
```

`set_alpha()` sets the **whole-surface** uniform alpha. But the font render already includes antialiased pixel alphas. Combining `set_alpha()` with antialiased renders creates a double-alpha effect: semi-transparent edge pixels get double-dimmed. Use `SRCALPHA` render + per-pixel blit instead for smooth results.

---

## Summary Table

| ID | File | Line(s) | Severity | Category |
|----|------|---------|----------|----------|
| BUG-01 | ui.py | 722 | CRITICAL | Layout overflow |
| BUG-02 | ui.py | 562–593 | CRITICAL | Layout overflow |
| BUG-03 | sprites.py | 1064, 1078, 1113 | MAJOR | Sprite misalignment |
| BUG-04 | backgrounds.py | 567–569 | MAJOR | Alpha ignored |
| BUG-05 | backgrounds.py | 903–904 | MAJOR | Alpha ignored |
| BUG-06 | ui.py | 205–223 | MAJOR | HUD overflow |
| BUG-07 | game.py | 1062–1074 | MAJOR | Dead code / perf |
| BUG-08 | sprites.py | 38–83 | MINOR | Animation fidelity |
| BUG-09 | sprites.py | 87–116 | MINOR | Sprite clipping |
| BUG-10 | sprites.py | 448 | MINOR | Sprite clipping |
| BUG-11 | sprites.py | 152–196 | MINOR | Visual inconsistency |
| BUG-12 | ui.py | 165–170 | MINOR | HUD element misplaced |
| BUG-13 | backgrounds.py | 756–759 | MINOR | Composite quality |
| BUG-14 | game.py | 1095–1128 | MINOR | UI clipping |
| BUG-15 | game.py | 1031–1046 | MINOR | Animation |
| BUG-16 | game.py | 1211, 1309 | TINY | Style/perf |
| BUG-17 | engine.py | 213–363 | TINY | Dead code |
| BUG-18 | ui.py | 843 | TINY | Visual flash |
| BUG-19 | game.py | 1044+ | TINY | Perf |
| BUG-20 | ui.py | 817–823 | TINY | Render quality |

---

*Report generated by Claude Rendering & Visual Glitch Hunter agent — BambooForest web build.*
