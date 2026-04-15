"""Title screen, HUD, transitions, and overlays."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from config import (
    COL_BAMBOO, COL_BLACK, COL_GOLD, COL_HP_GREEN, COL_HP_RED, COL_HUD_BG,
    COL_MENU_BG, COL_RED, COL_WHITE, LEVEL_NAMES, SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from save import get_best_score

if TYPE_CHECKING:
    from engine import Camera
    from sprites import Player

# ---------------------------------------------------------------------------
# Font cache
# ---------------------------------------------------------------------------

_font_cache: dict[tuple[int, bool], pygame.font.Font] = {}


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont("consolas", size, bold=bold)
    return _font_cache[key]


def draw_text(screen: pygame.Surface, text: str, size: int,
              color: tuple, cx: int, cy: int, bold: bool = False) -> None:
    font = get_font(size, bold)
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(cx, cy)))


def draw_text_shadow(screen: pygame.Surface, text: str, size: int,
                     color: tuple, cx: int, cy: int, bold: bool = False) -> None:
    draw_text(screen, text, size, (0, 0, 0), cx + 2, cy + 2, bold)
    draw_text(screen, text, size, color, cx, cy, bold)


def draw_text_left(screen: pygame.Surface, text: str, size: int,
                   color: tuple, x: int, cy: int, bold: bool = False) -> None:
    font = get_font(size, bold)
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(midleft=(x, cy)))


# ---------------------------------------------------------------------------
# Mini bamboo icon for HUD
# ---------------------------------------------------------------------------

def _draw_bamboo_icon(screen: pygame.Surface, x: int, y: int,
                      checked: bool = False) -> None:
    """Small 10x16 bamboo with optional checkmark."""
    c = COL_BAMBOO if not checked else (180, 180, 180)
    pygame.draw.rect(screen, c, (x + 3, y, 4, 16))
    pygame.draw.rect(screen, (50, 120, 0), (x + 2, y + 5, 6, 2))
    pygame.draw.rect(screen, (50, 120, 0), (x + 2, y + 11, 6, 2))
    if checked:
        # Green checkmark overlay
        pygame.draw.line(screen, (50, 220, 50), (x + 1, y + 8), (x + 4, y + 12), 2)
        pygame.draw.line(screen, (50, 220, 50), (x + 4, y + 12), (x + 9, y + 3), 2)


# ---------------------------------------------------------------------------
# Floating score text
# ---------------------------------------------------------------------------

class FloatingText:
    def __init__(self, text: str, x: float, y: float, color: tuple) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life: float = 1.0
        self.max_life: float = 1.0

    def update(self, dt: float) -> bool:
        self.y -= 60 * dt
        self.life -= dt
        return self.life > 0

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        sx, sy = camera.apply_pos(self.x, self.y)
        alpha = max(0, int(255 * (self.life / self.max_life)))
        font = get_font(22, bold=True)
        surf = font.render(self.text, True, self.color)
        alpha_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        alpha_surf.blit(surf, (0, 0))
        alpha_surf.set_alpha(alpha)
        screen.blit(alpha_surf, alpha_surf.get_rect(center=(int(sx), int(sy))))


# ---------------------------------------------------------------------------
# HUD with bamboo counter
# ---------------------------------------------------------------------------

class HUD:
    def __init__(self) -> None:
        self.displayed_hp: float = 100.0
        self.floating_texts: list[FloatingText] = []
        self.combo_display_timer: float = 0.0
        self.combo_scale: float = 1.0
        self.total_bamboos: int = 0
        self.collected_bamboos: int = 0
        self.lives: int = 3

    def set_bamboo_count(self, total: int) -> None:
        self.total_bamboos = total
        self.collected_bamboos = 0

    def on_bamboo_collected(self) -> None:
        self.collected_bamboos += 1

    def update(self, dt: float, player: Player) -> None:
        diff = player.health - self.displayed_hp
        self.displayed_hp += diff * min(1.0, 6 * dt)
        if self.combo_display_timer > 0:
            self.combo_display_timer -= dt
        self.combo_scale = max(1.0, self.combo_scale - 2 * dt)
        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]

    def draw(self, screen: pygame.Surface, player: Player,
             level_num: int, camera: Camera) -> None:
        # HUD backing
        hud_surf = pygame.Surface((260, 85), pygame.SRCALPHA)
        hud_surf.fill((*COL_HUD_BG, 190))
        pygame.draw.rect(hud_surf, (60, 60, 60, 100), (0, 0, 260, 85), 2, border_radius=8)
        screen.blit(hud_surf, (8, 8))

        # HP label + bar
        draw_text(screen, "HP", 18, COL_WHITE, 30, 28)
        pygame.draw.rect(screen, COL_HP_RED, (48, 20, 150, 14), border_radius=4)
        fill_w = max(0, int(self.displayed_hp * 1.5))
        if fill_w > 0:
            pygame.draw.rect(screen, COL_HP_GREEN, (48, 20, fill_w, 14), border_radius=4)
        # HP text
        draw_text(screen, f"{int(self.displayed_hp)}", 14, COL_WHITE, 123, 28)

        # Score
        draw_text(screen, f"SCORE: {player.score}", 20, COL_GOLD, 138, 50, bold=True)

        # Bamboo counter with checkmark icons
        bx = 22
        by = 65
        for i in range(min(self.total_bamboos, 12)):
            checked = i < self.collected_bamboos
            _draw_bamboo_icon(screen, bx + i * 14, by, checked)
        if self.total_bamboos > 12:
            draw_text(screen, f"{self.collected_bamboos}/{self.total_bamboos}",
                      14, COL_BAMBOO, bx + 12 * 14 + 20, by + 8)
        else:
            draw_text(screen, f"{self.collected_bamboos}/{self.total_bamboos}",
                      14, (150, 220, 150), bx + self.total_bamboos * 14 + 15, by + 8)

        # Level indicator
        draw_text_shadow(screen, f"LEVEL {level_num}", 20, COL_WHITE,
                         SCREEN_WIDTH - 60, 25)

        # Lives display (panda head icons)
        lives_x = SCREEN_WIDTH - 100
        lives_y = 45
        draw_text(screen, "LIVES:", 14, (180, 180, 180), lives_x - 5, lives_y)
        for li in range(self.lives):
            lx = lives_x + 28 + li * 20
            pygame.draw.circle(screen, (240, 240, 235), (lx, lives_y), 7)
            pygame.draw.circle(screen, (30, 30, 30), (lx - 2, lives_y - 1), 2)
            pygame.draw.circle(screen, (30, 30, 30), (lx + 2, lives_y - 1), 2)

        # Combo counter
        if player.combo_count > 1:
            sz = int(28 * self.combo_scale)
            draw_text_shadow(screen, f"x{player.combo_count}!", sz, COL_GOLD,
                             SCREEN_WIDTH // 2, 30, bold=True)

        # Floating texts
        for ft in self.floating_texts:
            ft.draw(screen, camera)

    def add_floating_text(self, text: str, x: float, y: float,
                          color: tuple = COL_GOLD) -> None:
        self.floating_texts.append(FloatingText(text, x, y, color))
        self.combo_display_timer = 1.0
        self.combo_scale = 1.5


# ---------------------------------------------------------------------------
# Character showcase - generate actual sprite previews at import time
# ---------------------------------------------------------------------------

_sprite_cache: dict[str, pygame.Surface] | None = None


def _get_sprite_cache() -> dict[str, pygame.Surface]:
    """Lazy-init sprite previews (needs pygame.display to be set)."""
    global _sprite_cache
    if _sprite_cache is not None:
        return _sprite_cache

    from sprites import (
        generate_panda_frames, _generate_mushroom_frames,
        _generate_chaser_frames, _generate_slime_frames,
        _generate_flying_frames, generate_mutant_boss,
    )

    _sprite_cache = {}

    panda_frames = generate_panda_frames()
    _sprite_cache["panda"] = pygame.transform.scale(panda_frames["idle"][0], (54, 66))

    mush = _generate_mushroom_frames()[0]
    _sprite_cache["mushroom"] = pygame.transform.scale(mush, (54, 54))

    chase = _generate_chaser_frames()[0]
    _sprite_cache["panther"] = pygame.transform.scale(chase, (66, 54))

    slime = _generate_slime_frames()[0]
    _sprite_cache["slime"] = pygame.transform.scale(slime, (54, 50))

    bat = _generate_flying_frames()[0]
    _sprite_cache["bat"] = pygame.transform.scale(bat, (54, 44))

    _sprite_cache["boss"] = pygame.transform.scale(generate_mutant_boss(90, 90), (66, 66))

    return _sprite_cache


_CHARACTERS = [
    {"name": "Pain-da",   "role": "HERO",    "desc": "Exiled warrior. Reclaim the sacred grove.",      "key": "panda",    "color": (220, 240, 220)},
    {"name": "Shroomba",  "role": "PATROL",  "desc": "A twisted fungus guarding stolen bamboo",         "key": "mushroom", "color": (220, 100, 100)},
    {"name": "Shadow",    "role": "CHASER",  "desc": "Shadowblade of the corrupted forest",             "key": "panther",  "color": (180, 255, 100)},
    {"name": "Blobby",    "role": "BOUNCER", "desc": "Acid jelly. Looks cute -- still lethal.",         "key": "slime",    "color": (100, 230, 140)},
    {"name": "Nightwing", "role": "FLYER",   "desc": "Razor-winged bat. Do NOT try to stomp.",          "key": "bat",      "color": (170, 120, 230)},
    {"name": "The Mutant","role": "BOSS",    "desc": "The fallen king. Stomp only when stunned.",        "key": "boss",     "color": (255, 120, 120)},
]


def _draw_card(screen: pygame.Surface, char: dict,
               x: int, y: int, w: int, h: int,
               timer: float, idx: int) -> None:
    """Draw one character card with sprite, name, role, and description."""
    sprites = _get_sprite_cache()

    # Card bg
    card = pygame.Surface((w, h), pygame.SRCALPHA)
    card.fill((12, 25, 12, 210))
    pygame.draw.rect(card, (40, 70, 40, 180), (0, 0, w, h), 1, border_radius=6)
    # Colored accent bar at top
    pygame.draw.rect(card, (*char["color"], 140), (0, 0, w, 3), border_radius=6)
    screen.blit(card, (x, y))

    # Sprite preview (centered, bobbing)
    sprite = sprites.get(char["key"])
    if sprite:
        bob = math.sin(timer * 2.5 + idx * 1.1) * 3
        sw, sh = sprite.get_size()
        sx = x + (w - sw) // 2
        sy = y + 10 + int(bob)
        screen.blit(sprite, (sx, sy))

    # Name
    name_y = y + 78
    draw_text(screen, char["name"], 16, char["color"], x + w // 2, name_y, bold=True)

    # Role tag
    role_y = name_y + 16
    tag_font = get_font(10)
    tag_surf = tag_font.render(char["role"], True, (30, 50, 30))
    tw, th = tag_surf.get_size()
    tag_bg = pygame.Surface((tw + 8, th + 4), pygame.SRCALPHA)
    tag_bg.fill((*char["color"], 100))
    tag_x = x + (w - tw - 8) // 2
    screen.blit(tag_bg, (tag_x, role_y - 2))
    screen.blit(tag_surf, (tag_x + 4, role_y))

    # Description (single line, fits in card)
    desc_y = role_y + 18
    draw_text(screen, char["desc"], 11, (140, 180, 140), x + w // 2, desc_y)


# ---------------------------------------------------------------------------
# Title Screen
# ---------------------------------------------------------------------------

class TitleScreen:
    def __init__(self) -> None:
        self.title_y: float = -60.0
        self.title_target_y: float = SCREEN_HEIGHT * 0.09
        self.prompt_timer: float = 0.0
        # Pre-render background once
        self._bg: pygame.Surface | None = None

    def update(self, dt: float) -> None:
        self.title_y += (self.title_target_y - self.title_y) * min(1.0, 4 * dt)
        self.prompt_timer += dt

    def _ensure_bg(self) -> pygame.Surface:
        """Pre-render the static background."""
        if self._bg is not None:
            return self._bg
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Gradient
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(15 + 8 * t)
            g = int(35 + 15 * t)
            b = int(15 + 8 * t)
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        # Bamboo stalks in background
        for bx in range(30, SCREEN_WIDTH, 80):
            bh = 80 + (bx * 37) % 60
            c = (20 + (bx % 12), 50 + (bx % 18), 18)
            pygame.draw.rect(bg, c, (bx, SCREEN_HEIGHT - bh, 5, bh))
            for jy in range(SCREEN_HEIGHT - bh + 12, SCREEN_HEIGHT, 18):
                pygame.draw.rect(bg, (16, 42, 14), (bx - 1, jy, 7, 2))
            # Tiny leaf
            pygame.draw.polygon(bg, (30, 65, 25),
                                [(bx + 5, SCREEN_HEIGHT - bh + 2),
                                 (bx + 14, SCREEN_HEIGHT - bh - 4),
                                 (bx + 5, SCREEN_HEIGHT - bh - 3)])
        self._bg = bg
        return bg

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._ensure_bg(), (0, 0))

        # Title
        draw_text_shadow(screen, "BAMBOO FOREST", 54, (200, 255, 200),
                         SCREEN_WIDTH // 2, int(self.title_y), bold=True)
        draw_text(screen, "~ The Legend of Pain-da ~", 18, (120, 180, 120),
                  SCREEN_WIDTH // 2, int(self.title_y) + 32)

        # Character gallery -- 2 rows x 3 columns
        card_w = 280
        card_h = 118
        gap_x = 20
        gap_y = 14
        total_row_w = 3 * card_w + 2 * gap_x
        start_x = (SCREEN_WIDTH - total_row_w) // 2
        row1_y = int(SCREEN_HEIGHT * 0.22)
        row2_y = row1_y + card_h + gap_y

        for i, char in enumerate(_CHARACTERS):
            col = i % 3
            row = i // 3
            cx = start_x + col * (card_w + gap_x)
            cy = row1_y if row == 0 else row2_y
            _draw_card(screen, char, cx, cy, card_w, card_h,
                       self.prompt_timer, i)

        # Pulsing prompt
        prompt_y = row2_y + card_h + 28
        alpha = int(128 + 127 * math.sin(self.prompt_timer * 3))
        font = get_font(26)
        prompt = font.render("Press ENTER to Start", True, (200, 255, 200))
        prompt.set_alpha(alpha)
        screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, prompt_y)))

        # Controls + high score
        draw_text(screen, "Arrows / WASD + Space to Jump (double jump!)  |  Stomp enemies!",
                  14, (90, 140, 90), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

        best = get_best_score()
        if best > 0:
            draw_text_shadow(screen, f"Best: {best}", 18, COL_GOLD,
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)


# ---------------------------------------------------------------------------
# Pause Overlay
# ---------------------------------------------------------------------------

class PauseOverlay:
    def draw(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        draw_text_shadow(screen, "PAUSED", 56, COL_WHITE,
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, bold=True)
        draw_text(screen, "ESC to Resume  |  Q to Quit", 24, (180, 180, 180),
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)


# ---------------------------------------------------------------------------
# Game Over Screen
# ---------------------------------------------------------------------------

class GameOverScreen:
    def __init__(self) -> None:
        self.fade_alpha: float = 0.0

    def update(self, dt: float) -> None:
        self.fade_alpha = min(200, self.fade_alpha + 300 * dt)

    def draw(self, screen: pygame.Surface, final_score: int) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(self.fade_alpha)))
        screen.blit(overlay, (0, 0))
        if self.fade_alpha > 100:
            draw_text_shadow(screen, "GAME OVER", 64, COL_RED,
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, bold=True)
            draw_text(screen, f"Score: {final_score}", 32, COL_WHITE,
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            draw_text(screen, "Press ENTER to Try Again", 24, (180, 180, 180),
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)


# ---------------------------------------------------------------------------
# Victory Screen
# ---------------------------------------------------------------------------

class VictoryScreen:
    def __init__(self) -> None:
        self.timer: float = 0.0

    def update(self, dt: float) -> None:
        self.timer += dt

    def draw(self, screen: pygame.Surface, final_score: int,
             is_high_score: bool) -> None:
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(20 * (1 - t) + 5 * t)
            g = int(50 * (1 - t) + 20 * t)
            b = int(20 * (1 - t) + 5 * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        bounce = math.sin(self.timer * 3) * 8
        draw_text_shadow(screen, "VICTORY!", 72, COL_GOLD,
                         SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.3 + bounce), bold=True)
        draw_text(screen, f"Final Score: {final_score}", 36, COL_WHITE,
                  SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.5))
        if is_high_score:
            alpha = int(128 + 127 * math.sin(self.timer * 5))
            font = get_font(28, bold=True)
            surf = font.render("NEW HIGH SCORE!", True, COL_GOLD)
            surf.set_alpha(alpha)
            screen.blit(surf, surf.get_rect(center=(
                SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.58))))
        draw_text(screen, "Press ENTER to Play Again", 24, (180, 180, 180),
                  SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.75))


# ---------------------------------------------------------------------------
# Level Transition
# ---------------------------------------------------------------------------

class LevelTransition:
    def __init__(self, level_number: int) -> None:
        self.level_number = level_number
        self.timer: float = 0.0
        self.duration: float = 2.0

    def update(self, dt: float) -> bool:
        self.timer += dt
        return self.timer >= self.duration

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COL_BLACK)
        t = self.timer / self.duration
        alpha = int(255 * (1 - abs(t - 0.5) * 2))
        alpha = max(0, min(255, alpha))

        font = get_font(56, bold=True)
        text = font.render(f"LEVEL {self.level_number}", True, COL_WHITE)
        text.set_alpha(alpha)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        idx = self.level_number - 1
        if 0 <= idx < len(LEVEL_NAMES):
            name_font = get_font(28)
            name = name_font.render(LEVEL_NAMES[idx], True, (180, 220, 180))
            name.set_alpha(alpha)
            screen.blit(name, name.get_rect(center=(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))


# ---------------------------------------------------------------------------
# Death Animation
# ---------------------------------------------------------------------------

class DeathAnimation:
    def __init__(self) -> None:
        self.timer: float = 1.0
        self.time_scale: float = 0.3

    def update(self, dt: float) -> bool:
        self.timer -= dt
        return self.timer <= 0

    def get_time_scale(self) -> float:
        return self.time_scale
