"""Biome-themed parallax backgrounds.

All backgrounds use the same seamless-tile pattern: one surface of exactly
SCREEN_WIDTH, rendered twice per frame at anchor and anchor+width.
Features crossing tile edges use _wrap_polygon for seamless wrapping.
"""

from __future__ import annotations

import math
import random

import pygame

from config import COL_WHITE, SCREEN_HEIGHT, SCREEN_WIDTH


class _BaseBackground:
    """Base class: produces a seamless-tileable surface.

    Uses .convert() for performance on low-end hardware (Pi 1).
    Opaque parallax layer -- no per-pixel alpha lookups.
    """

    def __init__(self) -> None:
        self.w: int = SCREEN_WIDTH
        self.scroll_factor: float = 0.18
        surface = self._build()
        # Convert to display format for faster blits (Pi 1 optimization).
        # Fallback if display not initialized yet.
        try:
            self.surface: pygame.Surface = surface.convert()
        except pygame.error:
            self.surface = surface

    def _build(self) -> pygame.Surface:
        """Subclasses override to paint the biome."""
        raise NotImplementedError

    def _wrap_polygon(self, surf: pygame.Surface, color: tuple,
                     pts: list[tuple[int, int]]) -> None:
        """Draw polygon with horizontal wrap at tile edges."""
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, color, [(x - self.w, y) for x, y in pts])
        pygame.draw.polygon(surf, color, [(x + self.w, y) for x, y in pts])

    def _wrap_rect(self, surf: pygame.Surface, color: tuple,
                   rect: tuple[int, int, int, int]) -> None:
        x, y, w, h = rect
        pygame.draw.rect(surf, color, rect)
        pygame.draw.rect(surf, color, (x - self.w, y, w, h))
        pygame.draw.rect(surf, color, (x + self.w, y, w, h))

    def _sky_gradient(self, surf: pygame.Surface, top: tuple,
                      bottom: tuple) -> None:
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(surf, c, (0, y), (self.w, y))

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:
        parallax_x = camera_x * self.scroll_factor
        offset = -(parallax_x % self.w)
        draw_x = math.floor(offset)
        screen.blit(self.surface, (draw_x, 0))
        screen.blit(self.surface, (draw_x + self.w, 0))


# ---------------------------------------------------------------------------
# Forest (original, for levels 1-3)
# ---------------------------------------------------------------------------

class ForestBackground(_BaseBackground):
    """Original bamboo forest -- blue sky, green mountains, pine trees."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Yoshi's Island: soft peach-tinted sky fading to cream horizon
        self._sky_gradient(surf, (165, 210, 240), (255, 225, 215))
        random.seed(42)
        # Clouds
        for _ in range(5):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(40, 140)
            for _ in range(8):
                pygame.draw.circle(surf, COL_WHITE,
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-8, 5)),
                                   random.randint(18, 30))
        random.seed(101)
        # Back mountains
        for i in range(8):
            x = int(i * self.w / 6) + random.randint(-40, 40)
            peak_h = random.randint(190, 290)
            base_w = random.randint(250, 400)
            top_y = SCREEN_HEIGHT - peak_h
            shade = random.randint(-8, 8)
            self._wrap_polygon(surf, (105 + shade, 130 + shade, 160 + shade),
                               [(x - base_w // 2, SCREEN_HEIGHT),
                                (x, top_y),
                                (x + base_w // 2, SCREEN_HEIGHT)])
            sw = base_w // 7
            self._wrap_polygon(surf, (230, 238, 248),
                               [(x - sw, top_y + 18), (x, top_y),
                                (x + sw, top_y + 18)])
        # Front hills
        for i in range(7):
            x = int(i * self.w / 5) + random.randint(-30, 30)
            peak_h = random.randint(100, 170)
            base_w = random.randint(200, 340)
            top_y = SCREEN_HEIGHT - peak_h
            shade = random.randint(-6, 6)
            self._wrap_polygon(surf, (80 + shade, 110 + shade, 75 + shade),
                               [(x - base_w // 2, SCREEN_HEIGHT),
                                (x, top_y),
                                (x + base_w // 2, SCREEN_HEIGHT)])
        # Yoshi's Island dreamy pastel forest -- 3 depth layers with
        # strong tonal contrast: hazy teal back, soft pink mid, vibrant
        # lime front. Each layer gets warmer and more saturated as it
        # comes toward the camera (atmospheric perspective).

        # BACK LAYER -- dusty teal bamboo, blended into sky haze
        for i in range(30):
            bx = int(i * self.w / 24) + random.randint(-12, 12)
            bh = random.randint(55, 95)
            by_top = SCREEN_HEIGHT - bh - 40
            stalk_c = (130, 170, 155)   # dusty teal
            joint_c = (95, 135, 130)
            for dx in (-self.w, 0, self.w):
                pygame.draw.rect(surf, stalk_c, (bx - 1 + dx, by_top, 2, bh))
                for jy in range(by_top + 12, SCREEN_HEIGHT - 40, 22):
                    pygame.draw.rect(surf, joint_c,
                                     (bx - 2 + dx, jy, 4, 1))
            for dx in (-self.w, 0, self.w):
                pygame.draw.polygon(surf, (150, 190, 175),
                                    [(bx + dx, by_top - 1),
                                     (bx + 5 + dx, by_top + 3),
                                     (bx + dx, by_top + 5)])

        # MID LAYER -- soft-pink cherry blossom trees (Yoshi's Island candy)
        for i in range(5):
            tx = int(i * self.w / 4) + random.randint(-35, 35)
            tree_h = random.randint(85, 115)
            trunk_top = SCREEN_HEIGHT - tree_h - 8
            trunk_w = 6
            trunk_c = (110, 75, 55)  # warm brown, not too dark
            for dx in (-self.w, 0, self.w):
                pygame.draw.rect(surf, trunk_c,
                                 (tx - trunk_w // 2 + dx,
                                  trunk_top + tree_h // 3,
                                  trunk_w, tree_h * 2 // 3))
                pygame.draw.line(surf, trunk_c,
                                 (tx + dx, trunk_top + tree_h // 2),
                                 (tx - 14 + dx, trunk_top + tree_h // 4), 2)
                pygame.draw.line(surf, trunk_c,
                                 (tx + dx, trunk_top + tree_h // 2),
                                 (tx + 14 + dx, trunk_top + tree_h // 4), 2)
            # Chalky pastel blossom cloud (soft pinks + creams)
            cw = random.randint(26, 36)
            for _ in range(10):
                ox = random.randint(-cw, cw)
                oy = random.randint(-cw // 2, cw // 3)
                cr = random.randint(int(cw * 0.55), int(cw * 0.9))
                pc = random.choice([(255, 200, 220), (255, 215, 230),
                                    (250, 185, 210), (255, 225, 235),
                                    (240, 175, 200)])
                self._wrap_polygon(surf, pc, [
                    (tx + ox - cr, trunk_top + tree_h // 4 + oy),
                    (tx + ox, trunk_top + tree_h // 4 + oy - cr // 2),
                    (tx + ox + cr, trunk_top + tree_h // 4 + oy),
                    (tx + ox, trunk_top + tree_h // 4 + oy + cr // 2)])
            # Sprinkle of bright cream highlights
            for _ in range(3):
                ox = random.randint(-cw // 2, cw // 2)
                oy = random.randint(-cw // 3, cw // 4)
                pygame.draw.circle(surf, (255, 245, 225),
                                   (tx + ox, trunk_top + tree_h // 4 + oy),
                                   random.randint(3, 5))

        # FRONT LAYER -- vibrant lime-green bamboo, strong warm highlight
        for i in range(12):
            bx = int(i * self.w / 10) + random.randint(-20, 20)
            bh = random.randint(110, 170)
            by_top = SCREEN_HEIGHT - bh + 8
            stalk_c = (140, 210, 95)      # bright lime (Yoshi green)
            highlight = (195, 240, 130)   # warm cream-lime
            joint_c = (75, 145, 55)
            shadow_c = (90, 165, 65)
            for dx in (-self.w, 0, self.w):
                # Shadow side
                pygame.draw.rect(surf, shadow_c, (bx + 1 + dx, by_top, 3, bh))
                # Main stalk
                pygame.draw.rect(surf, stalk_c, (bx - 3 + dx, by_top, 5, bh))
                # Bright highlight
                pygame.draw.rect(surf, highlight, (bx - 2 + dx, by_top, 2, bh))
                # Joint rings (dark green segments)
                for jy in range(by_top + 14, SCREEN_HEIGHT, 22):
                    pygame.draw.rect(surf, joint_c,
                                     (bx - 4 + dx, jy, 8, 2))
            # Lush leaf clusters at top (2-tone for volume)
            for dx in (-self.w, 0, self.w):
                pygame.draw.polygon(surf, (110, 185, 75),
                                    [(bx + dx, by_top - 6),
                                     (bx + 18 + dx, by_top + 4),
                                     (bx + 2 + dx, by_top + 10)])
                pygame.draw.polygon(surf, (160, 215, 100),
                                    [(bx + dx, by_top - 4),
                                     (bx + 14 + dx, by_top + 2),
                                     (bx + 3 + dx, by_top + 8)])
                pygame.draw.polygon(surf, (100, 170, 65),
                                    [(bx + dx, by_top - 6),
                                     (bx - 18 + dx, by_top + 4),
                                     (bx - 2 + dx, by_top + 10)])
                pygame.draw.polygon(surf, (150, 205, 90),
                                    [(bx + dx, by_top - 4),
                                     (bx - 14 + dx, by_top + 2),
                                     (bx - 3 + dx, by_top + 8)])
        # Ground strip
        for y in range(SCREEN_HEIGHT - 12, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 12)) / 12
            gc = (int(30 + 20 * t), int(85 + 30 * t), int(28 + 15 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf


# ---------------------------------------------------------------------------
# Volcanic (Level 4: Caldera)
# ---------------------------------------------------------------------------

class VolcanicBackground(_BaseBackground):
    """Red-orange sky, dark volcanic peaks, lava glow, ash particles."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (120, 40, 30), (220, 100, 40))
        random.seed(42)
        # Ash clouds (dark red-gray)
        for _ in range(6):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(30, 160)
            for _ in range(7):
                pygame.draw.circle(surf, (100, 50, 40),
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-8, 8) + 3),
                                   random.randint(20, 35))
            for _ in range(5):
                pygame.draw.circle(surf, (60, 30, 25),
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-8, 6)),
                                   random.randint(20, 32))
        random.seed(211)
        # Dark volcanic mountains (almost black)
        for i in range(8):
            x = int(i * self.w / 6) + random.randint(-50, 50)
            peak_h = random.randint(220, 320)
            base_w = random.randint(280, 450)
            top_y = SCREEN_HEIGHT - peak_h
            self._wrap_polygon(surf, (40, 25, 30),
                               [(x - base_w // 2, SCREEN_HEIGHT),
                                (x, top_y),
                                (x + base_w // 2, SCREEN_HEIGHT)])
            # Lava crack
            crack_c = (220, 80, 30)
            pygame.draw.line(surf, crack_c,
                             (x - base_w // 8, SCREEN_HEIGHT - 30),
                             (x, top_y + 40), 2)
            pygame.draw.line(surf, (255, 140, 50),
                             (x - base_w // 8, SCREEN_HEIGHT - 30),
                             (x, top_y + 40), 1)
            # Smoke wisp from peak
            for sy_off in range(0, 40, 5):
                pygame.draw.circle(surf, (80, 50, 45),
                                   (x + random.randint(-5, 5),
                                    top_y - sy_off),
                                   3)
        # Front smaller peaks
        for i in range(6):
            x = int(i * self.w / 5) + random.randint(-40, 40)
            peak_h = random.randint(110, 180)
            base_w = random.randint(220, 360)
            top_y = SCREEN_HEIGHT - peak_h
            self._wrap_polygon(surf, (30, 20, 25),
                               [(x - base_w // 2, SCREEN_HEIGHT),
                                (x, top_y),
                                (x + base_w // 2, SCREEN_HEIGHT)])
        # Lava glow at base
        for y in range(SCREEN_HEIGHT - 20, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 20)) / 20
            gc = (int(180 + 60 * t), int(60 + 40 * t), int(20 + 10 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf


# ---------------------------------------------------------------------------
# Basalt (Level 5: Basalt Columns)
# ---------------------------------------------------------------------------

class BasaltBackground(_BaseBackground):
    """Misty gray sky, hexagonal column silhouettes, sea spray."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (140, 150, 160), (200, 210, 220))
        random.seed(42)
        # Fog clouds
        for _ in range(6):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(40, 200)
            for _ in range(8):
                pygame.draw.circle(surf, (180, 190, 200),
                                   (cx + random.randint(-40, 40),
                                    cy + random.randint(-10, 10)),
                                   random.randint(25, 45))
        random.seed(311)
        # Distant hex column cliffs (silhouette)
        for i in range(10):
            x = int(i * self.w / 7) + random.randint(-30, 30)
            col_h = random.randint(140, 250)
            col_w = random.randint(30, 50)
            shade = random.randint(-10, 10)
            c = (70 + shade, 80 + shade, 95 + shade)
            for dx in (-self.w, 0, self.w):
                pygame.draw.rect(surf, c,
                                 (x - col_w // 2 + dx, SCREEN_HEIGHT - col_h,
                                  col_w, col_h))
            # Hex pattern lines on top
            for ty in range(SCREEN_HEIGHT - col_h, SCREEN_HEIGHT, 24):
                pygame.draw.line(surf, (50, 60, 75),
                                 (x - col_w // 2, ty),
                                 (x + col_w // 2, ty), 1)
        # Front cliffs (darker)
        for i in range(6):
            x = int(i * self.w / 4) + random.randint(-40, 40)
            col_h = random.randint(80, 140)
            col_w = random.randint(60, 100)
            c = (45, 50, 60)
            for dx in (-self.w, 0, self.w):
                pygame.draw.rect(surf, c,
                                 (x - col_w // 2 + dx, SCREEN_HEIGHT - col_h,
                                  col_w, col_h))
        # Sea spray at very bottom
        for y in range(SCREEN_HEIGHT - 10, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 10)) / 10
            gc = (int(70 + 30 * t), int(80 + 30 * t), int(95 + 20 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf


# ---------------------------------------------------------------------------
# Desert (Level 6: Arid Rift)
# ---------------------------------------------------------------------------

class DesertBackground(_BaseBackground):
    """Warm orange sky, sand dunes, distant mesas, heat haze."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (255, 180, 100), (255, 230, 160))
        random.seed(42)
        # Sun
        pygame.draw.circle(surf, (255, 220, 120), (self.w // 2, 90), 50)
        pygame.draw.circle(surf, (255, 240, 160), (self.w // 2, 90), 35)
        random.seed(411)
        # Distant mesas (dark red-orange)
        for i in range(7):
            x = int(i * self.w / 5) + random.randint(-50, 50)
            mesa_h = random.randint(120, 180)
            mesa_w = random.randint(200, 350)
            top_y = SCREEN_HEIGHT - mesa_h
            c = (150 + random.randint(-15, 15),
                 85 + random.randint(-10, 10),
                 50 + random.randint(-10, 10))
            # Flat-top mesa
            for dx in (-self.w, 0, self.w):
                pygame.draw.polygon(surf, c, [
                    (x - mesa_w // 2 + dx, SCREEN_HEIGHT),
                    (x - mesa_w // 3 + dx, top_y),
                    (x + mesa_w // 3 + dx, top_y),
                    (x + mesa_w // 2 + dx, SCREEN_HEIGHT)])
            # Top stripe
            pygame.draw.line(surf, (180, 100, 60),
                             (x - mesa_w // 3, top_y),
                             (x + mesa_w // 3, top_y), 2)
        # Foreground dunes
        for i in range(5):
            x = int(i * self.w / 3) + random.randint(-60, 60)
            dune_h = random.randint(60, 120)
            dune_w = random.randint(300, 500)
            top_y = SCREEN_HEIGHT - dune_h
            c = (194 + random.randint(-10, 10), 160 + random.randint(-10, 10),
                 100 + random.randint(-10, 10))
            # Smooth rolling dune
            pts = [(x - dune_w // 2, SCREEN_HEIGHT)]
            for px_off in range(-dune_w // 2, dune_w // 2, 20):
                py = top_y + int(20 * math.sin(px_off * 0.02))
                pts.append((x + px_off, py))
            pts.append((x + dune_w // 2, SCREEN_HEIGHT))
            self._wrap_polygon(surf, c, pts)
        # Sand strip
        for y in range(SCREEN_HEIGHT - 12, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 12)) / 12
            gc = (int(200 + 20 * t), int(170 + 15 * t), int(110 + 10 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf


# ---------------------------------------------------------------------------
# Cave (Level 7: Karst Caves) -- near black, bioluminescent specks
# ---------------------------------------------------------------------------

class CaveBackground(_BaseBackground):
    """Dark cave with stalactites + stalagmites + glowworm specks."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Deep dark gradient
        self._sky_gradient(surf, (10, 12, 20), (25, 20, 35))
        random.seed(42)
        # Stalactites from ceiling
        for i in range(15):
            x = int(i * self.w / 12) + random.randint(-20, 20)
            s_h = random.randint(40, 100)
            s_w = random.randint(15, 30)
            c = (40, 35, 50)
            self._wrap_polygon(surf, c, [
                (x - s_w // 2, 0), (x + s_w // 2, 0), (x, s_h)])
        # Bioluminescent specks (tiny cyan dots)
        random.seed(77)
        for _ in range(80):
            sx = random.randint(0, self.w)
            sy = random.randint(50, SCREEN_HEIGHT - 50)
            glow_c = random.choice([(100, 220, 255), (200, 255, 180), (255, 200, 120)])
            pygame.draw.circle(surf, glow_c, (sx, sy), 1)
        # Distant stalagmites from floor
        random.seed(511)
        for i in range(12):
            x = int(i * self.w / 9) + random.randint(-30, 30)
            s_h = random.randint(60, 130)
            s_w = random.randint(25, 45)
            c = (30, 28, 40)
            self._wrap_polygon(surf, c, [
                (x - s_w // 2, SCREEN_HEIGHT),
                (x, SCREEN_HEIGHT - s_h),
                (x + s_w // 2, SCREEN_HEIGHT)])
        random.seed()
        return surf


# ---------------------------------------------------------------------------
# Salt Flats (Level 8) -- white/blue sky, distant Andes, reflective ground
# ---------------------------------------------------------------------------

class SaltFlatsBackground(_BaseBackground):
    """Pale sky, snowy Andes silhouettes, mirror-flat salt surface."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (180, 220, 250), (220, 240, 255))
        random.seed(42)
        # Wispy high clouds
        for _ in range(4):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(30, 100)
            for _ in range(5):
                pygame.draw.ellipse(surf, (240, 245, 255),
                                    (cx + random.randint(-40, 40),
                                     cy + random.randint(-5, 5),
                                     60, 10))
        # Distant snowy Andes
        random.seed(611)
        for i in range(9):
            x = int(i * self.w / 6) + random.randint(-50, 50)
            peak_h = random.randint(150, 240)
            base_w = random.randint(200, 350)
            top_y = SCREEN_HEIGHT - peak_h - 20
            # Base (purple-gray)
            c = (120, 130, 150)
            self._wrap_polygon(surf, c, [
                (x - base_w // 2, SCREEN_HEIGHT - 20),
                (x, top_y),
                (x + base_w // 2, SCREEN_HEIGHT - 20)])
            # Snow cap (large, takes upper half)
            sw = base_w // 2
            self._wrap_polygon(surf, (245, 248, 255), [
                (x - sw // 2, top_y + 40), (x, top_y),
                (x + sw // 2, top_y + 40)])
        # Reflective salt surface (horizon band)
        for y in range(SCREEN_HEIGHT - 20, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 20)) / 20
            gc = (int(220 + 10 * t), int(230 + 10 * t), int(245 + 10 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_BIOME_MAP = {
    "forest": ForestBackground,
    "volcanic": VolcanicBackground,
    "basalt": BasaltBackground,
    "desert": DesertBackground,
    "cave": CaveBackground,
    "salt": SaltFlatsBackground,
}


class BiomeBackground:
    """Factory that returns the correct background for each biome."""

    def __init__(self, biome: str = "forest") -> None:
        cls = _BIOME_MAP.get(biome, ForestBackground)
        self.bg = cls()

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:
        self.bg.draw(screen, camera_x)
