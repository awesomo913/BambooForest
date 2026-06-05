# BambooForest — Web Build Parity & WASM Bug Report
**Generated:** 2026-06-05  
**Scope:** `web/*.py` vs root `*.py`, CI pipeline, touch overlay, site embedding  
**Method:** Full read + `git diff --no-index` on all file pairs  

---

## Summary

| Severity | Count | Area |
|---|---|---|
| 🔴 CRITICAL | 1 | `web/save.py` — scores never persist in browser |
| 🟠 HIGH | 2 | CI `pip` violation; favicon.png fragile step |
| 🟡 MEDIUM | 8 | Content divergences (web vs root out of sync) |
| 🟢 LOW | 3 | Touch/UI concerns, informational |

**Files with no divergence (safe):** `web/engine.py`, `web/backgrounds.py`, `web/ui.py`, `web/audio.py`, `web/config.py`, `web/main.py`

---

## 🔴 CRITICAL

### BUG-01 — High Scores Never Persist in Browser
**File:** `web/save.py` (identical to root `save.py`)  
**Impact:** Every player's score is lost on page refresh. No persistence at all.

**What it does:**
```python
with open(SAVE_FILE, "w") as f:
    json.dump({"high_scores": scores}, f, indent=2)
```

**Why it silently fails:** Pyodide (the WebAssembly Python runtime) provides a virtual in-memory filesystem. File writes succeed at the Python level — no exception is thrown — but the data lives only in RAM. When the page reloads, the filesystem is reset and all data is gone. The existing `except OSError: return False` only catches explicit OS errors, not the silent memory-only write.

**Fix needed:** Detect the WASM environment at startup and use `localStorage` instead:
```python
import sys
_IS_WASM = sys.platform == "emscripten"

if _IS_WASM:
    # Use window.localStorage via JavaScript bridge
    from js import localStorage  # available in Pyodide
    def save_high_score(score, level_reached):
        ...
        localStorage.setItem("bamboo_scores", json.dumps(data))
    def load_high_scores():
        raw = localStorage.getItem("bamboo_scores")
        if raw: return json.loads(raw)
        ...
else:
    # existing open() path for desktop
```

---

## 🟠 HIGH

### BUG-02 — CI Uses `pip install` (Workspace HOT Rule Violation)
**File:** `.github/workflows/deploy.yml`  
**Line:** `pip install pygbag==0.9.3`

The workspace HOT rule requires `uv pip install` everywhere — never bare `pip`. GitHub Actions uses a fresh runner, so it works either way today, but this violates the workspace convention and would fail if a `pip`-blocking hook were ever added.

**Fix:** Replace with `uv pip install pygbag==0.9.3` (and add `pip install uv` or the UV installer step before it).

---

### BUG-03 — favicon.png Copy Step Can Silently Break CI
**File:** `.github/workflows/deploy.yml`  
**Step:** `cp web/build/web/favicon.png deploy/game/`

Pygbag 0.9.3's build output structure isn't guaranteed to include `favicon.png` at that exact path. If pygbag changes the output layout or the file isn't emitted, this step either fails hard (breaking the deploy) or copies nothing (serving a broken favicon). There's no `|| true` fallback and no existence check.

**Fix:**
```yaml
- name: Copy favicon (optional)
  run: cp web/build/web/favicon.png deploy/game/ 2>/dev/null || echo "No favicon.png emitted by pygbag — skipping"
```

---

## 🟡 MEDIUM — Content Divergences (web vs root out of sync)

These don't crash the web build, but they mean desktop players and web players are playing different games. Sync should go in one direction.

---

### BUG-04 — Pickup Text Names Inconsistent (Forest Theme vs Action Names)
**Files:** `web/game.py` vs `game.py` (root)

| Element | Web | Root |
|---|---|---|
| Glide pickup toast | `"BAMBOO LEAF! {sec}s"` | `"GLIDE! {sec}s"` |
| Dash pickup toast | `"BAMBOO WIND! {sec}s"` | `"DASH! {sec}s"` |
| Glide hint title | `"BAMBOO LEAF!"` | `"GLIDE UNLOCKED!"` |

Web uses a forest-themed naming scheme; root uses action-verb naming. Pick one and apply it everywhere.

---

### BUG-05 — Glide/Dash Pickup Positions Stripped from Root Levels (GAMEPLAY BREAK)
**Files:** `web/levels.py` vs `levels.py` (root)  
**Impact:** Desktop players almost never encounter glide pickups. The glide mechanic is effectively non-functional on desktop.

Root has removed `glide_positions` from **levels 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18**. Root also removed `dash_positions` from levels 4, 6, 7, 8, 9, 10, 11, 14, 16, 17, 18.

Example:
- Level 1: Web has both `glide_positions` and `dash_positions`. Root has only `dash_positions`.
- Level 14: Web has `glide_positions=[(2600, FLOOR_Y), (5400, 300)]`. Root has only `[(5200, FLOOR_Y)]`.

**Fix:** Decide which layout is canonical (web is richer) and backport the positions to root.

---

### BUG-06 — Glide/Dash Animation States Missing from Root Sprites
**Files:** `web/sprites.py` vs `sprites.py` (root)

Web generates explicit `"glide"` and `"dash"` animation frames for the player sprite. Root does not generate these frames, so `anim_state = "dash"` and `anim_state = "glide"` fall back to `"run"` and `"fall"` respectively.

Additionally, the glide **trigger threshold** differs:
- Web: `velocity_y > 10` — glide pose appears very responsively on any downward movement
- Root: `velocity_y > 80` — glide pose almost never triggers (requires very fast falling)

**Impact:** On desktop, the player never visually enters glide mode even when holding the glide pickup.

---

### BUG-07 — Power-Up Item Art Completely Diverged
**Files:** `web/sprites.py` vs `sprites.py` (root)

| Sprite | Web | Root |
|---|---|---|
| DashBoots visual | Bamboo scroll with wind swirls | Winged boots with speed streaks |
| DashBoots halo color | Green `(120, 210, 100)` | Orange `(255, 160, 80)` |
| GlideFeather visual | Bamboo leaf shape | Cyan/white feather with shaft |

Both are valid art styles, but they produce different-looking items. Web = forest-themed; root = fantasy-action.

---

### BUG-08 — Darkness Mechanic Visual Older in Web
**Files:** `web/game.py` vs `game.py` (root)

Root has a polished crystal-fade darkness system using `CRYSTAL_LIGHT_TIME` with smooth radius falloff (more atmospheric). Web has the older simpler darkness overlay.

Additionally, root does NOT have these two visual helper methods that exist in web:
- `_draw_glide_leaf()` — draws the glide effect
- `_draw_dash_trail()` — draws the dash speed trail

This means on desktop the player has no visual feedback for glide/dash, but the web build does.

---

### BUG-09 — DustDevil Sprite Completely Redesigned in Root (Content Drift)
**File:** `biomes.py` (root) vs `web/biomes.py`

| Property | Web | Root |
|---|---|---|
| Size | 44×72 | 64×110 |
| Frames | 4 | 6 |
| Shape | Wider base, narrower top | Wide top, narrow at ground (real dust-devil) |
| Debris streaks | 4 diagonal lines | 6 diagonal + 15 flying sand particles |
| Has "cloud cap"? | No | Yes (dark ellipse at top) |

The root version is visually richer. Web players see the older, smaller sprite.

---

### BUG-10 — DarkWall Completely Redesigned in Root (Content Drift)
**File:** `biomes.py` (root) vs `web/biomes.py`

| Property | Web | Root |
|---|---|---|
| Animation | Static (1 surface) | 4-frame animated barrier |
| Visual style | Eldritch void wall with glowing eyes, cracks, corruption dots | Magical barrier with runic sigils, energy flow packets, climbing particles |
| Faded state | `self._faded` (single alpha-set surface) | `self._faded_frames` (4 alpha-set frames, still animated when transparent) |

Each version is internally consistent. But they look completely different. The root version is more readable and animated.

**Note for WASM:** No compatibility risk here — both implementations work correctly in their respective builds. The web version's static wall is fine for WASM.

---

## 🟢 LOW / Informational

### INFO-01 — No GLIDE Button in Touch Overlay (Intentional — Confirmed OK)
**File:** `web/touch_overlay.html`

Touch overlay has: joystick (left/right), A (attack = E), B (jump = Space), DASH (Shift), START (Enter). No GLIDE button.

Glide is passive — it activates automatically when `velocity_y > 10` (web threshold) during a fall after picking up the glide leaf. No button needed. This is correct.

---

### INFO-02 — Game iframe Has No `touch-action: none` in Site Shell
**File:** `site/index.html` / `site/styles.css`

The touch controls inside the game set `touch-action: none` on their own elements. But the `<iframe>` container in `site/index.html` doesn't have `touch-action: none` on its shell element. On some mobile browsers, scroll and pinch-to-zoom gestures on the outer page can leak into the iframe during gameplay, especially when starting a touch near the edge of the iframe.

**Low-risk fix:**
```css
.game-embed-shell {
  touch-action: none;
}
```

---

### INFO-03 — pygame Submodule Imports Correctly Present in web/ Files Only
**Files:** `web/biomes.py`, `web/sprites.py`, `web/levels.py`

All web-specific files include explicit submodule imports at the top:
```python
import pygame.sprite   # noqa: F401
import pygame.transform  # noqa: F401
import pygame.draw     # noqa: F401
```

These are correctly NOT in root files (desktop CPython auto-registers them). They exist in web files because Pyodide's lazy submodule registration doesn't always fire `pygame.__getattr__` in WASM. This is correct behavior — not a bug.

---

## Files Confirmed Identical (web = root, no bugs)

| File pair | Lines | Status |
|---|---|---|
| `web/engine.py` / `engine.py` | 363 | ✅ Identical |
| `web/backgrounds.py` / `backgrounds.py` | 941 | ✅ Identical |
| `web/ui.py` / `ui.py` | 876 | ✅ Identical |
| `web/audio.py` | 241 | ✅ WASM-safe (procedural, no files, robust fallback) |
| `web/config.py` | — | ✅ Correct (no PyInstaller frozen logic) |
| `web/main.py` | 26 | ✅ Correct (explicit submodule imports + asyncio.run) |

---

## Recommended Fix Priority

1. **BUG-01** — localStorage save system (players currently lose all progress in browser)
2. **BUG-05** — Backport glide/dash positions to root levels (desktop gameplay is broken)
3. **BUG-06** — Sync glide animation frames + threshold to root sprites
4. **BUG-08** — Port `_draw_glide_leaf()` and `_draw_dash_trail()` to root
5. **BUG-02** — Fix `pip install` → `uv pip install` in CI
6. **BUG-03** — Make favicon copy step non-fatal in CI
7. **BUG-04** — Pick one naming convention (forest-theme or action-verb) and unify
8. **BUG-07 / BUG-09 / BUG-10** — Decide on canonical art and backport
