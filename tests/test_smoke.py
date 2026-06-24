"""Headless smoke harness for BambooForest.

Purpose:
- Verify the game can at least be imported and core objects constructed.
- Provide a pattern for short, timed headless runs (physics ticks only).
- Do NOT require a real display or audio device.

How to run (PowerShell):
    cd BambooForest
    $env:SDL_VIDEODRIVER="dummy"
    python -m unittest discover -s tests -v

How to run a quick manual smoke (no pytest):
    cd BambooForest
    $env:SDL_VIDEODRIVER="dummy"
    python -c "import tests.test_smoke as s; s.smoke_run_frames(30)"

If importing the full 'game' module fails (SyntaxError or ImportError),
that is a hard blocker -- the entry point is broken before any runtime.
"""
from __future__ import annotations

import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()


class TestImportSmoke(unittest.TestCase):
    """Ensure the main game package can be imported without crashing."""

    def test_import_game_module(self) -> None:
        # This will raise on SyntaxError or missing deps at import time.
        # If this fails, the desktop and web builds are both un-runnable.
        import game  # noqa: F401

    def test_import_sprites_and_levels(self) -> None:
        from sprites import Player  # noqa: F401
        from levels import build_level_state  # noqa: F401
        ls = build_level_state(0)
        self.assertGreater(len(ls.platforms), 0)


def smoke_run_frames(n: int = 30, level: int = 0) -> None:
    """Run N physics frames headless with a real LevelState + Player.

    This is the safe pattern for 'does it explode in the first second?' checks.
    No rendering, no event loop, no audio.
    """
    from sprites import Player
    from levels import build_level_state
    from config import FLOOR_Y

    ls = build_level_state(level)
    p = Player(100, FLOOR_Y)
    ls.all_sprites.add(p)
    dt = 1.0 / 60.0
    for _ in range(n):
        keys = pygame.key.get_pressed()
        p.update(dt, keys, ls.platforms)
        # Also tick simple groups that have .update(dt) and no side effects
        ls.bamboos.update(dt)
        ls.heals.update(dt)
    print(f"[smoke] {n} frames on level {level} OK; "
          f"pos=({p.rect.x:.0f},{p.rect.y:.0f}) vy={p.velocity_y:.1f} "
          f"ground={p.is_on_ground}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
