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
    checkpoint_positions: list[int] = field(default_factory=list)
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

        floor = Platform(0, FLOOR_Y, level_def.world_width, SCREEN_HEIGHT - FLOOR_Y)
        self.platforms.add(floor)
        self.all_sprites.add(floor)

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

        for bx, by in level_def.bamboo_positions:
            b = Bamboo(bx, by)
            self.bamboos.add(b)
            self.all_sprites.add(b)

        for hx, hy in level_def.heal_positions:
            h = HealingItem(hx, hy)
            self.heals.add(h)
            self.all_sprites.add(h)

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

        for cp_x in level_def.checkpoint_positions:
            cp = Checkpoint(cp_x, FLOOR_Y)
            self.checkpoints.add(cp)
            self.all_sprites.add(cp)

        sz = SafeZone(level_def.goal_x, 200)
        self.goal = sz
        self.all_sprites.add(sz)

        if level_def.has_boss:
            self.boss = Boss(level_def.boss_pos[0], level_def.boss_pos[1])
            self.all_sprites.add(self.boss)

        step = random.randint(45, 65)
        for gx in range(0, level_def.world_width, step):
            self.decorations.add(GrassTuft(gx, FLOOR_Y))


# ---------------------------------------------------------------------------
# Level builders -- platforms well-spaced, min 400px gap between centers
# ---------------------------------------------------------------------------

def _scatter_bamboos(platforms: list[PlatformDef], world_width: int,
                     floor_y: int, target_count: int) -> list[tuple[int, int]]:
    """Generate varied bamboo positions: on platforms + clusters on floor."""
    positions: list[tuple[int, int]] = []

    # One bamboo per platform, randomized within platform width
    for p in platforms:
        bx = p.x + random.randint(20, max(20, p.w - 30))
        positions.append((bx, p.y))

    # Floor clusters in gaps between platforms, spread across the level
    # Find open floor areas (200px+ gaps between platform x ranges)
    occupied = sorted([(p.x, p.x + p.w) for p in platforms])
    gaps: list[tuple[int, int]] = []
    prev_end = 100
    for start, end in occupied:
        if start - prev_end > 250:
            gaps.append((prev_end + 50, start - 50))
        prev_end = max(prev_end, end)
    if world_width - prev_end > 250:
        gaps.append((prev_end + 50, world_width - 200))

    # Fill gaps with bamboo clusters until we hit target count
    while len(positions) < target_count and gaps:
        gap = random.choice(gaps)
        cluster_x = random.randint(gap[0], gap[1])
        cluster_size = random.randint(1, 3)
        for ci in range(cluster_size):
            bx = cluster_x + ci * random.randint(25, 45)
            if bx < gap[1] and len(positions) < target_count:
                positions.append((bx, floor_y))

    return positions


def _build_level_1() -> LevelDef:
    """Bamboo Grove - tutorial. Wide spacing, easy jumps."""
    plats = [
        PlatformDef(400, 420, 240),
        PlatformDef(900, 380, 200),
        PlatformDef(1400, 410, 260),
        PlatformDef(1900, 370, 220, moving=True, axis="horizontal", distance=100),
        PlatformDef(2450, 400, 240),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[0],
        platforms=plats,
        enemies=[
            EnemyDef(440, 410, "patrol", 180),
            EnemyDef(1440, 400, "patrol", 200),
            EnemyDef(2480, 390, "slime", 160),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[0], FLOOR_Y, 11),
        heal_positions=[(950, 380), (2500, 400)],
        goal_x=2800,
        checkpoint_positions=[1500],
    )


def _build_level_2() -> LevelDef:
    """Mountain Pass - intermediate. More platforms, still well-spaced."""
    plats = [
        PlatformDef(400, 420, 220),
        PlatformDef(900, 370, 180),
        PlatformDef(1400, 410, 240),
        PlatformDef(1900, 360, 200, moving=True, axis="horizontal", distance=110),
        PlatformDef(2450, 400, 200),
        PlatformDef(2950, 350, 200, moving=True, axis="vertical", distance=50),
        PlatformDef(3450, 390, 240),
        PlatformDef(3950, 380, 220),
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[1],
        platforms=plats,
        enemies=[
            EnemyDef(440, 410, "patrol", 180),
            EnemyDef(1440, 400, "patrol", 200),
            EnemyDef(2480, 390, "patrol", 160),
            EnemyDef(3480, 380, "slime", 180),
            EnemyDef(950, 360, "chaser"),
            EnemyDef(2990, 340, "chaser"),
            EnemyDef(1700, 260, "flying", 200),
            EnemyDef(3200, 270, "slime", 150),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[1], FLOOR_Y, 16),
        heal_positions=[(1450, 410), (3490, 390)],
        goal_x=4200,
        checkpoint_positions=[1700, 3200],
    )


def _build_level_3() -> LevelDef:
    """Mutant Lair - final level with boss."""
    plats = [
        PlatformDef(400, 420, 220),
        PlatformDef(900, 370, 180),
        PlatformDef(1400, 410, 240),
        PlatformDef(1950, 360, 200, moving=True, axis="vertical", distance=50),
        PlatformDef(2500, 400, 220),
        PlatformDef(3050, 370, 200),
        PlatformDef(3550, 400, 240, moving=True, axis="horizontal", distance=100),
        PlatformDef(4100, 380, 220),
        PlatformDef(4600, 400, 260),
        PlatformDef(5100, 420, 700, 20),  # boss arena
    ]
    return LevelDef(
        world_width=LEVEL_WIDTHS[2],
        platforms=plats,
        enemies=[
            EnemyDef(440, 410, "patrol", 180),
            EnemyDef(1440, 400, "patrol", 200),
            EnemyDef(2540, 390, "slime", 180),
            EnemyDef(3090, 360, "patrol", 160),
            EnemyDef(4140, 370, "patrol", 160),
            EnemyDef(950, 360, "chaser"),
            EnemyDef(2000, 350, "chaser"),
            EnemyDef(3580, 390, "chaser"),
            EnemyDef(1200, 260, "flying", 200),
            EnemyDef(2800, 250, "flying", 200),
            EnemyDef(4300, 260, "flying", 180),
            EnemyDef(3300, 390, "slime", 160),
        ],
        bamboo_positions=_scatter_bamboos(plats, LEVEL_WIDTHS[2], FLOOR_Y, 20),
        heal_positions=[(1450, 410), (3080, 370), (4900, FLOOR_Y)],
        goal_x=5850,
        checkpoint_positions=[1800, 3500, 4900],
        has_boss=True,
        boss_pos=(5500, FLOOR_Y),
    )


_BUILDERS = [_build_level_1, _build_level_2, _build_level_3]


def build_level_state(level_number: int) -> LevelState:
    return LevelState(_BUILDERS[level_number](), level_number)
