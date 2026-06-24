"""Headless unit tests for BambooForest player logic.

These tests exercise Player state machines, jump/coyote mechanics,
timers, powerup pickups, and core logic without requiring a display.

Run:
    cd BambooForest
    $env:SDL_VIDEODRIVER="dummy"
    python -m pytest tests/test_player.py -v
    # or
    python -m unittest discover -s tests -v
"""
from __future__ import annotations

import os
import sys
import unittest

# Force headless before any pygame import in this process
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402

# Ensure pygame submodules are registered (mirrors web/main.py safety)
import pygame.sprite  # noqa: F401,E402
import pygame.mixer   # noqa: F401,E402
import pygame.font    # noqa: F401,E402
import pygame.transform  # noqa: F401,E402
import pygame.draw    # noqa: F401,E402
import pygame.image   # noqa: F401,E402
import pygame.event   # noqa: F401,E402
import pygame.time    # noqa: F401,E402

# Add parent to path for package imports when running directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (  # noqa: E402
    FLOOR_Y,
    PLAYER_MAX_HP,
    PLAYER_JUMP,
    PLAYER_DAMAGE,
    GLIDE_DURATION_SEC,
    DASH_DURATION_SEC,
    COMBO_WINDOW,
    COMBO_MULTIPLIERS,
    BAMBOO_SCORE,
)
from sprites import Player  # noqa: E402


def make_player() -> Player:
    """Factory for a fresh player at floor level."""
    return Player(100, FLOOR_Y)


class TestPlayerBasics(unittest.TestCase):
    """Basic construction and initial state."""

    def test_constructs(self) -> None:
        p = make_player()
        self.assertIsNotNone(p)
        self.assertEqual(p.health, PLAYER_MAX_HP)
        self.assertEqual(p.score, 0)
        self.assertFalse(p.dead)
        self.assertFalse(p.is_on_ground)

    def test_initial_jump_state(self) -> None:
        p = make_player()
        self.assertEqual(p.jumps_remaining, 1)
        self.assertFalse(p.has_double_jump)
        self.assertEqual(p.coyote_timer, 0.0)


class TestJumpAndCoyote(unittest.TestCase):
    """Jump, double-jump, coyote time, and jump buffer."""

    def test_ground_jump_consumes_jump(self) -> None:
        p = make_player()
        p.is_on_ground = True
        p.jumps_remaining = 1
        ok = p.jump()
        self.assertTrue(ok)
        self.assertEqual(p.jumps_remaining, 0)
        self.assertEqual(p.velocity_y, PLAYER_JUMP)
        self.assertFalse(p.is_on_ground)

    def test_air_jump_without_double_fails(self) -> None:
        p = make_player()
        p.is_on_ground = True
        p.jump()
        p.is_on_ground = False
        ok = p.jump()
        self.assertFalse(ok)
        self.assertEqual(p.jumps_remaining, 0)

    def test_double_jump_enabled(self) -> None:
        p = make_player()
        p.has_double_jump = True
        p.is_on_ground = True
        p.jumps_remaining = 2
        p.jump()  # ground
        p.is_on_ground = False
        ok = p.jump()  # air
        self.assertTrue(ok)
        self.assertEqual(p.jumps_remaining, 0)

    def test_coyote_restores_ground_jump(self) -> None:
        p = make_player()
        # Simulate leaving ground; coyote window is normally set by collision code
        p.is_on_ground = False
        p.jumps_remaining = 0
        p.coyote_timer = 0.12
        # Also simulate a buffered early press so the restore path triggers
        p._jump_buffered = True
        p._jump_buffer_time = 0.1
        ok = p.jump()
        self.assertTrue(ok)
        self.assertEqual(p.jumps_remaining, 0)  # consumed immediately
        self.assertEqual(p.velocity_y, PLAYER_JUMP)
        self.assertEqual(p.coyote_timer, 0.0)
        self.assertFalse(getattr(p, "_jump_buffered", False))

    def test_jump_buffer_window(self) -> None:
        p = make_player()
        p.is_on_ground = True
        p.jumps_remaining = 1
        # Press slightly early while still on ground; buffer should be set
        # We can't easily call update without keys, so directly exercise the flag
        p._jump_buffered = True
        p._jump_buffer_time = 0.05
        # Jump should consume the buffer and fire
        ok = p.jump()
        self.assertTrue(ok)
        self.assertFalse(p._jump_buffered)


class TestDamageAndDeath(unittest.TestCase):
    """take_damage, i-frames, knockback, death."""

    def test_take_damage_reduces_health_and_sets_iframes(self) -> None:
        p = make_player()
        start = p.health
        ok = p.take_damage(PLAYER_DAMAGE)
        self.assertTrue(ok)
        self.assertEqual(p.health, start - PLAYER_DAMAGE)
        self.assertGreater(p.invincible_timer, 0)
        self.assertGreater(p.knockback_timer, 0)
        self.assertTrue(p.input_locked)

    def test_damage_during_iframes_is_ignored(self) -> None:
        p = make_player()
        p.invincible_timer = 0.5
        start = p.health
        ok = p.take_damage(PLAYER_DAMAGE)
        self.assertFalse(ok)
        self.assertEqual(p.health, start)

    def test_death_sets_dead_flag(self) -> None:
        p = make_player()
        p.health = 10
        p.take_damage(100)
        self.assertEqual(p.health, 0)
        self.assertTrue(p.dead)


class TestTimers(unittest.TestCase):
    """Combo, glide, dash, weapon timers."""

    def test_combo_window_resets(self) -> None:
        p = make_player()
        p.combo_count = 2
        p.combo_timer = 0.01
        p.update(0.1, pygame.key.get_pressed(), pygame.sprite.Group())
        self.assertEqual(p.combo_count, 0)
        self.assertEqual(p.combo_timer, 0.0)

    def test_glide_timer_counts_only_while_gliding(self) -> None:
        p = make_player()
        p.glide_time_remaining = GLIDE_DURATION_SEC
        p.is_gliding = True
        p.update(1.0, pygame.key.get_pressed(), pygame.sprite.Group())
        self.assertLess(p.glide_time_remaining, GLIDE_DURATION_SEC)
        # When not gliding, timer should not tick
        p.is_gliding = False
        before = p.glide_time_remaining
        p.update(1.0, pygame.key.get_pressed(), pygame.sprite.Group())
        self.assertEqual(p.glide_time_remaining, before)

    def test_glide_auto_clears_when_timer_expires(self) -> None:
        p = make_player()
        p.glide_time_remaining = 0.01
        p.is_gliding = True
        p.update(0.1, pygame.key.get_pressed(), pygame.sprite.Group())
        self.assertEqual(p.glide_time_remaining, 0.0)
        self.assertFalse(p.is_gliding)

    def test_dash_timer_counts_down(self) -> None:
        p = make_player()
        p.dash_time_remaining = DASH_DURATION_SEC
        p.update(1.0, pygame.key.get_pressed(), pygame.sprite.Group())
        self.assertLess(p.dash_time_remaining, DASH_DURATION_SEC)

    def test_weapon_timer_disarms(self) -> None:
        p = make_player()
        p.has_bamboo_weapon = True
        p.weapon_time_remaining = 0.01
        p.update(0.1, pygame.key.get_pressed(), pygame.sprite.Group())
        self.assertFalse(p.has_bamboo_weapon)
        self.assertEqual(p.weapon_time_remaining, 0.0)


class TestPowerupPickups(unittest.TestCase):
    """Dash availability, glide enable, weapon enable (logic only)."""

    def test_dash_requires_time_remaining(self) -> None:
        p = make_player()
        p.dash_time_remaining = 0.0
        self.assertFalse(p.dash())

    def test_dash_starts_and_consumes_availability(self) -> None:
        p = make_player()
        p.dash_time_remaining = 10.0
        ok = p.dash()
        self.assertTrue(ok)
        self.assertTrue(p.is_dashing)
        self.assertTrue(p.input_locked)
        self.assertGreater(p.dash_timer, 0)
        self.assertGreater(p.dash_cooldown, 0)

    def test_set_gliding_requires_conditions(self) -> None:
        p = make_player()
        p.glide_time_remaining = 5.0
        p.is_on_ground = False
        p.velocity_y = 100
        p.set_gliding(True)
        self.assertTrue(p.is_gliding)

        # On ground -> no glide
        p.is_on_ground = True
        p.set_gliding(True)
        self.assertFalse(p.is_gliding)

    def test_collect_bamboo_increments_combo_and_score(self) -> None:
        p = make_player()
        pts1 = p.collect_bamboo()
        self.assertEqual(pts1, BAMBOO_SCORE * COMBO_MULTIPLIERS[0])
        self.assertEqual(p.combo_count, 1)
        self.assertGreater(p.combo_timer, 0)

        pts2 = p.collect_bamboo()
        self.assertEqual(pts2, BAMBOO_SCORE * COMBO_MULTIPLIERS[1])
        self.assertEqual(p.combo_count, 2)


class TestResetState(unittest.TestCase):
    """reset_state clears transient locks and pending actions."""

    def test_resets_all_flags(self) -> None:
        p = make_player()
        p.input_locked = True
        p.is_attacking = True
        p.is_dashing = True
        p.is_slamming = True
        p.is_gliding = True
        p.pending_throws = [(0, 0, 1)]
        p.pending_ice_casts = [(0, 0, 1)]
        p._jump_buffered = True
        p.reset_state()
        self.assertFalse(p.input_locked)
        self.assertFalse(p.is_attacking)
        self.assertFalse(p.is_dashing)
        self.assertFalse(p.is_slamming)
        self.assertFalse(p.is_gliding)
        self.assertEqual(p.pending_throws, [])
        self.assertEqual(p.pending_ice_casts, [])
        self.assertFalse(p._jump_buffered)

    def test_preserves_permanent_unlocks(self) -> None:
        p = make_player()
        p.has_ice_magic = True
        p.has_double_jump = True
        p.reset_state()
        self.assertTrue(p.has_ice_magic)
        self.assertTrue(p.has_double_jump)


class TestHealAndAttack(unittest.TestCase):
    """heal and attack rect / cooldowns."""

    def test_heal_caps_at_max(self) -> None:
        p = make_player()
        p.health = PLAYER_MAX_HP - 5
        p.heal(100)
        self.assertEqual(p.health, PLAYER_MAX_HP)

    def test_attack_requires_weapon_and_not_on_cooldown(self) -> None:
        p = make_player()
        self.assertFalse(p.attack())
        p.has_bamboo_weapon = True
        self.assertTrue(p.attack())
        self.assertTrue(p.is_attacking)
        self.assertGreater(p.attack_timer, 0)
        self.assertGreater(p.attack_cooldown, 0)
        # While attacking, cannot start another
        self.assertFalse(p.attack())


if __name__ == "__main__":
    unittest.main(verbosity=2)
