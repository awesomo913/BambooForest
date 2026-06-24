"""Camera, particle system, parallax background, and screen shake."""

from __future__ import annotations

import math
import random

import pygame

from config import (
    COL_PLAT_DIRT, COL_SKY, COL_WHITE, DUST_LIFE, LEAF_COUNT,
    SCREEN_HEIGHT, SCREEN_WIDTH, SHAKE_DURATION, SHAKE_INTENSITY, SPARKLE_LIFE,
)


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

class Camera:
    """Smooth-follow camera. Logic state is float, render state is int.

    offset_x / offset_y: float -- smooth lerp tracking (logic camera).
    render_x / render_y: int   -- math.floor of offset (render camera).

    All sprites and tiles are drawn relative to render_x/render_y,
    which locks everything to the same integer pixel grid.
    """

    def __init__(self, world_width: int, world_height: int) -> None:
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0
        self.render_x: int = 0
        self.render_y: int = 0
        self.world_width = world_width
        self.world_height = world_height

    def update(self, target: pygame.sprite.Sprite, dt: float) -> None:
        # Direct lock for no jitter + tiny velocity lead for juicy anticipation.
        # Lead makes camera peek ahead when running, feels responsive without laggy lerp.
        goal_x = -target.rect.centerx + SCREEN_WIDTH // 2
        goal_y = -target.rect.centery + SCREEN_HEIGHT // 2
        # Small forward lead (tuned low so platforming precision stays perfect)
        vx = getattr(target, "velocity_x", 0.0)
        lead = vx * 0.11
        goal_x -= lead
        self.offset_x = float(max(-(self.world_width - SCREEN_WIDTH), min(0, goal_x)))
        self.offset_y = float(max(-(self.world_height - SCREEN_HEIGHT), min(0, goal_y)))
        self.render_x = math.floor(self.offset_x)
        self.render_y = math.floor(self.offset_y)

    def apply(self, entity: pygame.sprite.Sprite) -> pygame.Rect:
        return entity.rect.move(math.floor(self.offset_x), math.floor(self.offset_y))

    def apply_pos(self, x: float, y: float) -> tuple[float, float]:
        return (x + self.offset_x, y + self.offset_y)

    def get_visible_rect(self) -> pygame.Rect:
        return pygame.Rect(-self.render_x, -self.render_y, SCREEN_WIDTH, SCREEN_HEIGHT)


# ---------------------------------------------------------------------------
# Screen Shake
# ---------------------------------------------------------------------------

class ScreenShake:
    def __init__(self) -> None:
        self.timer: float = 0.0
        self.intensity: int = 0
        self.scale: float = 1.0

    def set_scale(self, v: float) -> None:
        self.scale = max(0.0, min(2.0, float(v)))

    def trigger(self, intensity: int = SHAKE_INTENSITY,
                duration: float = SHAKE_DURATION) -> None:
        self.timer = duration
        self.intensity = intensity

    def update(self, dt: float) -> tuple[int, int]:
        if self.timer > 0:
            self.timer -= dt
            i = int(self.intensity * self.scale)
            return (random.randint(-i, i), random.randint(-i, i))
        return (0, 0)

    def tick(self, dt: float) -> None:
        """Advance timer only -- no RNG, no return. Use in update loop."""
        if self.timer > 0:
            self.timer -= dt

    def get_offset(self) -> tuple[int, int]:
        """Sample current shake offset. Use in draw loop."""
        if self.timer > 0:
            i = int(self.intensity * self.scale)
            return (random.randint(-i, i), random.randint(-i, i))
        return (0, 0)


# ---------------------------------------------------------------------------
# Particle System
# ---------------------------------------------------------------------------

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color",
                 "size", "shape", "gravity")

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 life: float, color: tuple, size: float,
                 shape: str = "circle", gravity: bool = False) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
        self.shape = shape
        self.gravity = gravity


class ParticleSystem:
    def __init__(self) -> None:
        self.particles: list[Particle] = []
        self.intensity: float = 1.0
        self.reduced_motion: bool = False

    def set_intensity(self, v: float) -> None:
        """Accessibility: scale emitted counts (0.0 = none, 1.0 = normal, 2.0 = lots)."""
        self.intensity = max(0.0, min(2.0, float(v)))

    def set_reduced_motion(self, v: bool) -> None:
        """Accessibility: when true, skip some sparkles (e.g. decorative/ambient)."""
        self.reduced_motion = bool(v)

    def _count(self, n: int) -> int:
        if self.intensity <= 0.01:
            return 0
        return max(0, int(n * self.intensity))

    def update(self, dt: float) -> None:
        alive: list[Particle] = []
        for p in self.particles:
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.gravity:
                p.vy += 400 * dt
            p.life -= dt
            if p.life > 0:
                alive.append(p)
        self.particles = alive

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        for p in self.particles:
            sx, sy = camera.apply_pos(p.x, p.y)
            if sx < -20 or sx > SCREEN_WIDTH + 20 or sy < -20 or sy > SCREEN_HEIGHT + 20:
                continue
            alpha = max(0, min(255, int(255 * (p.life / p.max_life))))
            r, g, b = p.color
            color = (min(255, r), min(255, g), min(255, b))
            sz = max(1, int(p.size * (p.life / p.max_life)))
            if p.shape == "circle":
                if alpha > 200:
                    pygame.draw.circle(screen, color, (int(sx), int(sy)), sz)
                else:
                    s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*color, alpha), (sz, sz), sz)
                    screen.blit(s, (int(sx) - sz, int(sy) - sz))
            elif p.shape == "leaf":
                s = pygame.Surface((sz + 2, sz + 2), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (*color, alpha), (0, 0, sz + 2, max(1, sz // 2)))
                screen.blit(s, (int(sx), int(sy)))
            elif p.shape == "rect":
                if alpha > 200:
                    pygame.draw.rect(screen, color, (int(sx), int(sy), sz, sz))
                else:
                    s = pygame.Surface((sz, sz), pygame.SRCALPHA)
                    s.fill((*color, alpha))
                    screen.blit(s, (int(sx), int(sy)))

    def emit_sparkle(self, x: float, y: float, count: int = 8) -> None:
        n = self._count(count)
        if self.reduced_motion:
            n = max(0, n // 2)  # simple reduced motion: skip some sparkles
        for _ in range(n):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(60, 180)
            self.particles.append(Particle(
                x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                SPARKLE_LIFE + random.uniform(-0.1, 0.1),
                (255, 215 + random.randint(-20, 20), random.randint(0, 80)),
                random.uniform(2, 5), "circle",
            ))

    def emit_dust(self, x: float, y: float, count: int = 5) -> None:
        for _ in range(self._count(count)):
            self.particles.append(Particle(
                x + random.uniform(-10, 10), y,
                random.uniform(-40, 40), random.uniform(-80, -20),
                DUST_LIFE + random.uniform(0, 0.1),
                (COL_PLAT_DIRT[0] + random.randint(-15, 15),
                 COL_PLAT_DIRT[1] + random.randint(-10, 10),
                 COL_PLAT_DIRT[2] + random.randint(-5, 5)),
                random.uniform(2, 4), "circle", gravity=True,
            ))

    def emit_dash_trail(self, x: float, y: float, direction: float = -1.0) -> None:
        """Speed lines / afterimage particles for dash. Small, fast, short life. Richer for juice."""
        for _ in range(2):
            # Horizontal speed lines, slight vertical scatter
            speed = random.uniform(180, 320)
            vx = direction * speed + random.uniform(-30, 30)
            vy = random.uniform(-40, 40)
            life = random.uniform(0.08, 0.16)
            # Cool blue-white streak color
            color = (180 + random.randint(0, 40),
                     200 + random.randint(0, 55),
                     255)
            self.particles.append(Particle(
                x, y, vx, vy, life, color,
                random.uniform(1.5, 3.0), "rect", gravity=False,
            ))
            # Mix in tiny forward bamboo leaf flecks for theme
            if random.random() < 0.6:
                self.particles.append(Particle(
                    x + random.uniform(-2, 2), y + random.uniform(-4, 4),
                    direction * random.uniform(140, 220), random.uniform(-30, 30),
                    random.uniform(0.09, 0.18),
                    (70, 160, 55),
                    random.uniform(2, 3.5), "leaf", gravity=False,
                ))

    def emit_glide_wisp(self, x: float, y: float) -> None:
        """Soft rising wisp while gliding. Very gentle, almost decorative."""
        # Slow upward drift, tiny horizontal wander + occasional leaf for forest feel
        vx = random.uniform(-8, 8)
        vy = random.uniform(-35, -15)
        life = random.uniform(0.25, 0.45)
        # Pale cyan/white soft
        color = (200 + random.randint(0, 55),
                 230 + random.randint(0, 25),
                 255)
        self.particles.append(Particle(
            x, y, vx, vy, life, color,
            random.uniform(1.0, 2.2), "circle", gravity=False,
        ))
        if random.random() < 0.35:
            # light leaf accent
            self.particles.append(Particle(
                x + random.uniform(-3, 3), y,
                random.uniform(-12, 12), random.uniform(-28, -12),
                random.uniform(0.35, 0.65),
                random.choice([(60, 150, 50), (80, 170, 60)]),
                random.uniform(2.5, 4.5), "leaf", gravity=False,
            ))

    def emit_graft_leaves(self, x: float, y: float, count: int = 10) -> None:
        """Leaf burst + sparkle when grafts are applied (Grove meta juice)."""
        n = self._count(count)
        for _ in range(n):
            angle = random.uniform(-1.0, 1.0)
            speed = random.uniform(35, 95)
            vx = math.sin(angle) * speed
            vy = -abs(math.cos(angle) * speed) * 0.9 - random.uniform(20, 50)
            greens = [(55, 145, 45), (75, 165, 55), (45, 125, 35), (90, 175, 70)]
            self.particles.append(Particle(
                x + random.uniform(-4, 4), y + random.uniform(-2, 2),
                vx, vy,
                random.uniform(0.55, 1.05),
                random.choice(greens),
                random.uniform(3, 6), "leaf", gravity=True,
            ))
        # Bonus sparkles for "applied" pop
        for _ in range(max(2, n // 3)):
            self.emit_sparkle(x + random.uniform(-6, 6), y - 4, 1)

    def emit_ice_trail(self, x: float, y: float, direction: float = -1.0) -> None:
        """Frosty motes / speed lines for ice sliding and ice magic. Cold blue-white."""
        for _ in range(2):
            vx = direction * random.uniform(90, 180) + random.uniform(-20, 20)
            vy = random.uniform(-25, 35)
            life = random.uniform(0.18, 0.32)
            c = (170 + random.randint(0, 50), 210 + random.randint(0, 40), 255)
            self.particles.append(Particle(
                x + random.uniform(-3, 3), y + random.uniform(-2, 2),
                vx, vy, life, c,
                random.uniform(1.2, 2.8), "circle", gravity=False,
            ))

    def emit_damage(self, x: float, y: float, count: int = 6) -> None:
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            self.particles.append(Particle(
                x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                0.3, (255, random.randint(30, 80), random.randint(0, 30)),
                random.uniform(2, 5), "circle", gravity=True,
            ))

    def emit_death(self, x: float, y: float, count: int = 15) -> None:
        for _ in range(self._count(count)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            self.particles.append(Particle(
                x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                random.uniform(0.3, 0.7),
                (255, random.randint(50, 150), random.randint(0, 50)),
                random.uniform(3, 7), "circle", gravity=True,
            ))

    def emit_ambient_leaves(self, visible_rect: pygame.Rect) -> None:
        target = self._count(LEAF_COUNT)
        leaf_count = sum(1 for p in self.particles if p.shape == "leaf")
        while leaf_count < target:
            x = visible_rect.x + random.uniform(0, visible_rect.width)
            y = visible_rect.y + random.uniform(-40, visible_rect.height * 0.4)
            greens = [(60, 140, 40), (40, 120, 30), (80, 160, 50), (50, 130, 20),
                      (70, 150, 35), (90, 170, 55)]
            self.particles.append(Particle(
                x, y,
                random.uniform(-20, 20), random.uniform(15, 45),
                random.uniform(4, 8),
                random.choice(greens),
                random.uniform(3, 6), "leaf",
            ))
            leaf_count += 1

    def emit_geyser_burst(self, x: float, y: float, count: int = 12) -> None:
        """Strong upward volcanic launch juice for geyser rides."""
        for _ in range(self._count(count)):
            angle = random.uniform(-0.6, 0.6)
            speed = random.uniform(120, 320)
            vx = math.sin(angle) * speed * 0.3
            vy = -abs(math.cos(angle) * speed)
            self.particles.append(Particle(
                x + random.uniform(-8, 8), y,
                vx, vy,
                random.uniform(0.35, 0.65),
                (255, 160 + random.randint(0, 60), 40),
                random.uniform(2, 5), "circle", gravity=False,
            ))

    def emit_updraft_lift(self, x: float, y: float, count: int = 3) -> None:
        """Gentle rising bubbles/leaves for thermal columns."""
        for _ in range(count):
            vx = random.uniform(-25, 25)
            vy = random.uniform(-140, -60)
            self.particles.append(Particle(
                x + random.uniform(-18, 18), y + random.uniform(0, 30),
                vx, vy,
                random.uniform(0.5, 1.0),
                (255, 230, 160),
                random.uniform(2, 4), "circle", gravity=False,
            ))

    def emit_wind_drift(self, x: float, y: float, direction: float, count: int = 4) -> None:
        """Horizontal sand/dust for wind zones."""
        for _ in range(count):
            vx = direction * random.uniform(80, 160)
            vy = random.uniform(-30, 30)
            self.particles.append(Particle(
                x + random.uniform(-10, 10), y + random.uniform(-40, 40),
                vx, vy,
                random.uniform(0.25, 0.55),
                (210, 180, 130),
                random.uniform(1.5, 3.5), "circle", gravity=True,
            ))

    def emit_gravity_motes(self, x: float, y: float, count: int = 5) -> None:
        """Subtle floating particles inside altered gravity zones."""
        for _ in range(count):
            vx = random.uniform(-35, 35)
            vy = random.uniform(-60, 60)
            self.particles.append(Particle(
                x + random.uniform(-20, 20), y + random.uniform(-15, 15),
                vx, vy,
                random.uniform(0.6, 1.2),
                (200, 160, 255),
                random.uniform(1, 3), "circle", gravity=False,
            ))

    def emit_mushroom_puff(self, x: float, y: float, count: int = 8) -> None:
        """Bouncy puff when mushroom launches player."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(40, 110)
            self.particles.append(Particle(
                x, y,
                math.cos(angle) * speed, math.sin(angle) * speed - 60,
                random.uniform(0.3, 0.55),
                (220, 140, 200),
                random.uniform(2, 4), "circle", gravity=True,
            ))
