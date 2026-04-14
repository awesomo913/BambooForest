"""Biome-specific sprites: mechanics, enemies, NPCs for levels 4-8."""

from __future__ import annotations

import math
import random
from math import floor as _fl

import pygame

from config import (
    ASH_BAT_RANGE, ASH_BAT_SWOOP, BRINE_DMG_RADIUS, BRINE_GROW_RATE,
    COL_BASALT, COL_BLACK, COL_CRYSTAL, COL_ICE, COL_LAVA, COL_LIMESTONE,
    COL_SALT, COL_SANDSTONE, COL_TOXIC, COL_WHITE, CRUMBLE_DELAY,
    CRUMBLE_RESPAWN, CRYSTAL_LIGHT_TIME, CRYSTAL_RADIUS, DARK_RADIUS,
    DUST_DEVIL_SPEED, ENEMY_PATROL_SPEED, FLOOR_Y, GLOWWORM_SNAP_RANGE,
    GEYSER_DURATION, GEYSER_INTERVAL, GEYSER_LAUNCH, GOLEM_COOLDOWN,
    GOLEM_STRIKE_RANGE, GOLEM_STRIKE_SPEED, GRAVITY, ICE_ACCEL,
    ICE_FRICTION, KELP_CRAB_SPEED, NPC_RANGE, PHANTOM_SPEED,
    PLAYER_SPEED, SCORPION_FIRE_RATE, SCORPION_PROJ_SPEED,
    SPIDER_DROP_RANGE, SPIDER_DROP_SPEED, SULFUR_SPEED,
    SULFUR_TRAIL_DMG, SULFUR_TRAIL_LIFE, TERMINAL_VELOCITY,
    WIND_PUSH,
)

# ===================================================================
# BIOME-THEMED PLATFORM TILES
# ===================================================================

def generate_volcanic_tile(width: int, height: int) -> pygame.Surface:
    """Dark volcanic basalt with orange lava crack highlights."""
    surf = pygame.Surface((width, height))
    # Dark rock base
    for y in range(height):
        t = y / max(1, height)
        c = (int(45 - 15 * t), int(30 - 10 * t), int(25 - 5 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Top crust (cooled lava)
    pygame.draw.rect(surf, (80, 50, 40), (0, 0, width, 4))
    pygame.draw.rect(surf, (120, 70, 40), (0, 0, width, 2))
    # Lava cracks (random horizontal squiggles)
    for _ in range(width // 20):
        cx = random.randint(0, width - 10)
        cy = random.randint(6, height - 4)
        cw = random.randint(6, 14)
        pygame.draw.line(surf, (220, 80, 30), (cx, cy), (cx + cw, cy + 2), 1)
        pygame.draw.line(surf, (255, 150, 60), (cx, cy), (cx + cw, cy + 2), 1)
    # Pumice specks
    for _ in range(width * height // 50):
        nx = random.randint(1, width - 2)
        ny = random.randint(5, height - 2)
        surf.set_at((nx, ny), (80, 60, 55))
    # Edge
    pygame.draw.rect(surf, (20, 15, 20), (0, 0, 2, height))
    pygame.draw.rect(surf, (20, 15, 20), (width - 2, 0, 2, height))
    return surf


def generate_basalt_tile(width: int, height: int) -> pygame.Surface:
    """Hexagonal basalt columns -- dark gray with top lip."""
    surf = pygame.Surface((width, height))
    # Deep gray body
    for y in range(height):
        t = y / max(1, height)
        c = (int(70 - 20 * t), int(75 - 20 * t), int(90 - 20 * t))
        pygame.draw.line(surf, c, (0, y), (width, y))
    # Hex top stripe (lighter)
    pygame.draw.rect(surf, (100, 105, 120), (0, 0, width, 3))
    # Vertical column lines (every 40px)
    for cx in range(0, width, 40):
        pygame.draw.line(surf, (40, 45, 55), (cx, 3), (cx, height), 1)
        pygame.draw.line(surf, (90, 95, 110), (cx + 1, 3), (cx + 1, height), 1)
    # Subtle horizontal banding
    for by in range(8, height, 12):
        pygame.draw.line(surf, (55, 60, 75), (0, by), (width, by), 1)
    # Edge
    pygame.draw.rect(surf, (30, 30, 40), (0, 0, 2, height))
    pygame.draw.rect(surf, (30, 30, 40), (width - 2, 0, 2, height))
    return surf


def generate_sandstone_tile(width: int, height: int) -> pygame.Surface:
    """Layered tan sandstone with erosion marks."""
    surf = pygame.Surface((width, height))
    # Layered bands of varying tan
    band_colors = [
        (210, 175, 120), (195, 160, 105), (180, 145, 90),
        (170, 135, 85), (160, 125, 80),
    ]
    band_h = max(2, height // len(band_colors))
    for i, c in enumerate(band_colors):
        pygame.draw.rect(surf, c, (0, i * band_h, width, band_h))
    # Top lighter stripe (wind-polished)
    pygame.draw.rect(surf, (225, 195, 140), (0, 0, width, 3))
    # Erosion divots
    for _ in range(width // 15):
        ex = random.randint(2, width - 4)
        ey = random.randint(4, height - 2)
        pygame.draw.ellipse(surf, (150, 115, 75), (ex, ey, 4, 2))
    # Specks
    for _ in range(width * height // 60):
        nx = random.randint(1, width - 2)
        ny = random.randint(3, height - 2)
        shade = random.randint(-15, 15)
        surf.set_at((nx, ny),
                    (max(0, min(255, 180 + shade)),
                     max(0, min(255, 145 + shade)),
                     max(0, min(255, 90 + shade))))
    pygame.draw.rect(surf, (120, 95, 60), (0, 0, 2, height))
    pygame.draw.rect(surf, (120, 95, 60), (width - 2, 0, 2, height))
    return surf


def generate_limestone_tile(width: int, height: int) -> pygame.Surface:
    """Pale gray-tan limestone cave floor with fossil marks."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height)
        c = (int(170 - 30 * t), int(165 - 30 * t), int(150 - 30 * t))
        pygame.draw.line(surf, c, (0, y), (width, y))
    pygame.draw.rect(surf, (190, 180, 165), (0, 0, width, 3))
    # Fossil impressions (small curved lines)
    for _ in range(width // 25):
        fx = random.randint(4, width - 8)
        fy = random.randint(6, height - 4)
        pygame.draw.arc(surf, (120, 115, 100), (fx, fy, 6, 4), 0, 3.14, 1)
    # Specks
    for _ in range(width * height // 70):
        nx = random.randint(1, width - 2)
        ny = random.randint(3, height - 2)
        shade = random.randint(-15, 10)
        surf.set_at((nx, ny),
                    (max(0, min(255, 155 + shade)),
                     max(0, min(255, 150 + shade)),
                     max(0, min(255, 135 + shade))))
    pygame.draw.rect(surf, (90, 85, 75), (0, 0, 2, height))
    pygame.draw.rect(surf, (90, 85, 75), (width - 2, 0, 2, height))
    return surf


def generate_salt_tile(width: int, height: int) -> pygame.Surface:
    """Pale blue-white salt crystal surface, reflective."""
    surf = pygame.Surface((width, height))
    # Near-white body with pale blue hint
    for y in range(height):
        t = y / max(1, height)
        c = (int(220 - 20 * t), int(235 - 15 * t), int(250 - 10 * t))
        pygame.draw.line(surf, c, (0, y), (width, y))
    # Bright top
    pygame.draw.rect(surf, (245, 250, 255), (0, 0, width, 4))
    # Crystal facet lines
    for cx in range(0, width, random.randint(20, 35)):
        pygame.draw.line(surf, (180, 210, 235), (cx, 4),
                         (cx + random.randint(-3, 3), height), 1)
    # Sparkle highlights
    for _ in range(width // 10):
        sx = random.randint(1, width - 2)
        sy = random.randint(3, height - 2)
        surf.set_at((sx, sy), (255, 255, 255))
    pygame.draw.rect(surf, (160, 190, 220), (0, 0, 2, height))
    pygame.draw.rect(surf, (160, 190, 220), (width - 2, 0, 2, height))
    return surf


_TILE_GENERATORS = {
    "volcanic": generate_volcanic_tile,
    "basalt": generate_basalt_tile,
    "desert": generate_sandstone_tile,
    "cave": generate_limestone_tile,
    "salt": generate_salt_tile,
}


class BiomePlatform(pygame.sprite.Sprite):
    """Platform with biome-specific tile art."""

    def __init__(self, x: int, y: int, w: int, h: int = 20,
                 biome: str = "forest") -> None:
        super().__init__()
        gen = _TILE_GENERATORS.get(biome)
        if gen:
            self.image = gen(w, h)
        else:
            from sprites import generate_platform_tile
            self.image = generate_platform_tile(w, h)
        self.rect = self.image.get_rect(topleft=(x, y))


class BiomeMovingPlatform(pygame.sprite.Sprite):
    """Moving platform with biome-specific tile art."""

    def __init__(self, x: int, y: int, w: int, h: int,
                 axis: str = "horizontal", distance: float = 150.0,
                 biome: str = "forest") -> None:
        super().__init__()
        gen = _TILE_GENERATORS.get(biome)
        if gen:
            self.image = gen(w, h)
        else:
            from sprites import generate_platform_tile
            self.image = generate_platform_tile(w, h)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.axis = axis
        self.distance = distance
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update_moving(self, dt: float) -> tuple[float, float]:
        from config import MOVING_PLAT_SPEED
        old_x, old_y = self.pos_x, self.pos_y
        step = MOVING_PLAT_SPEED * self.direction * dt
        if self.axis == "horizontal":
            self.pos_x += step
            if self.pos_x > self.origin_x + self.distance:
                self.pos_x = self.origin_x + self.distance
                self.direction = -1.0
            elif self.pos_x < self.origin_x - self.distance:
                self.pos_x = self.origin_x - self.distance
                self.direction = 1.0
        else:
            self.pos_y += step
            if self.pos_y > self.origin_y + self.distance:
                self.pos_y = self.origin_y + self.distance
                self.direction = -1.0
            elif self.pos_y < self.origin_y - self.distance:
                self.pos_y = self.origin_y - self.distance
                self.direction = 1.0
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(self.pos_y)
        return (self.pos_x - old_x, self.pos_y - old_y)


# ===================================================================
# MECHANIC SPRITES
# ===================================================================


class Geyser(pygame.sprite.Sprite):
    """Level 4. Periodically erupts, launching player upward."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # Dormant: dark rock opening with faint orange glow
        self._img_off = pygame.Surface((44, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(self._img_off, (40, 25, 30), (0, 8, 44, 16))
        pygame.draw.ellipse(self._img_off, (80, 45, 35), (4, 10, 36, 12))
        pygame.draw.ellipse(self._img_off, (180, 80, 40), (8, 12, 28, 8))
        pygame.draw.ellipse(self._img_off, (60, 35, 30), (2, 18, 40, 6))  # rock lip
        # Erupting: tall steam+lava column
        self._img_on = pygame.Surface((44, 200), pygame.SRCALPHA)
        # Base glow
        pygame.draw.ellipse(self._img_on, (40, 25, 30), (0, 184, 44, 16))
        pygame.draw.ellipse(self._img_on, (255, 100, 30), (4, 186, 36, 12))
        # Rising jet (narrowing toward top)
        for y in range(0, 185):
            t = y / 185.0
            w = int(8 + 24 * t)  # wider at bottom
            xc = 22
            alpha = int(200 - 150 * (1 - t))
            if y < 40:
                c = (255, 240, 180, min(255, alpha))
            elif y < 100:
                c = (255, 180, 80, min(255, alpha))
            else:
                c = (255, 120, 50, min(255, alpha))
            pygame.draw.rect(self._img_on, c, (xc - w // 2, y, w, 1))
        # Steam puffs at top
        for _ in range(8):
            px = random.randint(8, 36)
            py = random.randint(0, 40)
            pygame.draw.circle(self._img_on, (240, 230, 220, 180), (px, py),
                               random.randint(4, 8))
        self.image = self._img_off
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self._off_rect = self.image.get_rect(bottomleft=(x, y))
        self._on_rect = self._img_on.get_rect(bottomleft=(x, y))
        self.erupt_timer: float = random.uniform(0, GEYSER_INTERVAL)
        self.erupt_remaining: float = 0.0

    def update(self, dt: float) -> None:
        if self.erupt_remaining > 0:
            self.erupt_remaining -= dt
            if self.image is not self._img_on:
                self.image = self._img_on
                self.rect = self._on_rect.copy()
            if self.erupt_remaining <= 0:
                self.erupt_timer = GEYSER_INTERVAL
                self.image = self._img_off
                self.rect = self._off_rect.copy()
        else:
            self.erupt_timer -= dt
            if self.erupt_timer <= 0:
                self.erupt_remaining = GEYSER_DURATION

    def is_active(self) -> bool:
        return self.erupt_remaining > 0


class ToxicTrail(pygame.sprite.Sprite):
    """Level 4. Damage zone left by SulfurSlime."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((22, 8), pygame.SRCALPHA)
        # Goo puddle with bubbles
        pygame.draw.ellipse(self.image, (100, 160, 40), (0, 2, 22, 6))
        pygame.draw.ellipse(self.image, (160, 220, 60), (2, 3, 18, 3))
        # Bubbles
        pygame.draw.circle(self.image, (220, 255, 120), (6, 3), 1)
        pygame.draw.circle(self.image, (220, 255, 120), (14, 4), 1)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.lifetime: float = SULFUR_TRAIL_LIFE

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.lifetime -= dt
        # Fade as it ages
        if self.lifetime < 1.0:
            alpha = int(255 * self.lifetime)
            self.image.set_alpha(alpha)
        if self.lifetime <= 0:
            self.kill()


class CrumblingPlatform(pygame.sprite.Sprite):
    """Level 5. Crumbles after player stands on it, then respawns."""

    def __init__(self, x: int, y: int, w: int, h: int = 20,
                 platforms_group: pygame.sprite.Group | None = None) -> None:
        super().__init__()
        self.w, self.h = w, h
        self._img_solid = pygame.Surface((w, h))
        self._img_solid.fill(COL_BASALT)
        pygame.draw.rect(self._img_solid, (80, 80, 90), (0, 0, w, 4))
        self._img_crumbling = pygame.Surface((w, h), pygame.SRCALPHA)
        for bx in range(0, w, 6):
            by = random.randint(0, h - 4)
            pygame.draw.rect(self._img_crumbling, (70, 70, 80, 150), (bx, by, 5, 4))

        self.image = self._img_solid
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = True
        self.touched = False
        self.crumble_timer: float = 0.0
        self.respawn_timer: float = 0.0
        self._platforms_group = platforms_group
        self._origin = (x, y)

    def touch(self) -> None:
        if not self.touched and self.solid:
            self.touched = True
            self.crumble_timer = CRUMBLE_DELAY

    def update(self, dt: float) -> None:  # type: ignore[override]
        if self.touched and self.solid:
            self.crumble_timer -= dt
            # Flicker before crumbling
            if self.crumble_timer < 0.3 and int(self.crumble_timer * 20) % 2:
                self.image = self._img_crumbling
            else:
                self.image = self._img_solid
            if self.crumble_timer <= 0:
                self.solid = False
                self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
                self.rect = self.image.get_rect(topleft=self._origin)
                if self._platforms_group and self in self._platforms_group:
                    self._platforms_group.remove(self)
                self.respawn_timer = CRUMBLE_RESPAWN
        elif not self.solid:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.solid = True
                self.touched = False
                self.image = self._img_solid
                self.rect = self.image.get_rect(topleft=self._origin)
                if self._platforms_group and self not in self._platforms_group:
                    self._platforms_group.add(self)


class WindZone(pygame.sprite.Sprite):
    """Level 6. Pushes player sideways."""

    def __init__(self, x: int, y: int, w: int, h: int,
                 direction: float = 1.0) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        col = (*COL_SANDSTONE, 40)
        self.image.fill(col)
        # Arrow indicators
        for ay in range(10, h - 10, 30):
            ax = w // 2 + (10 if direction > 0 else -10)
            pygame.draw.polygon(self.image, (*COL_SANDSTONE, 80), [
                (ax - 8, ay), (ax + 8, ay + 8), (ax - 8, ay + 16)])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction

    def get_push(self) -> float:
        return WIND_PUSH * self.direction


class ThermalUpdraft(pygame.sprite.Sprite):
    """Level 6. Vertical column giving upward boost."""

    def __init__(self, x: int, y: int, w: int = 60, h: int = 200) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((220, 180, 100, 30))
        for uy in range(0, h, 15):
            pygame.draw.line(self.image, (240, 200, 120, 50),
                             (w // 2 - 5, uy), (w // 2 + 5, uy - 8), 1)
        self.rect = self.image.get_rect(bottomleft=(x, y))


class Crystal(pygame.sprite.Sprite):
    """Level 7. Strike to expand visibility in dark levels."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_dim = pygame.Surface((20, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self._img_dim, (60, 100, 140),
                            [(10, 0), (20, 15), (10, 30), (0, 15)])
        self._img_lit = pygame.Surface((20, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self._img_lit, COL_CRYSTAL,
                            [(10, 0), (20, 15), (10, 30), (0, 15)])
        pygame.draw.polygon(self._img_lit, (180, 240, 255),
                            [(10, 4), (16, 15), (10, 26), (4, 15)])
        self.image = self._img_dim
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.lit = False
        self.light_timer: float = 0.0

    def strike(self) -> None:
        self.lit = True
        self.light_timer = CRYSTAL_LIGHT_TIME
        self.image = self._img_lit

    def update(self, dt: float) -> None:  # type: ignore[override]
        if self.lit:
            self.light_timer -= dt
            if self.light_timer <= 0:
                self.lit = False
                self.image = self._img_dim

    def is_lit(self) -> bool:
        return self.lit


class IcePlatform(pygame.sprite.Sprite):
    """Level 8. Platform with ice physics flag."""

    is_ice: bool = True

    def __init__(self, x: int, y: int, w: int, h: int = 20) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(COL_ICE)
        pygame.draw.rect(self.image, (200, 235, 255), (0, 0, w, 4))
        # Ice shine
        for sx in range(0, w, 8):
            pygame.draw.rect(self.image, (220, 240, 255), (sx, 1, 3, 2))
        self.rect = self.image.get_rect(topleft=(x, y))


class ScorpionProjectile(pygame.sprite.Sprite):
    """Level 6. 45-degree thorn from CactusScorpion."""

    def __init__(self, x: int, y: int, direction: float) -> None:
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 180, 60), (4, 4), 4)
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.radians(45)
        self.vx = SCORPION_PROJ_SPEED * direction * math.cos(angle)
        self.vy = -SCORPION_PROJ_SPEED * math.sin(angle)
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.pos_x += self.vx * dt
        self.pos_y += self.vy * dt
        self.vy += GRAVITY * 0.3 * dt  # slight arc
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(self.pos_y)
        if self.rect.y > FLOOR_Y + 100 or self.rect.x < -50 or self.rect.x > 8000:
            self.kill()


# ===================================================================
# ENEMIES (all: update(dt, platforms, player), is_stompable, die())
# ===================================================================

class SulfurSlime(pygame.sprite.Sprite):
    """Level 4. Slow patrol, leaves toxic trail."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 150.0) -> None:
        super().__init__()
        self.image = pygame.Surface((30, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (180, 200, 40), (0, 4, 30, 24))
        pygame.draw.circle(self.image, COL_WHITE, (10, 12), 3)
        pygame.draw.circle(self.image, COL_WHITE, (20, 12), 3)
        pygame.draw.circle(self.image, COL_BLACK, (11, 12), 2)
        pygame.draw.circle(self.image, COL_BLACK, (19, 12), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.trail_timer: float = 0.0
        self._pending_trails: list[ToxicTrail] = []

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self._pending_trails.clear()
        self.pos_x += SULFUR_SPEED * self.direction * dt
        if self.pos_x > self.origin_x + self.patrol_width:
            self.pos_x = self.origin_x + self.patrol_width
            self.direction = -1.0
        elif self.pos_x < self.origin_x - self.patrol_width:
            self.pos_x = self.origin_x - self.patrol_width
            self.direction = 1.0
        self.rect.x = _fl(self.pos_x)
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
        self.trail_timer += dt
        if self.trail_timer >= 0.5:
            self.trail_timer = 0.0
            self._pending_trails.append(ToxicTrail(self.rect.centerx - 10, self.rect.bottom))

    def get_new_trails(self) -> list[ToxicTrail]:
        return self._pending_trails

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class AshBat(pygame.sprite.Sprite):
    """Level 4. Swoops when player is mid-air."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((34, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (80, 60, 60), (10, 8, 14, 16))
        pygame.draw.polygon(self.image, (100, 70, 70), [(10, 14), (0, 4), (14, 10)])
        pygame.draw.polygon(self.image, (100, 70, 70), [(24, 14), (34, 4), (20, 10)])
        pygame.draw.circle(self.image, (255, 120, 40), (14, 13), 2)
        pygame.draw.circle(self.image, (255, 120, 40), (20, 13), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.state = "hover"
        self.swoop_tx: float = 0.0
        self.swoop_ty: float = 0.0
        self.alive_flag = True
        self.hover_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag or player is None:
            return
        if self.state == "hover":
            self.hover_timer += dt
            self.rect.y = _fl(self.origin_y + math.sin(self.hover_timer * 3) * 8)
            dist = math.hypot(player.rect.centerx - self.rect.centerx,
                              player.rect.centery - self.rect.centery)
            if not player.is_on_ground and dist < ASH_BAT_RANGE:
                self.state = "swoop"
                self.swoop_tx = float(player.rect.centerx)
                self.swoop_ty = float(player.rect.centery)
        elif self.state == "swoop":
            dx = self.swoop_tx - self.rect.centerx
            dy = self.swoop_ty - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 5:
                self.rect.x += _fl(dx / dist * ASH_BAT_SWOOP * dt)
                self.rect.y += _fl(dy / dist * ASH_BAT_SWOOP * dt)
            else:
                self.state = "return"
        elif self.state == "return":
            dx = self.origin_x - self.rect.centerx
            dy = self.origin_y - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 5:
                self.rect.x += _fl(dx / dist * ASH_BAT_SWOOP * 0.5 * dt)
                self.rect.y += _fl(dy / dist * ASH_BAT_SWOOP * 0.5 * dt)
            else:
                self.state = "hover"

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class KelpCrab(pygame.sprite.Sprite):
    """Level 5. Armored patrol, stomp-only kill."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 120.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (180, 80, 60), (2, 2, 32, 18))
        pygame.draw.rect(self.image, (160, 60, 40), (0, 6, 6, 4))
        pygame.draw.rect(self.image, (160, 60, 40), (30, 6, 6, 4))
        pygame.draw.circle(self.image, COL_WHITE, (12, 8), 3)
        pygame.draw.circle(self.image, COL_WHITE, (24, 8), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 8), 2)
        pygame.draw.circle(self.image, COL_BLACK, (23, 8), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self.pos_x += KELP_CRAB_SPEED * self.direction * dt
        if self.pos_x > self.origin_x + self.patrol_width:
            self.pos_x = self.origin_x + self.patrol_width
            self.direction = -1.0
        elif self.pos_x < self.origin_x - self.patrol_width:
            self.pos_x = self.origin_x - self.patrol_width
            self.direction = 1.0
        self.rect.x = _fl(self.pos_x)
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class BasaltGolem(pygame.sprite.Sprite):
    """Level 5. Disguised pillar that lunges when close."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_dormant = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.rect(self._img_dormant, COL_BASALT, (0, 0, 30, 50), border_radius=3)
        self._img_active = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.rect(self._img_active, (90, 80, 80), (0, 0, 30, 50), border_radius=3)
        pygame.draw.circle(self._img_active, (255, 80, 40), (10, 15), 4)
        pygame.draw.circle(self._img_active, (255, 80, 40), (20, 15), 4)
        self.image = self._img_dormant
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.state = "dormant"
        self.state_timer: float = 0.0
        self.strike_dir: float = 0.0
        self.origin_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag or player is None:
            return
        # Gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0

        dist = abs(player.rect.centerx - self.rect.centerx)
        if self.state == "dormant":
            self.image = self._img_dormant
            if dist < GOLEM_STRIKE_RANGE:
                self.state = "telegraph"
                self.state_timer = 0.3
                self.strike_dir = 1.0 if player.rect.centerx > self.rect.centerx else -1.0
        elif self.state == "telegraph":
            self.image = self._img_active
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "striking"
                self.state_timer = 0.4
        elif self.state == "striking":
            self.image = self._img_active
            self.rect.x += _fl(GOLEM_STRIKE_SPEED * self.strike_dir * dt)
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "cooldown"
                self.state_timer = GOLEM_COOLDOWN
        elif self.state == "cooldown":
            self.image = self._img_dormant
            # Return to origin
            dx = self.origin_x - self.rect.x
            if abs(dx) > 2:
                self.rect.x += _fl(dx * 2 * dt)
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "dormant"

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class DustDevil(pygame.sprite.Sprite):
    """Level 6. Invincible erratic movement, must dodge."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int, patrol_width: float = 300.0) -> None:
        super().__init__()
        self.image = pygame.Surface((30, 50), pygame.SRCALPHA)
        for dy in range(0, 50, 3):
            w = 15 + int(8 * math.sin(dy * 0.2))
            pygame.draw.rect(self.image, (*COL_SANDSTONE, 120),
                             (15 - w // 2, dy, w, 3))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.pos_x = float(x)
        self.time: float = random.uniform(0, 6.28)
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        self.time += dt * 3
        self.pos_x = self.origin_x + math.sin(self.time) * self.patrol_width * 0.5
        self.pos_x += math.sin(self.time * 2.7) * self.patrol_width * 0.3
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(FLOOR_Y - 50 + math.sin(self.time * 1.5) * 10)

    def die(self) -> None:
        pass  # invincible


class CactusScorpion(pygame.sprite.Sprite):
    """Level 6. Fires 45-degree projectiles."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 100.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (160, 120, 60), (4, 8, 28, 18))
        pygame.draw.rect(self.image, (140, 100, 40), (28, 2, 6, 10))
        pygame.draw.circle(self.image, (200, 180, 60), (32, 2), 3)
        pygame.draw.circle(self.image, COL_WHITE, (12, 14), 3)
        pygame.draw.circle(self.image, COL_WHITE, (22, 14), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 14), 2)
        pygame.draw.circle(self.image, COL_BLACK, (21, 14), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.fire_timer: float = SCORPION_FIRE_RATE
        self._pending_proj: list[ScorpionProjectile] = []

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self._pending_proj.clear()
        self.pos_x += ENEMY_PATROL_SPEED * 0.5 * self.direction * dt
        if self.pos_x > self.origin_x + self.patrol_width:
            self.pos_x = self.origin_x + self.patrol_width
            self.direction = -1.0
        elif self.pos_x < self.origin_x - self.patrol_width:
            self.pos_x = self.origin_x - self.patrol_width
            self.direction = 1.0
        self.rect.x = _fl(self.pos_x)
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
        self.fire_timer -= dt
        if self.fire_timer <= 0:
            self.fire_timer = SCORPION_FIRE_RATE
            self._pending_proj.append(
                ScorpionProjectile(self.rect.centerx, self.rect.top, self.direction))

    def get_new_projectiles(self) -> list[ScorpionProjectile]:
        return self._pending_proj

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class StalactiteSpider(pygame.sprite.Sprite):
    """Level 7. Drops from ceiling when player passes below."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((28, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (60, 50, 50), (4, 2, 20, 16))
        for lx in (2, 8, 16, 22):
            pygame.draw.line(self.image, (50, 40, 40), (lx, 10), (lx - 2, 18), 1)
        pygame.draw.circle(self.image, (200, 40, 40), (11, 7), 2)
        pygame.draw.circle(self.image, (200, 40, 40), (17, 7), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.state = "hanging"
        self.origin_y = y
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.pos_x = float(x)
        self.direction: float = 1.0

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag or player is None:
            return
        if self.state == "hanging":
            if (abs(player.rect.centerx - self.rect.centerx) < SPIDER_DROP_RANGE
                    and player.rect.centery > self.rect.centery):
                self.state = "dropping"
                self.velocity_y = 0
        elif self.state == "dropping":
            self.velocity_y += GRAVITY * dt
            if self.velocity_y > SPIDER_DROP_SPEED:
                self.velocity_y = SPIDER_DROP_SPEED
            self.rect.y += _fl(self.velocity_y * dt)
            for hit in pygame.sprite.spritecollide(self, platforms, False):
                if self.velocity_y > 0:
                    self.rect.bottom = hit.rect.top
                    self.velocity_y = 0
                    self.state = "grounded"
                    self.pos_x = float(self.rect.x)
        elif self.state == "grounded":
            self.pos_x += ENEMY_PATROL_SPEED * 0.6 * self.direction * dt
            if abs(self.pos_x - self.rect.x) > 80:
                self.direction *= -1
            self.rect.x = _fl(self.pos_x)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class FalseGlowworm(pygame.sprite.Sprite):
    """Level 7. Looks like light source, snaps shut as trap."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_lure = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self._img_lure, (150, 255, 100), (8, 8), 8)
        pygame.draw.circle(self._img_lure, (200, 255, 180), (8, 8), 4)
        self._img_snap = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self._img_snap, (255, 60, 40), (8, 8), 8)
        pygame.draw.circle(self._img_snap, (255, 120, 100), (8, 8), 4)
        self.image = self._img_lure
        self.rect = self.image.get_rect(center=(x, y))
        self.state = "luring"
        self.state_timer: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if player is None:
            return
        dist = math.hypot(player.rect.centerx - self.rect.centerx,
                          player.rect.centery - self.rect.centery)
        if self.state == "luring":
            self.image = self._img_lure
            if dist < GLOWWORM_SNAP_RANGE:
                self.state = "snapping"
                self.state_timer = 0.5
        elif self.state == "snapping":
            self.image = self._img_snap
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "cooldown"
                self.state_timer = 3.0
        elif self.state == "cooldown":
            self.image = self._img_lure
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "luring"

    def die(self) -> None:
        pass  # invincible


class BrineShard(pygame.sprite.Sprite):
    """Level 8. Static crystal that grows when player stands still nearby."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_size = 16
        self.size_scale: float = 1.0
        self._regen_image()
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.base_y = y
        self.alive_flag = True

    def _regen_image(self) -> None:
        sz = max(8, int(self.base_size * self.size_scale))
        self.image = pygame.Surface((sz, sz * 2), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, COL_SALT,
                            [(sz // 2, 0), (sz, sz * 2), (0, sz * 2)])
        pygame.draw.polygon(self.image, COL_ICE,
                            [(sz // 2, sz // 2), (sz - 2, sz * 2), (2, sz * 2)])

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if player is None:
            return
        dist = math.hypot(player.rect.centerx - self.rect.centerx,
                          player.rect.centery - self.rect.centery)
        player_still = abs(player.velocity_x) < 10
        if dist < BRINE_DMG_RADIUS * 2 and player_still:
            self.size_scale = min(3.0, self.size_scale + BRINE_GROW_RATE * dt)
        else:
            self.size_scale = max(1.0, self.size_scale - BRINE_GROW_RATE * 0.5 * dt)
        old_center = self.rect.center
        self._regen_image()
        self.rect = self.image.get_rect(center=old_center)

    def die(self) -> None:
        pass


class ReflectionPhantom(pygame.sprite.Sprite):
    """Level 8. Patrol enemy only visible in reflection."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 200.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (*COL_WHITE, 60), (2, 2, 32, 32))
        pygame.draw.circle(self.image, (*COL_ICE, 80), (12, 14), 3)
        pygame.draw.circle(self.image, (*COL_ICE, 80), (24, 14), 3)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self.pos_x += PHANTOM_SPEED * self.direction * dt
        if self.pos_x > self.origin_x + self.patrol_width:
            self.pos_x = self.origin_x + self.patrol_width
            self.direction = -1.0
        elif self.pos_x < self.origin_x - self.patrol_width:
            self.pos_x = self.origin_x - self.patrol_width
            self.direction = 1.0
        self.rect.x = _fl(self.pos_x)
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


# ===================================================================
# NPC
# ===================================================================

class NPC(pygame.sprite.Sprite):
    """Non-combat character that shows dialog when player approaches."""

    def __init__(self, x: int, y: int, name: str,
                 dialog: list[str], color: tuple) -> None:
        super().__init__()
        self.image = pygame.Surface((32, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, (2, 4, 28, 32))
        pygame.draw.circle(self.image, color, (16, 8), 10)
        pygame.draw.circle(self.image, COL_WHITE, (12, 7), 3)
        pygame.draw.circle(self.image, COL_WHITE, (20, 7), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 7), 2)
        pygame.draw.circle(self.image, COL_BLACK, (19, 7), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.name = name
        self.dialog_lines = dialog
        self.current_line = 0
        self.show_dialog = False

    def update(self, dt: float, player) -> None:
        dist = math.hypot(player.rect.centerx - self.rect.centerx,
                          player.rect.centery - self.rect.centery)
        self.show_dialog = dist < NPC_RANGE
