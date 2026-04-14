"""All sprite classes and procedural pixel-art generators."""

from __future__ import annotations

import math
import random
from math import floor as _fl

import pygame

from config import (
    BOSS_CHARGE_SPEED, BOSS_HP, BOSS_IDLE_SEC, BOSS_SIZE,
    BOSS_STUN_SEC, COL_BAMBOO, COL_BAMBOO_JOINT, COL_BLACK,
    COL_HEAL_PINK, COL_HEAL_RED, COL_PANDA_BLACK, COL_PANDA_WHITE,
    COL_PLAT_DIRT, COL_PLAT_GRASS, COL_WHITE, COMBO_MULTIPLIERS,
    COMBO_WINDOW, BAMBOO_SCORE, ENEMY_CHASE_RANGE, ENEMY_CHASE_SPEED,
    ENEMY_CHASE_Y_RANGE, ENEMY_PATROL_SPEED, ENEMY_STOMP_BOUNCE,
    FLYING_ENEMY_AMP, FLYING_ENEMY_FREQ, GRAVITY, MOVING_PLAT_SPEED,
    PLAYER_DAMAGE, PLAYER_INVINCIBLE_SEC, PLAYER_JUMP,
    PLAYER_MAX_HP, PLAYER_SIZE, PLAYER_SPEED, TERMINAL_VELOCITY,
    HEAL_AMOUNT, SAFE_ZONE_WIDTH, SLIME_BOUNCE_SPEED, SLIME_HOP_POWER,
    FLOOR_Y,
)

# ---------------------------------------------------------------------------
# Procedural art generators
# ---------------------------------------------------------------------------

def generate_panda_frames() -> dict[str, list[pygame.Surface]]:
    """Cleaner panda with rounder proportions and visible detail."""
    w, h = PLAYER_SIZE  # 36x44

    def _draw_panda(surf: pygame.Surface, body_dy: int = 0,
                    arm_l: tuple[int, int, int, int] = (2, 20, 7, 12),
                    arm_r: tuple[int, int, int, int] = (27, 20, 7, 12),
                    leg_l: tuple[int, int, int, int] = (8, 35, 9, 9),
                    leg_r: tuple[int, int, int, int] = (19, 35, 9, 9)) -> None:
        dy = body_dy
        # Shadow under body
        pygame.draw.ellipse(surf, (200, 200, 190), (7, 15 + dy, 22, 22))
        # Body (round white torso)
        pygame.draw.ellipse(surf, COL_PANDA_WHITE, (6, 14 + dy, 24, 24))
        # Belly patch
        pygame.draw.ellipse(surf, (220, 220, 215), (11, 18 + dy, 14, 14))
        # Arms (rounded rects)
        for ax, ay, aw, ah in (arm_l, arm_r):
            pygame.draw.rect(surf, COL_PANDA_BLACK, (ax, ay + dy, aw, ah),
                             border_radius=3)
        # Legs (rounded rects)
        for lx, ly, lw, lh in (leg_l, leg_r):
            pygame.draw.rect(surf, COL_PANDA_BLACK, (lx, ly + dy, lw, lh),
                             border_radius=4)
        # Head
        pygame.draw.circle(surf, COL_PANDA_WHITE, (w // 2, 12), 11)
        # Ears (outer black + inner pink)
        for ex in (7, 29):
            pygame.draw.circle(surf, COL_PANDA_BLACK, (ex, 3), 5)
            pygame.draw.circle(surf, (180, 130, 130), (ex, 3), 2)
        # Eye patches (smooth ellipses)
        pygame.draw.ellipse(surf, COL_PANDA_BLACK, (10, 7, 8, 7))
        pygame.draw.ellipse(surf, COL_PANDA_BLACK, (18, 7, 8, 7))
        # Eyes (white with black pupil and highlight)
        for ex, px in ((14, 15), (22, 21)):
            pygame.draw.circle(surf, COL_WHITE, (ex, 10), 3)
            pygame.draw.circle(surf, COL_BLACK, (px, 10), 2)
            pygame.draw.circle(surf, COL_WHITE, (px - 1, 9), 1)
        # Nose
        pygame.draw.ellipse(surf, (60, 40, 40), (16, 14, 5, 3))
        # Mouth
        pygame.draw.arc(surf, COL_BLACK, (15, 15, 7, 4), 3.14, 6.28, 1)

    frames: dict[str, list[pygame.Surface]] = {}

    # Idle: gentle breathing bob
    for dy in (0, 1):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        _draw_panda(s, body_dy=dy)
        frames.setdefault("idle", []).append(s)

    # Run: alternating limb positions
    run_data = [
        ((0, 18, 7, 12), (29, 22, 7, 12), (6, 33, 9, 9), (21, 37, 9, 9)),
        ((2, 20, 7, 12), (27, 20, 7, 12), (8, 35, 9, 9), (19, 35, 9, 9)),
        ((29, 18, 7, 12), (0, 22, 7, 12), (21, 33, 9, 9), (6, 37, 9, 9)),
        ((2, 20, 7, 12), (27, 20, 7, 12), (8, 35, 9, 9), (19, 35, 9, 9)),
    ]
    for al, ar, ll, lr in run_data:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        _draw_panda(s, arm_l=al, arm_r=ar, leg_l=ll, leg_r=lr)
        frames.setdefault("run", []).append(s)

    # Jump: arms up, legs tucked
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    _draw_panda(s, body_dy=-2,
                arm_l=(0, 10, 7, 12), arm_r=(29, 10, 7, 12),
                leg_l=(10, 32, 8, 8), leg_r=(18, 32, 8, 8))
    frames["jump"] = [s]

    # Fall: arms spread, legs down
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    _draw_panda(s, body_dy=1,
                arm_l=(-1, 16, 8, 12), arm_r=(29, 16, 8, 12),
                leg_l=(9, 38, 8, 6), leg_r=(19, 38, 8, 6))
    frames["fall"] = [s]

    return frames


def generate_bamboo_surface() -> pygame.Surface:
    """20x55 bamboo stalk with joints and leaves."""
    surf = pygame.Surface((20, 55), pygame.SRCALPHA)
    pygame.draw.rect(surf, COL_BAMBOO, (7, 0, 6, 55))
    # Gradient stripe on stalk
    pygame.draw.rect(surf, (90, 170, 20), (9, 0, 2, 55))
    for jy in (12, 27, 42):
        pygame.draw.rect(surf, COL_BAMBOO_JOINT, (6, jy, 8, 3))
    # Leaves
    pygame.draw.polygon(surf, (50, 160, 30), [(10, 0), (19, 6), (10, 8)])
    pygame.draw.polygon(surf, (40, 140, 20), [(10, 0), (1, 6), (10, 8)])
    return surf


def generate_heal_surface() -> pygame.Surface:
    """25x25 heart shape."""
    surf = pygame.Surface((25, 25), pygame.SRCALPHA)
    pygame.draw.circle(surf, COL_HEAL_RED, (8, 8), 6)
    pygame.draw.circle(surf, COL_HEAL_RED, (17, 8), 6)
    pygame.draw.polygon(surf, COL_HEAL_RED, [(2, 10), (12, 23), (23, 10)])
    pygame.draw.circle(surf, COL_HEAL_PINK, (7, 6), 2)
    return surf


def generate_platform_tile(width: int, height: int) -> pygame.Surface:
    """Clean platform with grass top, dirt body, and stone edge."""
    surf = pygame.Surface((width, height))
    # Dirt gradient (darker at bottom)
    for y in range(height):
        t = y / max(1, height)
        c = (max(0, int(COL_PLAT_DIRT[0] - 15 * t)),
             max(0, int(COL_PLAT_DIRT[1] - 10 * t)),
             max(0, int(COL_PLAT_DIRT[2] - 8 * t)))
        pygame.draw.line(surf, c, (0, y), (width, y))
    # Stone edge on sides
    edge_c = (85, 60, 35)
    pygame.draw.rect(surf, edge_c, (0, 0, 2, height))
    pygame.draw.rect(surf, edge_c, (width - 2, 0, 2, height))
    # Grass top (thick, with blade shapes)
    grass_h = min(6, height)
    pygame.draw.rect(surf, COL_PLAT_GRASS, (0, 0, width, grass_h))
    dark_grass = (25, 120, 25)
    pygame.draw.rect(surf, dark_grass, (0, grass_h - 1, width, 1))
    # Grass blades sticking up
    for x in range(0, width - 1, 3):
        bh = random.randint(2, 6)
        shade = random.randint(-10, 20)
        gc = (min(255, COL_PLAT_GRASS[0] + shade),
              min(255, COL_PLAT_GRASS[1] + shade),
              min(255, COL_PLAT_GRASS[2] + shade))
        pygame.draw.line(surf, gc, (x, grass_h), (x + random.randint(-1, 1), grass_h - bh), 1)
    # Subtle dirt specks
    for _ in range(width * height // 40):
        nx = random.randint(2, width - 3)
        ny = random.randint(grass_h + 1, max(grass_h + 1, height - 1))
        shade = random.randint(-10, 10)
        c = (max(0, min(255, COL_PLAT_DIRT[0] + shade)),
             max(0, min(255, COL_PLAT_DIRT[1] + shade)),
             max(0, min(255, COL_PLAT_DIRT[2] + shade)))
        surf.set_at((nx, ny), c)
    return surf


def generate_safe_zone(height: int) -> pygame.Surface:
    """Natural forest clearing that the panda runs into to complete the level."""
    w = SAFE_ZONE_WIDTH
    surf = pygame.Surface((w, height), pygame.SRCALPHA)
    ground_y = height - 18

    # Ground: gradient transition from dirt to lush green
    for gy in range(ground_y, height):
        t = (gy - ground_y) / max(1, height - ground_y)
        r = int(80 - 40 * t)
        g = int(140 + 50 * t)
        b = int(50 - 20 * t)
        pygame.draw.line(surf, (r, g, b), (0, gy), (w, gy))

    # Clearing path in center (lighter earthy tone)
    path_w = 60
    path_x = w // 2 - path_w // 2
    for gy in range(ground_y, height):
        pygame.draw.rect(surf, (110, 160, 80), (path_x, gy, path_w, 1))

    # Dense grass blades along ground
    for gx in range(0, w, 3):
        gh = random.randint(6, 14)
        shade = random.randint(-15, 15)
        gc = (40 + shade, 140 + shade, 35 + shade)
        pygame.draw.line(surf, gc, (gx, ground_y),
                         (gx + random.randint(-2, 2), ground_y - gh), 1)

    # Trees: varied heights, proper trunks + layered canopy
    tree_defs = [(30, 0.9), (w // 2 - 50, 0.7), (w // 2 + 40, 0.75), (w - 45, 0.85)]
    for tx, scale in tree_defs:
        th = int(height * scale * 0.6)
        trunk_w = int(8 + 6 * scale)
        trunk_h = int(th * 0.45)
        trunk_top = ground_y - th

        # Trunk
        tc = (85 + random.randint(-10, 10), 58 + random.randint(-8, 8),
              32 + random.randint(-5, 5))
        pygame.draw.rect(surf, tc,
                         (tx - trunk_w // 2, trunk_top + th - trunk_h,
                          trunk_w, trunk_h), border_radius=2)
        # Bark lines
        for by in range(trunk_top + th - trunk_h, ground_y, 8):
            pygame.draw.line(surf, (tc[0] - 15, tc[1] - 12, tc[2] - 8),
                             (tx - trunk_w // 4, by), (tx + trunk_w // 4, by + 4), 1)

        # Canopy: 3 layered triangles (pine) or circles (oak), alternating
        canopy_c = (35 + random.randint(-8, 12), 120 + random.randint(-15, 20),
                    35 + random.randint(-8, 12))
        cw = int(22 + 18 * scale)
        if random.random() > 0.5:
            # Pine tree (triangles)
            for li, (ly_f, lw_f) in enumerate([(0.6, 1.0), (0.38, 0.8), (0.16, 0.6)]):
                ly = trunk_top + int(th * ly_f)
                lw = int(cw * lw_f)
                s = li * 10
                lc = (min(255, canopy_c[0] + s), min(255, canopy_c[1] + s),
                      min(255, canopy_c[2] + s))
                pygame.draw.polygon(surf, lc, [
                    (tx - lw, ly), (tx, trunk_top + int(th * 0.1 * (li + 1))),
                    (tx + lw, ly)])
        else:
            # Oak tree (overlapping circles)
            for _ in range(6):
                ox = random.randint(-cw, cw)
                oy = random.randint(-cw // 2, cw // 3)
                cr = random.randint(int(cw * 0.5), int(cw * 0.8))
                s = random.randint(-8, 8)
                lc = (min(255, canopy_c[0] + s), min(255, canopy_c[1] + s),
                      min(255, canopy_c[2] + s))
                pygame.draw.circle(surf, lc, (tx + ox, trunk_top + int(th * 0.3) + oy), cr)

    # Flower clusters (groups of 2-3 near each other)
    flower_colors = [(255, 90, 90), (255, 210, 60), (220, 120, 255),
                     (255, 160, 200), (120, 210, 255)]
    for _ in range(5):
        cluster_x = random.randint(40, w - 40)
        cluster_y = ground_y
        for fi in range(random.randint(2, 3)):
            fx = cluster_x + random.randint(-15, 15)
            fy = cluster_y - random.randint(4, 12)
            fc = random.choice(flower_colors)
            pygame.draw.line(surf, (40, 120, 35), (fx, cluster_y), (fx, fy), 1)
            for angle in range(0, 360, 72):
                px = fx + int(3 * math.cos(math.radians(angle)))
                py = fy + int(3 * math.sin(math.radians(angle)))
                pygame.draw.circle(surf, fc, (px, py), 2)
            pygame.draw.circle(surf, (255, 220, 50), (fx, fy), 1)

    # Sunbeam rays (wide diagonal golden shafts)
    for _ in range(4):
        rx = random.randint(20, w - 20)
        beam = pygame.Surface((18, height), pygame.SRCALPHA)
        for by in range(height):
            alpha = max(0, int(30 * (1 - by / height)))
            pygame.draw.line(beam, (255, 245, 180, alpha), (0, by), (18, by))
        surf.blit(beam, (rx + random.randint(-10, 10), 0))

    # Butterflies
    bf_colors = [(255, 140, 200), (140, 200, 255), (255, 255, 140),
                 (200, 255, 180), (255, 180, 120)]
    for _ in range(6):
        bx = random.randint(30, w - 30)
        by = random.randint(30, ground_y - 20)
        bc = random.choice(bf_colors)
        pygame.draw.ellipse(surf, bc, (bx - 5, by - 3, 6, 7))
        pygame.draw.ellipse(surf, bc, (bx + 1, by - 3, 6, 7))
        pygame.draw.line(surf, (60, 40, 30), (bx, by - 3), (bx, by + 4), 1)

    # Small ferns along ground edges
    for fx in range(10, w - 10, 20):
        fh = random.randint(6, 12)
        fc = (30 + random.randint(-5, 10), 110 + random.randint(-10, 15),
              30 + random.randint(-5, 5))
        # Two frond curves
        for side in (-1, 1):
            pts = [(fx, ground_y), (fx + side * fh // 2, ground_y - fh),
                   (fx + side * fh, ground_y - fh // 2)]
            pygame.draw.lines(surf, fc, False, pts, 1)

    return surf


def generate_grass_tuft() -> pygame.Surface:
    """Small decorative grass blades."""
    surf = pygame.Surface((12, 10), pygame.SRCALPHA)
    greens = [(30, 130, 30), (45, 155, 45), (25, 115, 25)]
    for i, gx in enumerate((2, 5, 8)):
        c = greens[i % len(greens)]
        bh = random.randint(5, 9)
        pygame.draw.line(surf, c, (gx, 9), (gx + random.randint(-2, 2), 9 - bh), 2)
    return surf


# -- Enemy art generators --

def _generate_mushroom_frames() -> list[pygame.Surface]:
    """Two-frame mushroom patrol enemy -- cleaner design."""
    frames = []
    for dy in (0, 1):
        surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        # Cap (red dome with white spots)
        pygame.draw.ellipse(surf, (180, 40, 40), (2, 2 + dy, 32, 20))
        pygame.draw.ellipse(surf, (200, 55, 55), (4, 4 + dy, 28, 16))
        for sx, sy in ((10, 6), (20, 4), (26, 10), (8, 12)):
            pygame.draw.circle(surf, COL_WHITE, (sx, sy + dy), 2)
        # Stem
        pygame.draw.rect(surf, (230, 210, 180), (12, 18 + dy, 12, 12), border_radius=3)
        # Eyes (angry)
        pygame.draw.circle(surf, COL_WHITE, (15, 22 + dy), 3)
        pygame.draw.circle(surf, COL_WHITE, (21, 22 + dy), 3)
        pygame.draw.circle(surf, COL_BLACK, (16, 22 + dy), 2)
        pygame.draw.circle(surf, COL_BLACK, (20, 22 + dy), 2)
        # Angry brows
        pygame.draw.line(surf, COL_BLACK, (12, 18 + dy), (17, 20 + dy), 2)
        pygame.draw.line(surf, COL_BLACK, (24, 18 + dy), (19, 20 + dy), 2)
        # Feet
        pygame.draw.ellipse(surf, (200, 180, 150), (10, 30 + dy, 8, 6))
        pygame.draw.ellipse(surf, (200, 180, 150), (18, 30 + dy, 8, 6))
        frames.append(surf)
    return frames


def _generate_chaser_frames() -> list[pygame.Surface]:
    """Two-frame shadow panther chaser -- sleek dark cat with glowing eyes."""
    frames = []
    for dy in (0, 1):
        surf = pygame.Surface((44, 36), pygame.SRCALPHA)
        body_c = (50, 35, 60)
        belly_c = (70, 55, 80)
        # Body (sleek ellipse)
        pygame.draw.ellipse(surf, body_c, (8, 10 + dy, 28, 18))
        pygame.draw.ellipse(surf, belly_c, (12, 15 + dy, 20, 10))
        # Head (round)
        pygame.draw.circle(surf, body_c, (12, 12 + dy), 10)
        pygame.draw.circle(surf, belly_c, (12, 14 + dy), 6)
        # Ears (triangular, clean)
        pygame.draw.polygon(surf, body_c, [(5, 8 + dy), (3, 0), (10, 5 + dy)])
        pygame.draw.polygon(surf, body_c, [(15, 6 + dy), (18, 0), (11, 3 + dy)])
        # Inner ear
        pygame.draw.polygon(surf, (100, 70, 90), [(6, 6 + dy), (4, 2), (9, 5 + dy)])
        pygame.draw.polygon(surf, (100, 70, 90), [(15, 5 + dy), (17, 2), (12, 4 + dy)])
        # Eyes (bright yellow-green, menacing)
        pygame.draw.circle(surf, (180, 255, 50), (9, 11 + dy), 3)
        pygame.draw.circle(surf, (180, 255, 50), (16, 11 + dy), 3)
        # Slit pupils
        pygame.draw.rect(surf, COL_BLACK, (9, 9 + dy, 1, 4))
        pygame.draw.rect(surf, COL_BLACK, (16, 9 + dy, 1, 4))
        # Nose
        pygame.draw.circle(surf, (30, 20, 30), (12, 16 + dy), 2)
        # Legs (slim)
        for lx in (12, 18, 26, 30):
            pygame.draw.rect(surf, body_c, (lx, 26 + dy, 4, 10), border_radius=2)
            pygame.draw.ellipse(surf, (40, 25, 50), (lx - 1, 33 + dy, 6, 3))  # paw
        # Tail (smooth curve)
        pts = [(36, 14 + dy), (40, 10 + dy), (43, 8 + dy), (44, 6 + dy)]
        pygame.draw.lines(surf, body_c, False, pts, 3)
        pygame.draw.circle(surf, body_c, (44, 6 + dy), 2)
        frames.append(surf)
    return frames


def _generate_flying_frames() -> list[pygame.Surface]:
    """Two-frame bat with spikes -- cleaner wing shape."""
    frames = []
    for wing_up in (True, False):
        surf = pygame.Surface((34, 28), pygame.SRCALPHA)
        body_c = (80, 30, 120)
        pygame.draw.ellipse(surf, body_c, (11, 9, 12, 14))
        if wing_up:
            pygame.draw.polygon(surf, (110, 50, 150), [(11, 14), (0, 3), (15, 11)])
            pygame.draw.polygon(surf, (110, 50, 150), [(23, 14), (34, 3), (19, 11)])
        else:
            pygame.draw.polygon(surf, (110, 50, 150), [(11, 14), (0, 21), (15, 17)])
            pygame.draw.polygon(surf, (110, 50, 150), [(23, 14), (34, 21), (19, 17)])
        # Eyes
        pygame.draw.circle(surf, (255, 50, 50), (14, 13), 2)
        pygame.draw.circle(surf, (255, 50, 50), (20, 13), 2)
        pygame.draw.circle(surf, (255, 200, 200), (14, 12), 1)
        pygame.draw.circle(surf, (255, 200, 200), (20, 12), 1)
        # Spikes
        for sx in (13, 17, 21):
            pygame.draw.polygon(surf, (200, 60, 60),
                                [(sx, 9), (sx - 2, 3), (sx + 2, 3)])
        frames.append(surf)
    return frames


def generate_mutant_boss(w: int, h: int) -> pygame.Surface:
    """Procedural mutant panda boss -- corrupted, larger, menacing."""
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2

    # Body (bulky dark torso)
    body_c = (60, 45, 70)
    pygame.draw.ellipse(surf, body_c, (cx - 28, cy - 8, 56, 42))
    # Belly scar / corruption glow
    pygame.draw.ellipse(surf, (90, 40, 50), (cx - 16, cy + 2, 32, 22))
    # Corruption veins on belly
    for vx in (-8, 0, 8):
        pygame.draw.line(surf, (120, 50, 60),
                         (cx + vx, cy + 4), (cx + vx + 3, cy + 20), 1)

    # Arms (thick, clawed)
    arm_c = (50, 35, 60)
    # Left arm
    pygame.draw.rect(surf, arm_c, (cx - 38, cy - 2, 12, 28), border_radius=4)
    # Right arm
    pygame.draw.rect(surf, arm_c, (cx + 26, cy - 2, 12, 28), border_radius=4)
    # Claws
    claw_c = (200, 180, 160)
    for side, sx in [(-1, cx - 38), (1, cx + 30)]:
        for ci in range(3):
            px = sx + 2 + ci * 3
            pygame.draw.line(surf, claw_c, (px, cy + 24), (px + side, cy + 30), 2)

    # Legs (stocky)
    leg_c = (45, 30, 55)
    pygame.draw.rect(surf, leg_c, (cx - 20, cy + 28, 14, 16), border_radius=4)
    pygame.draw.rect(surf, leg_c, (cx + 6, cy + 28, 14, 16), border_radius=4)
    # Feet
    pygame.draw.ellipse(surf, (40, 25, 50), (cx - 22, cy + 40, 18, 6))
    pygame.draw.ellipse(surf, (40, 25, 50), (cx + 4, cy + 40, 18, 6))

    # Head (large, round, corrupted panda)
    head_c = (75, 60, 80)
    pygame.draw.circle(surf, head_c, (cx, cy - 16), 22)
    # Face lighter area
    pygame.draw.circle(surf, (100, 85, 105), (cx, cy - 12), 14)

    # Ears (tattered, one larger)
    ear_c = (65, 50, 70)
    pygame.draw.circle(surf, ear_c, (cx - 18, cy - 32), 9)
    pygame.draw.circle(surf, (120, 50, 50), (cx - 18, cy - 32), 4)  # red inner
    pygame.draw.circle(surf, ear_c, (cx + 18, cy - 34), 10)
    pygame.draw.circle(surf, (120, 50, 50), (cx + 18, cy - 34), 5)
    # Torn ear notch (triangle cut)
    pygame.draw.polygon(surf, (0, 0, 0, 0), [
        (cx + 14, cy - 42), (cx + 20, cy - 40), (cx + 16, cy - 36)])

    # Eye patches (corrupted red-tinted)
    pygame.draw.ellipse(surf, (80, 30, 40), (cx - 14, cy - 22, 12, 10))
    pygame.draw.ellipse(surf, (80, 30, 40), (cx + 2, cy - 22, 12, 10))

    # Eyes (glowing red with bright center)
    pygame.draw.circle(surf, (220, 40, 40), (cx - 8, cy - 17), 5)
    pygame.draw.circle(surf, (220, 40, 40), (cx + 8, cy - 17), 5)
    # Pupils (yellow slit)
    pygame.draw.rect(surf, (255, 200, 50), (cx - 9, cy - 20, 2, 6))
    pygame.draw.rect(surf, (255, 200, 50), (cx + 7, cy - 20, 2, 6))
    # Eye glow
    pygame.draw.circle(surf, (255, 80, 60), (cx - 8, cy - 17), 6, 1)
    pygame.draw.circle(surf, (255, 80, 60), (cx + 8, cy - 17), 6, 1)

    # Nose
    pygame.draw.ellipse(surf, (50, 30, 40), (cx - 3, cy - 10, 7, 5))

    # Mouth (snarling with fangs)
    pygame.draw.arc(surf, (40, 20, 30), (cx - 10, cy - 8, 20, 10), 3.14, 6.28, 2)
    # Fangs
    fang_c = (230, 220, 200)
    pygame.draw.polygon(surf, fang_c, [(cx - 7, cy - 4), (cx - 5, cy + 3), (cx - 3, cy - 4)])
    pygame.draw.polygon(surf, fang_c, [(cx + 3, cy - 4), (cx + 5, cy + 3), (cx + 7, cy - 4)])

    # Corruption marks (purple cracks across body)
    crack_c = (150, 50, 180)
    pygame.draw.line(surf, crack_c, (cx - 12, cy - 28), (cx - 20, cy - 10), 2)
    pygame.draw.line(surf, crack_c, (cx + 10, cy - 25), (cx + 22, cy - 8), 2)
    pygame.draw.line(surf, crack_c, (cx - 5, cy + 5), (cx - 15, cy + 20), 1)
    pygame.draw.line(surf, crack_c, (cx + 5, cy + 8), (cx + 12, cy + 22), 1)

    # Spiky corrupted mane/fur on top of head
    spike_c = (100, 40, 110)
    for sx_off in (-12, -6, 0, 6, 12):
        sh = 8 + abs(sx_off) // 3
        pygame.draw.polygon(surf, spike_c, [
            (cx + sx_off - 3, cy - 34),
            (cx + sx_off, cy - 34 - sh),
            (cx + sx_off + 3, cy - 34)])

    return surf


def _generate_slime_frames() -> list[pygame.Surface]:
    """Two-frame bouncing slime enemy -- green jelly blob."""
    frames = []
    # Frame 0: normal shape
    s0 = pygame.Surface((30, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(s0, (50, 180, 80), (2, 6, 26, 22))
    pygame.draw.ellipse(s0, (70, 210, 100), (6, 10, 18, 14))  # highlight
    pygame.draw.circle(s0, COL_WHITE, (10, 14), 3)
    pygame.draw.circle(s0, COL_WHITE, (20, 14), 3)
    pygame.draw.circle(s0, COL_BLACK, (11, 14), 2)
    pygame.draw.circle(s0, COL_BLACK, (19, 14), 2)
    pygame.draw.arc(s0, COL_BLACK, (11, 18, 8, 5), 3.14, 6.28, 1)
    frames.append(s0)
    # Frame 1: squished (wider, shorter)
    s1 = pygame.Surface((30, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(s1, (50, 180, 80), (0, 10, 30, 18))
    pygame.draw.ellipse(s1, (70, 210, 100), (4, 13, 22, 12))
    pygame.draw.circle(s1, COL_WHITE, (10, 17), 3)
    pygame.draw.circle(s1, COL_WHITE, (20, 17), 3)
    pygame.draw.circle(s1, COL_BLACK, (11, 17), 2)
    pygame.draw.circle(s1, COL_BLACK, (19, 17), 2)
    pygame.draw.arc(s1, COL_BLACK, (11, 20, 8, 4), 3.14, 6.28, 1)
    frames.append(s1)
    return frames


# ---------------------------------------------------------------------------
# Sprite classes
# ---------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    """The panda protagonist with full physics and animation."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.frames = generate_panda_frames()
        self.anim_state = "idle"
        self.anim_frame = 0
        self.anim_timer = 0.0
        self.facing_right = True

        self.image = self.frames["idle"][0]
        self.rect = self.image.get_rect(bottomleft=(x, y))

        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0
        self.is_on_ground = False

        self.health: int = PLAYER_MAX_HP
        self.score: int = 0
        self.invincible_timer: float = 0.0

        self.combo_count: int = 0
        self.combo_timer: float = 0.0

        self.has_double_jump: bool = False
        self.jumps_remaining: int = 1

        self.friction_mode: str = "normal"  # "normal" or "ice"
        self.dead = False

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper,
               platforms: pygame.sprite.Group) -> None:
        if self.dead:
            return

        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo_count = 0

        if self.friction_mode == "ice":
            from config import ICE_ACCEL, ICE_FRICTION
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocity_x -= ICE_ACCEL * dt
                self.facing_right = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocity_x += ICE_ACCEL * dt
                self.facing_right = True
            self.velocity_x *= ICE_FRICTION
            max_v = PLAYER_SPEED * 1.5
            self.velocity_x = max(-max_v, min(max_v, self.velocity_x))
            if abs(self.velocity_x) < 5:
                self.velocity_x = 0.0
        else:
            self.velocity_x = 0.0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocity_x = -PLAYER_SPEED
                self.facing_right = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocity_x = PLAYER_SPEED
                self.facing_right = True

        self.rect.x += _fl(self.velocity_x * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_x > 0:
                self.rect.right = hit.rect.left
            elif self.velocity_x < 0:
                self.rect.left = hit.rect.right

        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)

        self.is_on_ground = False
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
                self.is_on_ground = True
                self.jumps_remaining = 2 if self.has_double_jump else 1
            elif self.velocity_y < 0:
                self.rect.top = hit.rect.bottom
                self.velocity_y = 0

        self._update_animation(dt)

    def jump(self) -> bool:
        if self.jumps_remaining > 0:
            self.velocity_y = PLAYER_JUMP
            self.jumps_remaining -= 1
            if self.is_on_ground:
                self.is_on_ground = False
            return True
        return False

    def take_damage(self, amount: int = PLAYER_DAMAGE) -> bool:
        if self.invincible_timer > 0 or self.dead:
            return False
        self.health -= amount
        self.invincible_timer = PLAYER_INVINCIBLE_SEC
        if self.health <= 0:
            self.health = 0
            self.dead = True
        return True

    def collect_bamboo(self) -> int:
        self.combo_count = min(self.combo_count + 1, len(COMBO_MULTIPLIERS) - 1)
        self.combo_timer = COMBO_WINDOW
        mult = COMBO_MULTIPLIERS[min(self.combo_count, len(COMBO_MULTIPLIERS) - 1)]
        points = BAMBOO_SCORE * mult
        self.score += points
        return points

    def heal(self, amount: int = HEAL_AMOUNT) -> None:
        self.health = min(PLAYER_MAX_HP, self.health + amount)

    def get_stomp_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect.x + 4, self.rect.bottom - 8,
                           self.rect.width - 8, 8)

    def _update_animation(self, dt: float) -> None:
        prev = self.anim_state
        if not self.is_on_ground:
            self.anim_state = "jump" if self.velocity_y < 0 else "fall"
        elif abs(self.velocity_x) > 10:
            self.anim_state = "run"
        else:
            self.anim_state = "idle"

        if self.anim_state != prev:
            self.anim_frame = 0
            self.anim_timer = 0.0

        speed = 0.1 if self.anim_state == "run" else 0.5
        self.anim_timer += dt
        if self.anim_timer >= speed:
            self.anim_timer -= speed
            self.anim_frame += 1

        lst = self.frames[self.anim_state]
        frame = lst[self.anim_frame % len(lst)]
        self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int = 20) -> None:
        super().__init__()
        self.image = generate_platform_tile(w, h)
        self.rect = self.image.get_rect(topleft=(x, y))


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int,
                 axis: str = "horizontal", distance: float = 150.0) -> None:
        super().__init__()
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


class Bamboo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_image = generate_bamboo_surface()
        self.image = self.base_image
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.base_y = float(self.rect.y)
        self.bob_timer: float = random.uniform(0, 6.28)

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.bob_timer += dt * 2
        self.rect.y = _fl(self.base_y + math.sin(self.bob_timer) * 1.5)


class HealingItem(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_image = generate_heal_surface()
        self.image = self.base_image
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.pulse_timer: float = random.uniform(0, 6.28)

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.pulse_timer += dt * 4
        scale = 1.0 + 0.1 * math.sin(self.pulse_timer)
        w = int(25 * scale)
        h = int(25 * scale)
        cx, cy = self.rect.center
        self.image = pygame.transform.scale(self.base_image, (w, h))
        self.rect = self.image.get_rect(center=(cx, cy))


class PatrolEnemy(pygame.sprite.Sprite):
    """Mushroom that walks back and forth. Stompable."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 200.0) -> None:
        super().__init__()
        self._frames = _generate_mushroom_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.anim_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group,  # type: ignore[override]
               player: Player | None = None) -> None:
        if not self.alive_flag:
            return
        self.pos_x += ENEMY_PATROL_SPEED * self.direction * dt
        if abs(self.pos_x - self.origin_x) > self.patrol_width:
            self.direction *= -1
        self.rect.x = _fl(self.pos_x)
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
        self.anim_timer += dt
        idx = int(self.anim_timer * 4) % 2
        frame = self._frames[idx]
        self.image = frame if self.direction > 0 else pygame.transform.flip(frame, True, False)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class ChaserEnemy(pygame.sprite.Sprite):
    """Dark wolf that chases the player."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._frames = _generate_chaser_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.facing_right = True
        self.anim_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group,  # type: ignore[override]
               player: Player | None = None) -> None:
        if not self.alive_flag or player is None:
            return
        dx = player.rect.centerx - self.rect.centerx
        dy_abs = abs(player.rect.centery - self.rect.centery)
        if abs(dx) < ENEMY_CHASE_RANGE and dy_abs < ENEMY_CHASE_Y_RANGE:
            if dx > 0:
                self.rect.x += _fl(ENEMY_CHASE_SPEED * dt)
                self.facing_right = True
            elif dx < 0:
                self.rect.x -= _fl(ENEMY_CHASE_SPEED * dt)
                self.facing_right = False
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
        self.anim_timer += dt
        idx = int(self.anim_timer * 5) % 2
        frame = self._frames[idx]
        self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class SlimeEnemy(pygame.sprite.Sprite):
    """Bouncing slime blob. Stompable."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 180.0) -> None:
        super().__init__()
        self._frames = _generate_slime_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.on_ground = False
        self.hop_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group,  # type: ignore[override]
               player: Player | None = None) -> None:
        if not self.alive_flag:
            return
        # Horizontal drift
        self.pos_x += SLIME_BOUNCE_SPEED * self.direction * dt
        if abs(self.pos_x - self.origin_x) > self.patrol_width:
            self.direction *= -1
        self.rect.x = _fl(self.pos_x)
        # Hop periodically
        self.hop_timer += dt
        if self.on_ground and self.hop_timer > 0.8:
            self.velocity_y = SLIME_HOP_POWER
            self.on_ground = False
            self.hop_timer = 0.0
        # Gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        self.on_ground = False
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
                self.on_ground = True
        # Squished frame when on ground, normal when airborne
        self.image = self._frames[1] if self.on_ground else self._frames[0]
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class FlyingEnemy(pygame.sprite.Sprite):
    """Flying bat. NOT stompable."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int, flight_range: float = 200.0) -> None:
        super().__init__()
        self._frames = _generate_flying_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.flight_range = flight_range
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.time: float = random.uniform(0, 6.28)
        self.alive_flag = True
        self.anim_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group | None = None,  # type: ignore[override]
               player: Player | None = None) -> None:
        if not self.alive_flag:
            return
        self.pos_x += ENEMY_PATROL_SPEED * self.direction * dt
        if abs(self.pos_x - self.origin_x) > self.flight_range:
            self.direction *= -1
        self.time += dt * FLYING_ENEMY_FREQ * 2 * math.pi
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(self.origin_y + math.sin(self.time) * FLYING_ENEMY_AMP)
        self.anim_timer += dt
        idx = int(self.anim_timer * 6) % 2
        frame = self._frames[idx]
        self.image = frame if self.direction > 0 else pygame.transform.flip(frame, True, False)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()


class Boss(pygame.sprite.Sprite):
    """Large mutant panda boss."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._base_image = generate_mutant_boss(*BOSS_SIZE)
        self.image = self._base_image
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.hp: int = BOSS_HP
        self.state = "idle"
        self.state_timer: float = BOSS_IDLE_SEC
        self.charge_target_x: float = 0.0
        self.stunned: bool = False
        self.facing_right: bool = False
        self.velocity_y: float = 0.0
        self.alive_flag: bool = True
        self.flash_timer: float = 0.0

    def update(self, dt: float, player: Player,  # type: ignore[override]
               platforms: pygame.sprite.Group) -> None:
        if not self.alive_flag:
            return
        self.flash_timer = max(0, self.flash_timer - dt)
        if self.state == "idle":
            self.facing_right = player.rect.centerx > self.rect.centerx
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "charging"
                self.charge_target_x = float(player.rect.centerx)
                self.stunned = False
        elif self.state == "charging":
            dx = self.charge_target_x - self.rect.centerx
            if abs(dx) > 10:
                self.rect.x += _fl(BOSS_CHARGE_SPEED * dt * (1 if dx > 0 else -1))
                self.facing_right = dx > 0
            else:
                self.state = "stunned"
                self.stunned = True
                self.state_timer = BOSS_STUN_SEC
        elif self.state == "stunned":
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = BOSS_IDLE_SEC
                self.stunned = False
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
        img = self._base_image if self.facing_right else pygame.transform.flip(
            self._base_image, True, False)
        if self.flash_timer > 0 and int(self.flash_timer * 20) % 2:
            img = img.copy()
            img.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
        if self.stunned:
            tint = img.copy()
            tint.fill((80, 80, 200, 60), special_flags=pygame.BLEND_RGBA_ADD)
            img = tint
        self.image = img

    def take_hit(self) -> bool:
        self.hp -= 1
        self.flash_timer = 0.3
        if self.hp <= 0:
            self.alive_flag = False
            self.kill()
            return True
        return False

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag


class GrassTuft(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = generate_grass_tuft()
        self.rect = self.image.get_rect(bottomleft=(x, y))


class SafeZone(pygame.sprite.Sprite):
    """Forest clearing that acts as the level goal (replaces the old flag)."""
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        height = FLOOR_Y - y + (540 - FLOOR_Y)
        self.image = generate_safe_zone(max(80, height))
        self.rect = self.image.get_rect(bottomleft=(x, 540))


def _generate_checkpoint_surface(activated: bool = False) -> pygame.Surface:
    """A wooden signpost with a flag -- gray when inactive, green when hit."""
    surf = pygame.Surface((28, 60), pygame.SRCALPHA)
    # Pole
    pole_c = (100, 70, 40) if not activated else (110, 85, 50)
    pygame.draw.rect(surf, pole_c, (12, 10, 4, 50))
    # Base
    pygame.draw.rect(surf, (80, 55, 30), (6, 54, 16, 6), border_radius=2)
    # Flag
    if activated:
        flag_c = (50, 200, 80)
        flag_c2 = (40, 170, 60)
        # Checkmark on flag
        pygame.draw.polygon(surf, flag_c, [(16, 5), (28, 14), (16, 23)])
        pygame.draw.polygon(surf, flag_c2, [(16, 14), (28, 14), (16, 23)])
        pygame.draw.line(surf, COL_WHITE, (18, 15), (21, 19), 2)
        pygame.draw.line(surf, COL_WHITE, (21, 19), (26, 10), 2)
    else:
        flag_c = (160, 160, 160)
        flag_c2 = (130, 130, 130)
        pygame.draw.polygon(surf, flag_c, [(16, 5), (28, 14), (16, 23)])
        pygame.draw.polygon(surf, flag_c2, [(16, 14), (28, 14), (16, 23)])
    # Pole top knob
    pygame.draw.circle(surf, pole_c, (14, 8), 3)
    return surf


class Checkpoint(pygame.sprite.Sprite):
    """Checkpoint signpost. Saves player progress when touched."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_off = _generate_checkpoint_surface(False)
        self._img_on = _generate_checkpoint_surface(True)
        self.image = self._img_off
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.activated = False
        self.spawn_x = x
        self.spawn_y = y

    def activate(self) -> bool:
        """Activate this checkpoint. Returns True if newly activated."""
        if self.activated:
            return False
        self.activated = True
        self.image = self._img_on
        return True
