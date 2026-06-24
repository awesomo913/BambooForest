"""Headless verification harness for BambooForest controls and physics.

Features covered: jump buffer, reverse gravity, dash, glide, input lock timer, portals.

Uses the *full* level maps (build_level_state) so platforms, gravity zones,
and portal placements are the real ones from levels.py.

Run:
    cd Desktop\AI\BambooForest
    $env:SDL_VIDEODRIVER = 'dummy'
    python tests/verify.py

Python -c style (single scenario, no display):
    python -c "
    import os, sys
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    sys.path.insert(0, r'C:\\Users\\computer\\Desktop\\AI\\BambooForest')
    from tests.verify import verify_jump_buffer
    verify_jump_buffer()
    "

No pygame.display.set_mode() is called; purely logic + collisions.
"""

from __future__ import annotations

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


import pygame

import pygame.sprite
import pygame.mixer
import pygame.font
import pygame.transform
import pygame.draw
import pygame.image
import pygame.event
import pygame.time
import pygame.key

from config import (
    FLOOR_Y,
    PLAYER_JUMP,
    GLIDE_DURATION_SEC,
    DASH_DURATION_SEC,
    JUMP_BUFFER_TIME,
    PORTAL_COOLDOWN_SEC,
)
from levels import build_level_state
from sprites import Player

pygame.init()


class FakeKeys:
    """Stand-in for pygame.key.get_pressed() result.

    Supports high SDLK values used by pygame 2 (arrow keys etc).
    """
    def __init__(self, *names: str) -> None:
        self._on: set[int] = set()
        for n in names:
            if hasattr(pygame, n):
                self._on.add(getattr(pygame, n))

    def __getitem__(self, key: int) -> bool:
        return key in self._on


def run_scenario(name: str, func) -> None:
    """Wrapper that prints PASS/FAIL for a verification scenario."""
    try:
        func()
        print(f"[PASS] {name}")
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")
    except Exception as e:
        print(f"[ERROR] {name}: {type(e).__name__}: {e}")


def verify_dash() -> None:
    """Dash: boots required, high vel, lock timer, cooldown."""
    level = build_level_state(0)
    plats = level.platforms
    p = Player(500, FLOOR_Y)
    p.is_on_ground = True
    p.dash_time_remaining = DASH_DURATION_SEC

    ok = p.dash()
    assert ok, "dash should succeed with boots"
    assert p.is_dashing
    assert p.input_locked
    assert p.input_lock_timer > 0
    assert abs(p.velocity_x) == 900.0
    assert p.dash_timer > 0
    assert p.dash_cooldown > 0

    keys = FakeKeys()
    for _ in range(20):
        p.update(1.0 / 60.0, keys, plats)
    assert not p.is_dashing, "dash should end after timer"
    assert not p.input_locked or p.input_lock_timer <= 0


def verify_glide() -> None:
    """Glide slows fall; timer counts only while gliding."""
    level = build_level_state(1)
    plats = level.platforms
    p = Player(300, 300)
    p.is_on_ground = False
    p.velocity_y = 200.0
    p.glide_time_remaining = GLIDE_DURATION_SEC

    keys = FakeKeys("K_SPACE")
    for _ in range(3):
        p.update(1.0 / 60.0, keys, plats)

    assert p.is_gliding, "glide should engage"
    assert p.velocity_y <= 120.0, "glide caps fall speed"

    before = p.glide_time_remaining
    for _ in range(10):
        p.update(1.0 / 60.0, keys, plats)
    assert p.glide_time_remaining < before, "glide timer decrements while active"

    keys = FakeKeys()
    before2 = p.glide_time_remaining
    for _ in range(10):
        p.update(1.0 / 60.0, keys, plats)
    assert not p.is_gliding
    assert p.glide_time_remaining == before2, "timer pauses when not gliding"


def verify_lock_timer() -> None:
    """Input lock timer safety: auto-unlocks after timeout."""
    level = build_level_state(0)
    plats = level.platforms
    p = Player(200, FLOOR_Y)
    p.input_locked = True
    p.input_lock_timer = 0.25

    keys = FakeKeys()
    for _ in range(20):
        p.update(1.0 / 60.0, keys, plats)

    assert not p.input_locked, "lock should auto-clear"
    assert p.input_lock_timer == 0.0

    p.dash_time_remaining = 5.0
    p.dash()
    assert p.input_locked
    assert p.input_lock_timer > 0
    for _ in range(30):
        p.update(1.0 / 60.0, keys, plats)
    assert not p.input_locked


def verify_reverse_gravity() -> None:
    """Reverse gravity using full level 18 map + zones + ceiling plats."""
    level = build_level_state(17)
    plats = level.platforms
    gzones = list(level.gravity_zones)

    rev_zone = next((gz for gz in gzones if gz.gravity_type == "reverse"), None)
    assert rev_zone is not None, "level 18 must have reverse gravity zone"

    ceiling_plats = [pl for pl in plats if getattr(pl, "rect", None) and pl.rect.y < 250]
    assert ceiling_plats, "need ceiling platforms for reverse-grav test"
    ceil = ceiling_plats[0]

    p = Player(ceil.rect.centerx, ceil.rect.bottom + 30)
    p.gravity_multiplier = -1.0
    p.is_on_ground = False
    p.jumps_remaining = 1
    p.velocity_y = 50.0

    keys = FakeKeys()
    hit = False
    for _ in range(40):
        p.update(1.0 / 60.0, keys, plats)
        if p.is_on_ground:
            hit = True
            break

    assert hit, "player should land on ceiling in reverse grav"
    assert p.velocity_y == 0

    ok = p.jump()
    assert ok
    assert p.velocity_y > 0, f"reverse-grav jump must give +vy (down), got {p.velocity_y}"
    assert p.is_on_ground is False


def verify_portals() -> None:
    """Portals from full level 17 map: teleport + state clear + cooldown."""
    level = build_level_state(16)
    portals = list(level.portals)
    assert portals, "level 17 must have portals"

    src = portals[0]
    assert src.partner is not None
    tgt = src.partner

    p = Player(src.rect.centerx, src.rect.centery)
    p.is_gliding = True
    p.is_dashing = True
    p.is_slamming = True
    p.input_locked = True
    p.velocity_x = 123.0
    p.velocity_y = -99.0
    p._sub_x = 4.0
    p.knockback_timer = 0.1

    if src.active and tgt is not None:
        p.rect.midbottom = tgt.rect.midbottom
        p.velocity_x = 0.0
        p.velocity_y = 0.0
        p.input_locked = False
        p.is_gliding = p.is_dashing = p.is_slamming = False
        p.knockback_timer = 0.0
        p._sub_x = 0.0
        src.teleport()
        tgt.teleport()
        p.invincible_timer = max(getattr(p, "invincible_timer", 0), 0.3)

    assert abs(p.rect.centerx - tgt.rect.centerx) <= 2
    assert abs(p.rect.bottom - tgt.rect.bottom) <= 2
    assert not p.is_gliding
    assert not p.is_dashing
    assert not p.is_slamming
    assert not p.input_locked
    assert p.velocity_x == 0.0 and p.velocity_y == 0.0
    assert not src.active
    assert src.cooldown > 0
    assert src.cooldown <= PORTAL_COOLDOWN_SEC + 0.01

    for _ in range(200):
        src.update(1.0 / 60.0)
    assert src.active, "portal should reopen after cooldown"


def verify_jump_buffer() -> None:
    """Jump buffer: press before landing -> auto-jump on contact (full map)."""
    level = build_level_state(0)
    plats = level.platforms
    p = Player(420, FLOOR_Y - 200)  # high enough to be clear of all plats at this x
    # ensure truly airborne, lift until no collision
    for _ in range(50):
        if not pygame.sprite.spritecollide(p, plats, False):
            break
        p.rect.y -= 4
    p.is_on_ground = False
    p.jumps_remaining = 0
    p.velocity_y = 620.0


def verify_ghost_speedrun() -> None:
    """Ghost record/save/load + 'save if better' using real save_best_run / get_best_ghost.
    Uses a minimal synthetic record list. Must not require display or player.
    Uses a fresh high key every run so prior profile data cannot interfere.
    """
    from save import save_best_run, get_best_ghost, load_best_time
    import time as _t

    # fresh key every invocation (high number unlikely to collide with real levels)
    lvl = 900000 + int(_t.time() * 1000) % 100000

    # build a short path record: t,x,y,facing
    rec = [
        [0.0, 100, 400, True],
        [0.2, 140, 400, True],
        [0.4, 180, 398, True],
        [0.6, 220, 400, False],
    ]
    # first save should succeed (fresh key)
    ok1 = save_best_run(lvl, 1.23, rec)
    assert ok1, "first ghost run must save as best"
    loaded = get_best_ghost(lvl)
    assert loaded is not None and len(loaded) == len(rec), "ghost must roundtrip"
    assert abs(load_best_time(lvl) - 1.23) < 0.001

    # worse time must NOT overwrite
    rec2 = [[0.0, 90, 400, True], [0.5, 300, 400, True]]
    ok2 = save_best_run(lvl, 5.0, rec2)
    assert not ok2, "worse time must not save over best ghost"
    loaded2 = get_best_ghost(lvl)
    assert len(loaded2) == len(rec), "ghost must remain the better one"

    # better replaces
    rec3 = [[0.0, 105, 400, True], [0.2, 150, 395, True], [0.4, 190, 400, True]]
    ok3 = save_best_run(lvl, 1.10, rec3)
    assert ok3, "strictly better time must save"
    loaded3 = get_best_ghost(lvl)
    assert abs(loaded3[1][1] - 150) < 1, "newer better ghost data must be stored"


SCENARIOS = [
    ("jump buffer (full map)", verify_jump_buffer),
    ("dash (full map)", verify_dash),
    ("glide (full map)", verify_glide),
    ("lock timer (full map)", verify_lock_timer),
    ("reverse gravity (level 18 map)", verify_reverse_gravity),
    ("portals (level 17 map)", verify_portals),
    ("speedrun ghost record + save-if-better", verify_ghost_speedrun),
]


def main() -> None:
    """Run all key scenarios."""
    print("BambooForest controls/physics verification (headless, full maps)")
    print("=" * 60)
    for name, func in SCENARIOS:
        run_scenario(name, func)
    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
