"""Headless unit tests for core game logic."""

from __future__ import annotations

import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from config import (
    BAMBOO_SCORE,
    COMBO_MULTIPLIERS,
    FLOOR_Y,
    LEVEL_COUNT,
    PLAYER_DAMAGE,
    STARTING_LIVES,
    ST_GAME_OVER,
    ST_PAUSED,
    ST_PLAYING,
    ST_VICTORY,
    STOMP_SCORE,
    TRENCH_DEATH_Y,
)
from engine import Camera
from game import Game
from sprites import Bamboo, Checkpoint, Platform, Player


class FakeKeys:
    """Indexable key map for Player.update tests."""

    def __init__(self, pressed: set[int] | None = None) -> None:
        self.pressed = pressed or set()

    def __getitem__(self, key: int) -> bool:
        return key in self.pressed


NO_KEYS = FakeKeys()


class DummyEnemy(pygame.sprite.Sprite):
    """Minimal enemy sprite for collision tests."""

    def __init__(self, x: int, y: int, w: int = 30, h: int = 30) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alive_flag = True
        self.is_stompable = True

    def update(self, dt: float, platforms: pygame.sprite.Group, player: Player) -> None:
        return None

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class GameLogicTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def _make_stub_level(self) -> SimpleNamespace:
        return SimpleNamespace(
            world_width=2400,
            biome="forest",
            player_start=(100, FLOOR_Y),
            is_icy=False,
            all_sprites=pygame.sprite.Group(),
            bamboos=pygame.sprite.Group(),
            checkpoints=pygame.sprite.Group(),
        )

    def _make_minimal_gameplay_level(self) -> SimpleNamespace:
        return SimpleNamespace(
            world_width=2400,
            platforms=pygame.sprite.Group(),
            moving_platforms=pygame.sprite.Group(),
            enemies=pygame.sprite.Group(),
            boss=None,
            geysers=pygame.sprite.Group(),
            toxic_trails=pygame.sprite.Group(),
            crumbling=pygame.sprite.Group(),
            wind_zones=pygame.sprite.Group(),
            updrafts=pygame.sprite.Group(),
            projectiles=pygame.sprite.Group(),
            crystals=pygame.sprite.Group(),
            mushrooms=pygame.sprite.Group(),
            poison_spores=pygame.sprite.Group(),
            rising_lava=None,
            timed_gates=pygame.sprite.Group(),
            portals=pygame.sprite.Group(),
            gravity_zones=pygame.sprite.Group(),
            dark_walls=pygame.sprite.Group(),
            npcs=pygame.sprite.Group(),
            checkpoints=pygame.sprite.Group(),
            bamboos=pygame.sprite.Group(),
            weapons=pygame.sprite.Group(),
            glide_pickups=pygame.sprite.Group(),
            dash_pickups=pygame.sprite.Group(),
            heals=pygame.sprite.Group(),
            goal=None,
            all_sprites=pygame.sprite.Group(),
            decorations=pygame.sprite.Group(),
        )

    def _prepare_game_for_gameplay(self, level: SimpleNamespace, player: Player) -> Game:
        game = Game()
        game.level = level
        game.player = player
        game.camera = Camera(level.world_width, 540)
        game.hud = MagicMock()
        game.particles = MagicMock()
        game.shake = MagicMock()
        game.audio = MagicMock()
        game.death_anim = None
        game._outro_active = False
        game._boss_warning_timer = 0.0
        return game

    def test_player_lands_on_platform(self) -> None:
        player = Player(100, 120)
        platform = Platform(70, 140, 220, 20)
        player.rect.bottom = 130
        player.velocity_y = 300.0

        player.update(0.1, NO_KEYS, pygame.sprite.Group(platform))

        self.assertTrue(player.is_on_ground)
        self.assertEqual(player.rect.bottom, platform.rect.top)
        self.assertEqual(player.velocity_y, 0)

    def test_player_side_collision_blocks_movement(self) -> None:
        player = Player(80, FLOOR_Y)
        wall = Platform(120, 200, 40, 220)
        player.rect.right = 110
        player.rect.y = 250
        player.input_locked = True
        player.velocity_x = 400.0

        player.update(0.1, NO_KEYS, pygame.sprite.Group(wall))

        self.assertEqual(player.rect.right, wall.rect.left)
        self.assertEqual(player.velocity_x, 0)

    @patch("pygame.key.get_pressed", return_value=NO_KEYS)
    def test_collecting_bamboo_increases_score(self, _mock_keys: MagicMock) -> None:
        level = self._make_minimal_gameplay_level()
        player = Player(120, 220)
        player.update = MagicMock()  # type: ignore[method-assign]

        bamboo = Bamboo(player.rect.left, player.rect.bottom)
        bamboo.rect = bamboo.image.get_rect(topleft=player.rect.topleft)
        level.bamboos.add(bamboo)

        game = self._prepare_game_for_gameplay(level, player)
        game._update_gameplay(0.016)

        self.assertEqual(player.score, BAMBOO_SCORE * COMBO_MULTIPLIERS[0])
        self.assertEqual(len(level.bamboos), 0)

    @patch("pygame.key.get_pressed", return_value=NO_KEYS)
    def test_enemy_collision_deals_damage(self, _mock_keys: MagicMock) -> None:
        level = self._make_minimal_gameplay_level()
        player = Player(120, 220)
        player.update = MagicMock()  # type: ignore[method-assign]

        enemy = DummyEnemy(player.rect.x, player.rect.y)
        level.enemies.add(enemy)

        game = self._prepare_game_for_gameplay(level, player)
        start_hp = player.health
        game._update_gameplay(0.016)

        self.assertEqual(player.health, start_hp - PLAYER_DAMAGE)

    @patch("pygame.key.get_pressed", return_value=NO_KEYS)
    def test_stomping_enemy_awards_score(self, _mock_keys: MagicMock) -> None:
        level = self._make_minimal_gameplay_level()
        player = Player(200, 220)
        player.update = MagicMock()  # type: ignore[method-assign]
        player.velocity_y = 200.0

        enemy = DummyEnemy(player.rect.x + 2, player.rect.bottom - 8)
        level.enemies.add(enemy)

        game = self._prepare_game_for_gameplay(level, player)
        game._update_gameplay(0.016)

        self.assertEqual(player.score, STOMP_SCORE)
        self.assertFalse(enemy.alive_flag)

    @patch("pygame.key.get_pressed", return_value=NO_KEYS)
    def test_falling_below_trench_boundary_causes_death(self, _mock_keys: MagicMock) -> None:
        level = self._make_minimal_gameplay_level()
        player = Player(120, 220)
        player.update = MagicMock()  # type: ignore[method-assign]
        player.rect.top = TRENCH_DEATH_Y + 1

        game = self._prepare_game_for_gameplay(level, player)
        game._update_gameplay(0.016)

        self.assertTrue(player.dead)
        self.assertEqual(player.health, 0)
        self.assertTrue(player.is_falling_trench)

    @patch("game.build_level_state")
    def test_start_game_transitions_to_playing(self, mock_build_level: MagicMock) -> None:
        mock_build_level.return_value = self._make_stub_level()
        game = Game()

        game._start_game()

        self.assertEqual(game.state, ST_PLAYING)
        self.assertEqual(game.current_level, 0)
        self.assertEqual(game.lives, STARTING_LIVES)
        self.assertIsNotNone(game.player)

    def test_escape_pauses_and_resumes_play(self) -> None:
        game = Game()
        game.state = ST_PLAYING

        game._on_key_down(pygame.K_ESCAPE)
        self.assertEqual(game.state, ST_PAUSED)

        game._on_key_down(pygame.K_ESCAPE)
        self.assertEqual(game.state, ST_PLAYING)

    @patch("game.build_level_state")
    def test_respawn_keeps_playing_when_lives_remain(self, mock_build_level: MagicMock) -> None:
        old_level = self._make_stub_level()
        cp_old = Checkpoint(500, FLOOR_Y)
        cp_old.activate()
        old_level.checkpoints.add(cp_old)

        new_level = self._make_stub_level()
        cp_new = Checkpoint(500, FLOOR_Y)
        new_level.checkpoints.add(cp_new)

        mock_build_level.return_value = new_level

        game = Game()
        game.level = old_level
        game.current_level = 0
        game.lives = 2
        game._total_score = 321
        game.respawn_x = 500
        game.respawn_y = FLOOR_Y

        game._respawn_at_checkpoint()

        self.assertEqual(game.lives, 1)
        self.assertEqual(game.state, ST_PLAYING)
        self.assertEqual(game.player.score, 321)
        self.assertEqual(game.player.rect.bottomleft, (500, FLOOR_Y))
        self.assertTrue(any(cp.activated for cp in game.level.checkpoints))

    @patch("game.save_high_score")
    def test_respawn_sets_game_over_when_out_of_lives(self, mock_save: MagicMock) -> None:
        game = Game()
        game.level = self._make_stub_level()
        game.current_level = 2
        game.lives = 1
        game._total_score = 123

        game._respawn_at_checkpoint()

        self.assertEqual(game.state, ST_GAME_OVER)
        mock_save.assert_called_once_with(123, 3)

    @patch("game.save_high_score", return_value=True)
    def test_advancing_from_last_level_triggers_victory(self, _mock_save: MagicMock) -> None:
        game = Game()
        game.player = Player(100, FLOOR_Y)
        game.player.score = 777
        game.current_level = LEVEL_COUNT - 1

        game._advance_level()

        self.assertEqual(game.state, ST_VICTORY)
        self.assertTrue(game._is_high_score)


if __name__ == "__main__":
    unittest.main()
