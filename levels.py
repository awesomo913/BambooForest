"""Level definitions and construction."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import pygame

from config import FLOOR_Y, LEVEL_WIDTHS, SCREEN_HEIGHT
from sprites import (
    Bamboo, Boss, ChaserEnemy, Checkpoint, FlyingEnemy, GrassTuft,
    HealingItem, MovingPlatform, PatrolEnemy, Platform,
    SafeZone, SlimeEnemy,
)


@dataclass
class PlatformDef:
    x: int
    y: int
    w: int
    h: int = 20
    moving: bool = False
    axis: str = "horizontal"
    distance: float = 150.0


@dataclass
class EnemyDef:
    x: int
    y: int
    kind: str
    patrol_width: float = 200.0
    flight_range: float = 200.0


@dataclass
class LevelDef:
    world_width: int
    platforms: list[PlatformDef]
    enemies: list[EnemyDef]
    bamboo_positions: list[tuple[int, int]]
    heal_positions: list[tuple[int, int]]
    goal_x: int
    checkpoint_positions: list[int] = field(default_factory=list)  # x positions on floor
    has_boss: bool = False
    boss_pos: tuple[int, int] = (0, 0)
    player_start: tuple[int, int] = (100, FLOOR_Y)


class LevelState:
    """Instantiated level with all sprite groups."""

    def __init__(self, level_def: LevelDef, level_number: int) -> None:
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.moving_platforms = pygame.sprite.Group()
        self.bamboos = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.heals = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.goal: SafeZone | None = None
        self.boss: Boss | None = None
        self.world_width = level_def.world_width
        self.level_number = level_number
        self.player_start = level_def.player_start

        # Floor
        floor = Platform(0, FLOOR_Y, level_def.world_width, SCREEN_HEIGHT - FLOOR_Y)
        self.platforms.add(floor)
        self.all_sprites.add(floor)

        # Platforms
        for pd in level_def.platforms:
            if pd.moving:
                mp = MovingPlatform(pd.x, pd.y, pd.w, pd.h, pd.axis, pd.distance)
                self.moving_platforms.add(mp)
                self.platforms.add(mp)
                self.all_sprites.add(mp)
            else:
                p = Platform(pd.x, pd.y, pd.w, pd.h)
                self.platforms.add(p)
                self.all_sprites.add(p)

        # Bamboo
        for bx, by in level_def.bamboo_positions:
            b = Bamboo(bx, by)
            self.bamboos.add(b)
            self.all_sprites.add(b)

        # Heals
        for hx, hy in level_def.heal_positions:
            h = HealingItem(hx, hy)
            self.heals.add(h)
            self.all_sprites.add(h)

        # Enemies
        for ed in level_def.enemies:
            if ed.kind == "patrol":
                e = PatrolEnemy(ed.x, ed.y, ed.patrol_width)
            elif ed.kind == "chaser":
                e = ChaserEnemy(ed.x, ed.y)
            elif ed.kind == "flying":
                e = FlyingEnemy(ed.x, ed.y, ed.flight_range)
            elif ed.kind == "slime":
                e = SlimeEnemy(ed.x, ed.y, ed.patrol_width)
            else:
                continue
            self.enemies.add(e)
            self.all_sprites.add(e)

        # Checkpoints
        for cp_x in level_def.checkpoint_positions:
            cp = Checkpoint(cp_x, FLOOR_Y)
            self.checkpoints.add(cp)
            self.all_sprites.add(cp)

        # Safe zone goal
        sz = SafeZone(level_def.goal_x, 200)
        self.goal = sz
        self.all_sprites.add(sz)

        # Boss
        if level_def.has_boss:
            self.boss = Boss(level_def.boss_pos[0], level_def.boss_pos[1])
            self.all_sprites.add(self.boss)

        # Decorative grass tufts
        step = random.randint(40, 70)
        for gx in range(0, level_def.world_width, step):
            gt = GrassTuft(gx, FLOOR_Y)
            self.decorations.add(gt)


# ---------------------------------------------------------------------------
# Level builders
# ---------------------------------------------------------------------------

def _build_level_1() -> LevelDef:
    """Bamboo Grove - tutorial."""
    return LevelDef(
        world_width=LEVEL_WIDTHS[0],
        platforms=[
            PlatformDef(350, 420, 220),
            PlatformDef(650, 370, 180),
            PlatformDef(950, 410, 250),
            PlatformDef(1300, 350, 180),
            PlatformDef(1650, 390, 220, moving=True, axis="horizontal", distance=120),
            PlatformDef(2000, 360, 200),
            PlatformDef(2400, 400, 260),
        ],
        enemies=[
            EnemyDef(380, 410, "patrol", 180),
            EnemyDef(990, 400, "patrol", 200),
            EnemyDef(2050, 350, "slime", 160),
        ],
        bamboo_positions=[
            (400, 420), (720, 370), (1050, 410), (1360, 350),
            (1730, 390), (2080, 360), (2500, 400),
            (550, FLOOR_Y), (1500, FLOOR_Y),
        ],
        heal_positions=[(990, 410), (2050, 360), (2450, 400)],
        goal_x=2800,
        checkpoint_positions=[1400],  # roughly halfway
    )


def _build_level_2() -> LevelDef:
    """Mountain Pass - intermediate."""
    return LevelDef(
        world_width=LEVEL_WIDTHS[1],
        platforms=[
            PlatformDef(300, 420, 200),
            PlatformDef(580, 370, 160),
            PlatformDef(850, 420, 220),
            PlatformDef(1150, 350, 180),
            PlatformDef(1450, 390, 200, moving=True, axis="horizontal", distance=130),
            PlatformDef(1800, 340, 170),
            PlatformDef(2100, 400, 200),
            PlatformDef(2400, 350, 180, moving=True, axis="vertical", distance=60),
            PlatformDef(2700, 380, 200),
            PlatformDef(3050, 350, 200),
            PlatformDef(3400, 390, 260),
            PlatformDef(3800, 380, 220),
        ],
        enemies=[
            EnemyDef(340, 410, "patrol", 160),
            EnemyDef(880, 410, "patrol", 180),
            EnemyDef(2130, 390, "patrol", 160),
            EnemyDef(3430, 380, "slime", 200),
            EnemyDef(1180, 340, "chaser"),
            EnemyDef(2730, 370, "chaser"),
            EnemyDef(3080, 340, "chaser"),
            EnemyDef(1850, 260, "flying", 180),
            EnemyDef(3200, 270, "slime", 150),
        ],
        bamboo_positions=[
            (360, 420), (630, 370), (920, 420), (1200, 350),
            (1530, 390), (1850, 340), (2150, 400), (2450, 350),
            (2770, 380), (3110, 350), (3480, 390), (3870, 380),
            (500, FLOOR_Y), (1600, FLOOR_Y), (2900, FLOOR_Y),
        ],
        heal_positions=[(880, 420), (2130, 400)],
        goal_x=4200,
        checkpoint_positions=[1500, 3000],  # two checkpoints
    )


def _build_level_3() -> LevelDef:
    """Mutant Lair - final level with boss."""
    return LevelDef(
        world_width=LEVEL_WIDTHS[2],
        platforms=[
            PlatformDef(300, 420, 200),
            PlatformDef(580, 370, 160),
            PlatformDef(880, 420, 220),
            PlatformDef(1200, 360, 170, moving=True, axis="vertical", distance=50),
            PlatformDef(1500, 400, 200),
            PlatformDef(1800, 350, 180),
            PlatformDef(2100, 400, 220, moving=True, axis="horizontal", distance=120),
            PlatformDef(2450, 360, 180),
            PlatformDef(2750, 390, 170),
            PlatformDef(3050, 410, 220),
            PlatformDef(3400, 370, 200, moving=True, axis="horizontal", distance=100),
            PlatformDef(3750, 390, 220),
            PlatformDef(4100, 380, 200),
            PlatformDef(4450, 400, 260),
            PlatformDef(5000, 410, 800, 20),  # boss arena
        ],
        enemies=[
            EnemyDef(340, 410, "patrol", 160),
            EnemyDef(910, 410, "patrol", 180),
            EnemyDef(1530, 390, "slime", 160),
            EnemyDef(3080, 400, "patrol", 180),
            EnemyDef(4130, 370, "patrol", 160),
            EnemyDef(620, 360, "chaser"),
            EnemyDef(1830, 340, "chaser"),
            EnemyDef(2780, 380, "chaser"),
            EnemyDef(3780, 380, "chaser"),
            EnemyDef(1150, 260, "flying", 180),
            EnemyDef(2250, 240, "flying", 200),
            EnemyDef(3550, 260, "flying", 160),
            EnemyDef(2500, 350, "slime", 140),
        ],
        bamboo_positions=[
            (360, 420), (630, 370), (950, 420), (1250, 360),
            (1560, 400), (1860, 350), (2180, 400), (2500, 360),
            (2800, 390), (3110, 410), (3470, 370), (3810, 390),
            (4150, 380), (4530, 400),
            (600, FLOOR_Y), (1600, FLOOR_Y), (2900, FLOOR_Y), (4700, FLOOR_Y),
        ],
        heal_positions=[(910, 420), (2480, 360), (4750, FLOOR_Y)],
        goal_x=5850,
        checkpoint_positions=[1800, 3500, 4800],  # three checkpoints before boss
        has_boss=True,
        boss_pos=(5400, FLOOR_Y),
    )


_BUILDERS = [_build_level_1, _build_level_2, _build_level_3]


def build_level_state(level_number: int) -> LevelState:
    return LevelState(_BUILDERS[level_number](), level_number)
