"""Title screen, HUD, transitions, and overlays."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from config import (
    COL_BAMBOO, COL_BLACK, COL_GOLD, COL_HP_GREEN, COL_HP_RED, COL_HUD_BG,
    COL_MENU_BG, COL_RED, COL_WHITE, LEVEL_NAMES, SCREEN_HEIGHT,
    SCREEN_WIDTH, ACCESSIBILITY_LABELS, ACCESSIBILITY_RANGES,
)
from save import get_best_score, add_essence, load_essences, load_grafts, unlock_graft, ESSENCE_BIOME_KEYS, get_profile_essences_and_grafts, load_settings, save_settings, spend_essence, spend_specific_essences
from config import BIOME_ESSENCE, RECIPES

if TYPE_CHECKING:
    from engine import Camera
    from sprites import Player

# ---------------------------------------------------------------------------
# Font cache
# ---------------------------------------------------------------------------

_font_cache: dict[tuple[int, bool], pygame.font.Font] = {}

# Accessibility text scale (set from profile at load / change)
_text_scale: float = 1.0


def set_text_scale(scale: float) -> None:
    global _text_scale
    _text_scale = max(0.5, min(2.0, float(scale)))


def get_text_scale() -> float:
    return _text_scale


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    scaled = max(8, int(size * _text_scale))
    key = (scaled, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont("consolas", scaled, bold=bold)
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
    """Small 10x16 bamboo pip: dim/hollow when uncollected, bright + check when collected."""
    if checked:
        stalk, node = COL_BAMBOO, (50, 120, 0)           # collected = bright green
    else:
        stalk, node = (74, 84, 74), (52, 60, 52)         # uncollected = dim/hollow
    pygame.draw.rect(screen, stalk, (x + 3, y, 4, 16))
    pygame.draw.rect(screen, node, (x + 2, y + 5, 6, 2))
    pygame.draw.rect(screen, node, (x + 2, y + 11, 6, 2))
    if checked:
        # Green checkmark overlay
        pygame.draw.line(screen, (50, 220, 50), (x + 1, y + 8), (x + 4, y + 12), 2)
        pygame.draw.line(screen, (50, 220, 50), (x + 4, y + 12), (x + 9, y + 3), 2)


def _draw_mini_feather(screen: pygame.Surface, x: int, y: int, color: tuple) -> None:
    """Tiny glide feather icon -- juicy with tiny sparkle."""
    pygame.draw.polygon(screen, color, [(x, y+4), (x+6, y), (x+6, y+8)])
    pygame.draw.line(screen, (255,255,255), (x+1, y+4), (x+5, y+4), 1)
    # sparkle dot
    pygame.draw.circle(screen, (255,255,255), (x+4, y+2), 1)


def _draw_mini_boot(screen: pygame.Surface, x: int, y: int, color: tuple) -> None:
    """Tiny dash boot icon -- juicy with highlight."""
    pygame.draw.rect(screen, color, (x, y+2, 7, 5), border_radius=1)
    pygame.draw.rect(screen, (min(255,color[0]+40), min(255,color[1]+30), min(255,color[2]+20)), (x+1, y+5, 3, 3))
    pygame.draw.rect(screen, (255,255,220), (x+5, y+3, 1, 1))  # toe sparkle


def _draw_mini_staff(screen: pygame.Surface, x: int, y: int, color: tuple) -> None:
    """Tiny staff/sword icon -- juicy with leaf accent."""
    pygame.draw.line(screen, color, (x+2, y), (x+2, y+8), 2)
    pygame.draw.polygon(screen, (255, 230, 120), [(x+2, y), (x+6, y+3), (x+2, y+3)])
    # mini leaf
    pygame.draw.polygon(screen, (80, 160, 60), [(x+1, y+6), (x+3, y+4), (x+3, y+8)])


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
             level_num: int, camera: Camera, run_timer: float = 0.0,
             daily_seed: int = 0) -> None:
        # HUD backing (tall if mana bar visible)
        hud_h = 100 if player.has_ice_magic else 85
        hud_surf = pygame.Surface((260, hud_h), pygame.SRCALPHA)
        hud_surf.fill((*COL_HUD_BG, 190))
        pygame.draw.rect(hud_surf, (60, 60, 60, 100),
                        (0, 0, 260, hud_h), 2, border_radius=8)
        screen.blit(hud_surf, (8, 8))

        # HP label + bar
        draw_text(screen, "HP", 18, COL_WHITE, 30, 28)
        pygame.draw.rect(screen, COL_HP_RED, (48, 20, 150, 14), border_radius=4)
        fill_w = max(0, int(self.displayed_hp * 1.5))
        if fill_w > 0:
            pygame.draw.rect(screen, COL_HP_GREEN, (48, 20, fill_w, 14), border_radius=4)
        # HP text
        draw_text(screen, f"{int(self.displayed_hp)}", 14, COL_WHITE, 123, 28)

        # Mana bar (only shown if player has ice magic unlocked)
        if player.has_ice_magic:
            draw_text(screen, "MP", 14, COL_WHITE, 30, 44)
            # Background
            pygame.draw.rect(screen, (40, 40, 70), (48, 40, 150, 10),
                            border_radius=3)
            mana_w = max(0, int(player.mana * 1.5))
            if mana_w > 0:
                # Cyan gradient
                col = (80, 180, 240) if player.mana >= player.mana_max else (60, 140, 200)
                pygame.draw.rect(screen, col, (48, 40, mana_w, 10),
                                border_radius=3)
                # Bright edge highlight
                pygame.draw.rect(screen, (180, 230, 255),
                                (48, 40, mana_w, 2), border_radius=2)
            # "READY" indicator when full
            if player.mana >= player.mana_max:
                t = pygame.time.get_ticks() / 200.0
                pulse = 0.7 + 0.3 * math.sin(t)
                pygame.draw.circle(screen,
                                  (int(255 * pulse), 255, int(255 * pulse)),
                                  (48 + mana_w - 4, 45), 3)

        # Score (shift down if mana bar visible)
        score_y = 65 if player.has_ice_magic else 50
        draw_text(screen, f"SCORE: {player.score}", 20, COL_GOLD, 138, score_y, bold=True)

        # Bamboo counter with checkmark icons
        bx = 22
        by = 80 if player.has_ice_magic else 65
        for i in range(min(self.total_bamboos, 12)):
            checked = i < self.collected_bamboos
            _draw_bamboo_icon(screen, bx + i * 14, by, checked)
        if self.total_bamboos > 12:
            draw_text(screen, f"{self.collected_bamboos}/{self.total_bamboos}",
                      14, COL_BAMBOO, bx + 12 * 14 + 20, by + 8)
        else:
            draw_text(screen, f"{self.collected_bamboos}/{self.total_bamboos}",
                      14, (150, 220, 150), bx + self.total_bamboos * 14 + 15, by + 8)

        # Level indicator + daily seed (Feature #3) + speedrun timer
        draw_text_shadow(screen, f"LEVEL {level_num}", 20, COL_WHITE,
                         SCREEN_WIDTH - 78, 24)
        if daily_seed:
            draw_text(screen, f"DAILY {daily_seed}", 12, (160, 200, 160),
                      SCREEN_WIDTH // 2, 8)
        if run_timer > 0:
            m = int(run_timer // 60)
            s = run_timer % 60
            draw_text_shadow(screen, f"{m:02d}:{s:05.2f}", 16, COL_GOLD,
                             SCREEN_WIDTH // 2, 18, bold=True)

        # Lives display (panda heads) — right-anchored so the row never clips the
        # screen edge, even with extra lives; heads grow leftward from the margin.
        lives_y = 46
        head_r = 7
        head_gap = 20
        right_margin = 14
        n = max(0, self.lives)
        leftmost_cx = SCREEN_WIDTH - right_margin - head_r - max(0, n - 1) * head_gap
        for li in range(n):
            lx = leftmost_cx + li * head_gap
            pygame.draw.circle(screen, (240, 240, 235), (lx, lives_y), head_r)
            pygame.draw.circle(screen, (30, 30, 30), (lx - 2, lives_y - 1), 2)
            pygame.draw.circle(screen, (30, 30, 30), (lx + 2, lives_y - 1), 2)
        # "LIVES:" label, right-aligned just left of the leftmost head
        lbl = get_font(14).render("LIVES:", True, (190, 190, 190))
        screen.blit(lbl, lbl.get_rect(midright=(leftmost_cx - head_r - 8, lives_y)))

        # Power-up indicators (below lives) -- richer timer pills + mini icons, juicy gradients/sparkles, bigger touch targets
        pwr_x = SCREEN_WIDTH - 126
        pwr_y = lives_y + 18
        row = 0
        pill_h = 16
        pill_w = 78
        for ptype, pval, pcol, picon in [
            ("GLIDE", player.glide_time_remaining, (140, 220, 255), _draw_mini_feather),
            ("DASH", player.dash_time_remaining, (255, 180, 100), _draw_mini_boot),
        ] + ([("SWORD", player.weapon_time_remaining, (255, 230, 120), _draw_mini_staff)] if player.has_bamboo_weapon else []):
            if pval > 0:
                val = int(pval)
                col = pcol if val > (3 if ptype=="GLIDE" else 5) else (255, 120, 120)
                # Juicy pill: SRC surface for alpha + gradient layers + border
                pill = pygame.Surface((pill_w, pill_h + 4), pygame.SRCALPHA)
                pill.fill((*col, 55))
                # top gradient highlight
                pygame.draw.rect(pill, (255, 255, 255, 35), (1, 1, pill_w-2, 6), border_radius=3)
                pygame.draw.rect(pill, (*col, 220), (0, 0, pill_w, pill_h + 4), 2, border_radius=5)
                # mini sparkle when fresh
                if val > 6:
                    spx = 8 + int((self.combo_scale * 3 + row) % 12)
                    pygame.draw.circle(pill, (255, 255, 255, 200), (spx, 4), 2)
                screen.blit(pill, (pwr_x - 2, pwr_y + row * 20 - 2))
                picon(screen, pwr_x, pwr_y + row * 20 + 2, col)
                draw_text(screen, f"{ptype} {val}s", 10, col, pwr_x + 14, pwr_y + row * 20 + 6)
                row += 1

        # Combo counter
        if player.combo_count > 1:
            sz = int(28 * self.combo_scale)
            draw_text_shadow(screen, f"x{player.combo_count}!", sz, COL_GOLD,
                             SCREEN_WIDTH // 2, 30, bold=True)

        # Persistent controls hint at bottom-right (always visible during play)
        hint_font = get_font(11)
        hint = hint_font.render(
            "ESC pause  |  F11 fullscreen", True, (150, 170, 150))
        screen.blit(hint, (SCREEN_WIDTH - hint.get_width() - 8,
                           SCREEN_HEIGHT - 16))

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

    # Biome enemies (level 4-8)
    from biomes import (SulfurSlime, AshBat, KelpCrab, BasaltGolem,
                        DustDevil, CactusScorpion, StalactiteSpider,
                        FalseGlowworm, BrineShard, ReflectionPhantom,
                        SporePuffer, MagmaLeaper, TidalCrab, PhaseWraith,
                        GravityDrone, HomingSpecter, ForgeHammer, VoidEater)
    from config import FLOOR_Y
    _sprite_cache["sulfur"] = pygame.transform.scale(SulfurSlime(0, FLOOR_Y).image, (54, 50))
    _sprite_cache["ashbat"] = pygame.transform.scale(AshBat(0, FLOOR_Y).image, (54, 44))
    _sprite_cache["crab"] = pygame.transform.scale(KelpCrab(0, FLOOR_Y).image, (54, 36))
    _sprite_cache["golem"] = pygame.transform.scale(BasaltGolem(0, FLOOR_Y).image, (45, 66))
    _sprite_cache["dust"] = pygame.transform.scale(DustDevil(0, FLOOR_Y).image, (45, 66))
    _sprite_cache["scorp"] = pygame.transform.scale(CactusScorpion(0, FLOOR_Y).image, (54, 42))
    _sprite_cache["spider"] = pygame.transform.scale(StalactiteSpider(0, 0).image, (42, 30))
    _sprite_cache["glow"] = pygame.transform.scale(FalseGlowworm(0, 0).image, (32, 32))
    _sprite_cache["brine"] = pygame.transform.scale(BrineShard(0, FLOOR_Y).image, (32, 54))
    _sprite_cache["phantom"] = pygame.transform.scale(ReflectionPhantom(0, FLOOR_Y).image, (54, 54))
    # Levels 14-18 new enemies
    _sprite_cache["puffer"] = pygame.transform.scale(SporePuffer(0, FLOOR_Y).image, (42, 50))
    _sprite_cache["leaper"] = pygame.transform.scale(MagmaLeaper(0, FLOOR_Y).image, (45, 45))
    _sprite_cache["tidalcrab"] = pygame.transform.scale(TidalCrab(0, FLOOR_Y).image, (45, 33))
    _sprite_cache["wraith"] = pygame.transform.scale(PhaseWraith(0, FLOOR_Y).image, (45, 60))
    _sprite_cache["drone"] = pygame.transform.scale(GravityDrone(0, FLOOR_Y).image, (45, 45))
    _sprite_cache["specter"] = pygame.transform.scale(HomingSpecter(0, FLOOR_Y).image, (51, 42))
    _sprite_cache["hammer"] = pygame.transform.scale(ForgeHammer(0, 400).image, (72, 48))
    _sprite_cache["voideater"] = pygame.transform.scale(VoidEater(0, FLOOR_Y).image, (54, 54))

    return _sprite_cache


_CHARACTERS = [
    {"name": "Pain-da", "role": "HERO", "desc": "Exiled warrior of the grove",
     "key": "panda", "color": (220, 240, 220),
     "story": "Once the protector of the sacred Bamboo Grove, Pain-da was cast out when corruption tainted the forest. Armed only with bamboo, fury, and a questionable haircut, he returns to reclaim every biome from the mutant invaders. He jumps twice, dashes through danger, glides over pits, slams from above, and throws bamboo shurikens. He also dances when he wins.\n\nTIP: Stomp enemies from above. Pick up the bamboo staff to swing melee."},
    {"name": "Shroomba", "role": "PATROL", "desc": "Twisted fungus guardian",
     "key": "mushroom", "color": (220, 100, 100),
     "story": "A once-peaceful mushroom, corrupted by the spores of the Mutant King. Walks back and forth along a short patrol route, scowling. Slow but hits hard if you bump into its cap.\n\nHOW TO BEAT: Jump on its head. One stomp kills it. Avoid running into its side."},
    {"name": "Shadow", "role": "CHASER", "desc": "Shadowblade of the forest",
     "key": "panther", "color": (180, 255, 100),
     "story": "A sleek panther that slipped into the grove from the shadow realm. Its glowing eyes lock onto Pain-da whenever he's nearby -- it chases fast and doesn't stop until it catches you or you lose it.\n\nHOW TO BEAT: Jump over its head when it closes in, then stomp. Dash to escape if cornered."},
    {"name": "Blobby", "role": "BOUNCER", "desc": "Cute acid jelly",
     "key": "slime", "color": (100, 230, 140),
     "story": "Don't let the smile fool you. Blobby bounces in random arcs and leaves no trail -- but contact is lethal acid. The Mutant's bioweapon, too cute to hate, too dangerous to ignore.\n\nHOW TO BEAT: Time your jump for when Blobby is mid-hop. Stomp on the top of the bounce."},
    {"name": "Nightwing", "role": "FLYER", "desc": "Spiked bat -- can't be stomped",
     "key": "bat", "color": (170, 120, 230),
     "story": "Razor-winged bat with poisonous spikes on its back. Cannot be stomped -- try and you'll impale yourself. Flies in loose sine patterns through the sky.\n\nHOW TO BEAT: Do NOT jump on it. Use the bamboo staff (E) or shuriken (Q) from a safe distance, or just avoid it."},
    {"name": "The Mutant", "role": "BOSS", "desc": "Stomp only when stunned",
     "key": "boss", "color": (255, 120, 120),
     "story": "The fallen king of the forest, twisted by dark spores into a hulking mutant. Patrols, then charges at Pain-da. After each charge it stuns itself -- that's your only window to hit it.\n\nHOW TO BEAT: Dodge the charge, then stomp the BLUE (stunned) boss. 5 hits to defeat. Landing on its head at any other time is safe but deals no damage."},
    {"name": "Sulfurite", "role": "TOXIC", "desc": "Leaves poison trail",
     "key": "sulfur", "color": (200, 200, 40),
     "story": "A volcanic slime of liquid sulfur. Crawls slowly but drools an acid pool behind it that burns for 3 seconds. The Caldera's living trap.\n\nHOW TO BEAT: Stomp it directly. Jump OVER the yellow puddles it leaves -- don't step in them."},
    {"name": "Ash-Swoop", "role": "SWOOPER", "desc": "Dives at airborne prey",
     "key": "ashbat", "color": (120, 80, 70),
     "story": "Born of volcanic ash. Hovers in place until it senses you in the air -- then swoops down in a straight dive at your jump apex. A punishment for clumsy platforming.\n\nHOW TO BEAT: Jump at it to stomp on the way down. If it's swooping, dash under it horizontally."},
    {"name": "Kelp-Shell", "role": "ARMORED", "desc": "Stomp only -- sides bounce you off!",
     "key": "crab", "color": (180, 80, 60),
     "story": "Armored basalt crab with an impenetrable hard shell on all sides but the top. Side collisions do damage AND bounce you off.\n\nHOW TO BEAT: Come from above. Side hits = YOU take damage. The bamboo staff hits from the side work fine though."},
    {"name": "Column-Doom", "role": "AMBUSH", "desc": "Pillar that strikes when close",
     "key": "golem", "color": (90, 90, 110),
     "story": "Disguised as a harmless basalt column. When Pain-da comes within 80 pixels, it reveals glowing eyes and lunges horizontally toward him at high speed. Then cools for 2 seconds before retracting.\n\nHOW TO BEAT: Approach cautiously. When it telegraphs (reveals eyes), JUMP -- either over it or onto its head to stomp."},
    {"name": "Duster", "role": "DODGE", "desc": "Invincible vortex -- dodge!",
     "key": "dust", "color": (200, 180, 140),
     "story": "A desert dust-devil animated by old magic. Completely invincible. Moves in erratic sine-wave patterns across the rift. Does damage on contact.\n\nHOW TO BEAT: You can't kill it. You MUST evade. Watch its movement pattern, wait for a gap, dash through."},
    {"name": "Needler", "role": "RANGED", "desc": "Fires 45-degree thorns",
     "key": "scorp", "color": (160, 120, 60),
     "story": "Cactus-scorpion hybrid with a thorn-loaded tail. Fires a projectile every 2 seconds at a 45-degree upward arc.\n\nHOW TO BEAT: Stomp it from above. Watch for incoming thorns -- you can dash past them or duck by sliding on ice."},
    {"name": "Driptop", "role": "CEILING", "desc": "Drops from above when you pass",
     "key": "spider", "color": (80, 60, 60),
     "story": "Clings silently to cave ceilings. When Pain-da passes below, it drops straight down on a silk thread. Lands, then patrols the floor.\n\nHOW TO BEAT: Best handled mid-air -- hit its descent with a jump-stomp. Or dash past before it drops."},
    {"name": "Lure-Bug", "role": "TRAP", "desc": "Pretty light that snaps shut",
     "key": "glow", "color": (150, 255, 100),
     "story": "Glows a soft inviting green in the dark caves -- you'll be tempted to touch it. When you're within 60 pixels, it SNAPS to red and bites for 0.5s.\n\nHOW TO BEAT: It's invincible. Keep your distance. Green = safe, red = damage."},
    {"name": "Brine-Star", "role": "STATIC", "desc": "Grows if you stand still",
     "key": "brine", "color": (200, 220, 255),
     "story": "A salt crystal that responds to stillness. It grows larger the longer Pain-da stands near it motionless. At full size, it damages on contact.\n\nHOW TO BEAT: Keep moving! On the ice physics level, this is a test of control. The crystal is invincible -- never stand still near it."},
    {"name": "Phantom", "role": "MIRROR", "desc": "Only visible in reflection",
     "key": "phantom", "color": (220, 220, 240),
     "story": "A translucent spectre that roams the salt flats. Hard to see in the real world -- watch the mirror surface to spot them. Still does damage even when invisible.\n\nHOW TO BEAT: Use the reflection on the salt surface to track it. Stomp from above when you know where it is."},
    # --- Level 14-18 enemies ---
    {"name": "Puff-cap", "role": "SPORE", "desc": "Stationary, releases clouds",
     "key": "puffer", "color": (120, 200, 120),
     "story": "Sentient mushroom that periodically puffs drifting poison spores in two directions. Doesn't move, but its spores slowly float upward and damage on contact.\n\nHOW TO BEAT: Stomp it directly to kill -- this also clears its active spores. Or stay below its altitude."},
    {"name": "Magma-Leap", "role": "ERUPTER", "desc": "Jumps from rising lava",
     "key": "leaper", "color": (255, 150, 80),
     "story": "Molten creature that lurks beneath the rising lava. Periodically erupts in an arc, landing briefly before sinking back. Tracks toward the player during the rise.\n\nHOW TO BEAT: Stomp it while it's airborne -- it's vulnerable then. If it lands near you, dash away."},
    {"name": "Tide-Claw", "role": "CYCLING", "desc": "Patrols the timed gates",
     "key": "tidalcrab", "color": (80, 160, 180),
     "story": "Coastal crab that walks the alternating stone gates. When its gate vanishes, it plummets to the next solid surface and resumes patrolling. Their positions change every 3 seconds.\n\nHOW TO BEAT: Stomp from above. Just be aware its gate can disappear under you too."},
    {"name": "Phase-Wraith", "role": "TELEPORT", "desc": "Uses portals too",
     "key": "wraith", "color": (200, 140, 255),
     "story": "Ghostly figure that also uses the teleport portals. Patrols normally, then occasionally jumps through an active portal and reappears at its partner. Stompable but hard to predict.\n\nHOW TO BEAT: Track portal pairs. If you see it near a portal, expect it on the partner side next."},
    {"name": "Grav-Drone", "role": "PULLER", "desc": "Pulls you toward itself",
     "key": "drone", "color": (180, 120, 255),
     "story": "Floating mechanical sphere with a gravitational field. When you enter its 200px range, it drags your velocity toward its center -- disrupting jumps and platforming.\n\nHOW TO BEAT: Stomp it to kill. Or use the ice spell from outside its range."},
    {"name": "Specter", "role": "TRACKER", "desc": "ALWAYS homes on the player",
     "key": "specter", "color": (230, 160, 255),
     "story": "Ghostly flier designed to punish air-cheese. Slow on the ground but ACCELERATES when Pain-da is airborne -- especially when gliding. Red eyes lock on from across the level.\n\nHOW TO BEAT: Land often. Stomp it when it closes. Or freeze it with the ice spell."},
    {"name": "Forge-Hammer", "role": "CRUSHER", "desc": "Slams from the ceiling",
     "key": "hammer", "color": (100, 100, 120),
     "story": "Ceiling-mounted iron hammer on an invisible chain. Telegraphs for 0.5 seconds, then slams down with crushing force. Damages double on contact while slamming.\n\nHOW TO BEAT: Cannot be killed. Watch the telegraph flash and sprint out of its column."},
    {"name": "Void-Eater", "role": "MOUTH", "desc": "Hungry maw -- not stompable",
     "key": "voideater", "color": (140, 60, 200),
     "story": "A hungry void-spawn with a mouth that opens and closes on a timer. While open, it damages on contact. Floating bob pattern makes it tricky to predict.\n\nHOW TO BEAT: Not stompable. Freeze it with the ice spell, or dash past while its mouth is closed."},
]


def _draw_card(screen: pygame.Surface, char: dict,
               x: int, y: int, w: int, h: int,
               timer: float, idx: int, hovered: bool = False) -> None:
    """Draw one character card. Hovered cards are highlighted."""
    sprites = _get_sprite_cache()

    # Card bg -- brighter when hovered
    card = pygame.Surface((w, h), pygame.SRCALPHA)
    if hovered:
        card.fill((30, 55, 30, 240))
        pygame.draw.rect(card, (*char["color"], 255),
                         (0, 0, w, h), 2, border_radius=6)
    else:
        card.fill((12, 25, 12, 210))
        pygame.draw.rect(card, (40, 70, 40, 180), (0, 0, w, h), 1, border_radius=6)
    # Colored accent bar at top
    pygame.draw.rect(card, (*char["color"], 200 if hovered else 140),
                     (0, 0, w, 3), border_radius=6)
    screen.blit(card, (x, y))

    # Sprite preview -- scale to fit if card is small
    sprite = sprites.get(char["key"])
    if sprite:
        bob = math.sin(timer * 2.5 + idx * 1.1) * 2
        # Scale sprite to max 44px on small cards
        max_sprite = 44 if h < 110 else 54
        sw, sh = sprite.get_size()
        if sw > max_sprite or sh > max_sprite:
            scale = min(max_sprite / sw, max_sprite / sh)
            sw2 = int(sw * scale)
            sh2 = int(sh * scale)
            sprite = pygame.transform.scale(sprite, (sw2, sh2))
            sw, sh = sw2, sh2
        sx = x + (w - sw) // 2
        sy = y + 8 + int(bob)
        screen.blit(sprite, (sx, sy))

    # Name (smaller on compact cards)
    name_y = y + (h - 30)
    name_size = 13 if h < 110 else 16
    draw_text(screen, char["name"], name_size, char["color"],
              x + w // 2, name_y, bold=True)

    # Role tag
    role_y = name_y + 14
    tag_font = get_font(9 if h < 110 else 10)
    tag_surf = tag_font.render(char["role"], True, (30, 50, 30))
    tw, th = tag_surf.get_size()
    tag_bg = pygame.Surface((tw + 6, th + 3), pygame.SRCALPHA)
    tag_bg.fill((*char["color"], 100))
    tag_x = x + (w - tw - 6) // 2
    screen.blit(tag_bg, (tag_x, role_y - 2))
    screen.blit(tag_surf, (tag_x + 3, role_y))


# ---------------------------------------------------------------------------
# Title Screen
# ---------------------------------------------------------------------------

class TitleScreen:
    def __init__(self) -> None:
        self.title_y: float = -60.0
        self.title_target_y: float = SCREEN_HEIGHT * 0.09
        self.prompt_timer: float = 0.0
        self._bg: pygame.Surface | None = None
        # Interactive character selection
        self._card_rects: list[tuple[pygame.Rect, dict]] = []
        self.selected_char: dict | None = None
        # Dropdown state: gallery is HIDDEN by default to keep menu clean
        self.gallery_open: bool = False
        self._gallery_button_rect: pygame.Rect | None = None
        # Speedrun mode toggle (menu option / flag)
        self.speedrun_mode: bool = False
        self._speedrun_btn_rect: pygame.Rect | None = None
        # Daily challenge (Feature #3)
        self.daily_mode: bool = False
        self._daily_btn_rect: pygame.Rect | None = None

    def update(self, dt: float) -> None:
        self.title_y += (self.title_target_y - self.title_y) * min(1.0, 4 * dt)
        self.prompt_timer += dt

    def handle_click(self, pos: tuple[int, int]) -> bool:
        """Handle mouse click. Returns True if consumed (don't start game)."""
        # If detail panel open, click anywhere closes it
        if self.selected_char is not None:
            self.selected_char = None
            return True
        # Gallery toggle button
        if (self._gallery_button_rect is not None
                and self._gallery_button_rect.collidepoint(pos)):
            self.gallery_open = not self.gallery_open
            return True
        # Speedrun toggle button
        if (self._speedrun_btn_rect is not None
                and self._speedrun_btn_rect.collidepoint(pos)):
            self.speedrun_mode = not self.speedrun_mode
            return True
        # Daily toggle button
        if (self._daily_btn_rect is not None
                and self._daily_btn_rect.collidepoint(pos)):
            self.daily_mode = not self.daily_mode
            return True
        # Click a character card -> detail popup (only if gallery is open)
        if self.gallery_open:
            for rect, char in self._card_rects:
                if rect.collidepoint(pos):
                    self.selected_char = char
                    return True
        return False

    def handle_key(self, key: int) -> bool:
        """Returns True if the key was consumed (don't start game)."""
        if self.selected_char is not None:
            if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN):
                self.selected_char = None
                return True
            return True  # any key closes
        # ESC closes the gallery (lets you see the clean title again)
        if self.gallery_open and key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.gallery_open = False
            return True
        if key in (pygame.K_s, pygame.K_S):
            self.speedrun_mode = not self.speedrun_mode
            return True
        if key in (pygame.K_d, pygame.K_D):
            self.daily_mode = not self.daily_mode
            return True
        return False

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

        # Title + juicy sparkles/leaves (non-gameplay feel matches gameplay)
        import math as m
        draw_text_shadow(screen, "BAMBOO FOREST", 54, (200, 255, 200),
                         SCREEN_WIDTH // 2, int(self.title_y), bold=True)
        draw_text(screen, "~ The Legend of Pain-da ~", 18, (120, 180, 120),
                  SCREEN_WIDTH // 2, int(self.title_y) + 32)
        # subtle title sparkles and leaves
        for i in range(7):
            sx = SCREEN_WIDTH//2 - 160 + (i * 55)
            sy = int(self.title_y) - 8 + int(m.sin(self.prompt_timer * 2.3 + i) * 5)
            pygame.draw.circle(screen, (255, 255, 200), (sx, sy), 2)
            if i % 3 == 0:
                pygame.draw.polygon(screen, (60, 130, 40), [(sx+18, sy+4), (sx+24, sy-2), (sx+21, sy+6)])

        self._card_rects.clear()
        mouse_pos = pygame.mouse.get_pos()

        # === DROPDOWN BUTTON (always visible) -- larger, juicier, touch friendly ===
        btn_w, btn_h = 360, 56
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        btn_y = int(SCREEN_HEIGHT * 0.30)
        self._gallery_button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        btn_hovered = self._gallery_button_rect.collidepoint(mouse_pos)
        # Rich gradient-ish bg (layered for depth + sparkle feel)
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        base = (35, 65, 35) if not btn_hovered else (55, 105, 55)
        btn_surf.fill((*base, 245))
        # Top highlight for gradient pop
        pygame.draw.rect(btn_surf, (70, 130, 70, 90), (2, 2, btn_w-4, 12), border_radius=4)
        pygame.draw.rect(btn_surf, (200, 255, 200), (0, 0, btn_w, btn_h), 3, border_radius=8)
        # Sparkle accents on hover
        if btn_hovered:
            for si in range(5):
                sx = 12 + (si * 67) % (btn_w - 24)
                sy = 8 + int(math.sin(self.prompt_timer * 6 + si) * 6)
                pygame.draw.circle(btn_surf, (255, 255, 220, 180), (sx, sy), 2)
        screen.blit(btn_surf, (btn_x, btn_y))
        arrow = "V" if not self.gallery_open else "^"
        label = ("View Characters  " + arrow) if not self.gallery_open else ("Hide Characters  " + arrow)
        draw_text_shadow(screen, label, 22, (230, 255, 230), btn_x + btn_w // 2, btn_y + btn_h // 2, bold=True)

        # === GALLERY (only when dropdown open) ===
        if self.gallery_open:
            # Dynamic: use 5 cols + scale card sizes via start_y/total_h math so 6 rows fit 960x540 with no clip
            # All cards remain clickable. Auto-shrink on dense.
            n = len(_CHARACTERS)
            cols = 5 if n > 18 else 4
            rows = (n + cols - 1) // cols
            gap_x = 5
            gap_y = 3
            btn_bottom = btn_y + btn_h
            gallery_top = btn_bottom + 6
            # leave room below for hint + prompt (prevents overlap)
            bottom_reserve = 54
            max_card_area_h = max(110, SCREEN_HEIGHT - gallery_top - bottom_reserve)
            max_panel_w = SCREEN_WIDTH - 44
            card_w = min(154, (max_panel_w - (cols - 1) * gap_x) // cols)
            card_w = max(110, card_w)
            card_h = min(56, (max_card_area_h - (rows - 1) * gap_y) // rows)
            card_h = max(40, card_h)
            if card_h < 45:
                gap_y = 2
                card_h = max(40, (max_card_area_h - (rows - 1) * gap_y) // rows)
            total_w = cols * card_w + (cols - 1) * gap_x
            total_h = rows * card_h + (rows - 1) * gap_y
            start_x = (SCREEN_WIDTH - total_w) // 2
            start_y = gallery_top
            # tight panel
            panel_h = total_h + 22
            panel = pygame.Surface((total_w + 14, panel_h), pygame.SRCALPHA)
            panel.fill((8, 16, 8, 230))
            pygame.draw.rect(panel, (88, 138, 88),
                             (0, 0, total_w + 14, panel_h),
                             2, border_radius=5)
            screen.blit(panel, (start_x - 7, start_y - 5))
            for i, char in enumerate(_CHARACTERS):
                col = i % cols
                row = i // cols
                cx = start_x + col * (card_w + gap_x)
                cy = start_y + row * (card_h + gap_y)
                rect = pygame.Rect(cx, cy, card_w, card_h)
                self._card_rects.append((rect, char))
                hovered = rect.collidepoint(mouse_pos)
                _draw_card(screen, char, cx, cy, card_w, card_h,
                           self.prompt_timer, i, hovered=hovered)
            # instruction hint (kept above prompt)
            hint_y = start_y + total_h + 4
            if hint_y < SCREEN_HEIGHT - 42:
                draw_text(screen, "Click card for story  •  ESC close",
                          9, (160, 190, 160), SCREEN_WIDTH // 2, hint_y)

        # Pulsing "Press ENTER" prompt (always; y adjusted when gallery open so no overlap with cards/hint)
        if self.gallery_open:
            prompt_y = SCREEN_HEIGHT - 32
            p_size = 16
        else:
            prompt_y = SCREEN_HEIGHT - 78
            p_size = 26
        alpha = int(128 + 127 * math.sin(self.prompt_timer * 3))
        font = get_font(p_size)
        prompt = font.render("Press ENTER to Start", True, (200, 255, 200))
        prompt.set_alpha(alpha)
        screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, prompt_y)))

        # Daily challenge button (Feature #3) -- above speedrun when closed
        if not self.gallery_open:
            dbtn_w, dbtn_h = 180, 22
            dbx = (SCREEN_WIDTH - dbtn_w) // 2
            dby = SCREEN_HEIGHT - 96
            self._daily_btn_rect = pygame.Rect(dbx, dby, dbtn_w, dbtn_h)
            don = self.daily_mode
            dbgc = (50, 90, 110) if don else (30, 45, 55)
            pygame.draw.rect(screen, dbgc, (dbx, dby, dbtn_w, dbtn_h), border_radius=4)
            pygame.draw.rect(screen, (140, 200, 220), (dbx, dby, dbtn_w, dbtn_h), 1, border_radius=4)
            dseed = ""
            try:
                import datetime
                dseed = str(int(datetime.date.today().strftime("%Y%m%d")))
            except Exception:
                dseed = "----"
            dlabel = f"DAILY {dseed} ON" if don else f"DAILY {dseed} (D)"
            draw_text(screen, dlabel, 12, (200, 230, 240) if don else (170, 190, 200), SCREEN_WIDTH // 2, dby + 11)

        # Speedrun Mode toggle (small pill, visible when gallery closed)
        if not self.gallery_open:
            btn_w, btn_h = 160, 22
            bx = (SCREEN_WIDTH - btn_w) // 2
            by = SCREEN_HEIGHT - 70
            self._speedrun_btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
            on = self.speedrun_mode
            bgc = (60, 110, 60) if on else (40, 50, 40)
            pygame.draw.rect(screen, bgc, (bx, by, btn_w, btn_h), border_radius=4)
            pygame.draw.rect(screen, (140, 200, 140), (bx, by, btn_w, btn_h), 1, border_radius=4)
            label = "SPEEDRUN: ON" if on else "SPEEDRUN: OFF  (S)"
            draw_text(screen, label, 12, (220, 255, 220) if on else (170, 190, 170), SCREEN_WIDTH // 2, by + 11)
            if on:
                draw_text(screen, "L: load ghost for levels", 10, (160, 200, 160), SCREEN_WIDTH // 2, by + 28)

        # Controls (only when gallery is closed -- else it overlaps)
        if not self.gallery_open:
            draw_text(screen,
                      "Arrows/WASD  |  SPACE jump  |  SHIFT dash  |  E attack  |  F11 fullscreen",
                      13, (90, 140, 90), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 48)
            best = get_best_score()
            if best > 0:
                draw_text_shadow(screen, f"Best: {best}", 18, COL_GOLD,
                                 SCREEN_WIDTH // 2, SCREEN_HEIGHT - 22)
            draw_text(screen, "O: Accessibility Options", 12, (140, 180, 140),
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 8)

        # Detail popup on top of everything
        if self.selected_char is not None:
            self._draw_detail(screen)

    def _draw_detail(self, screen: pygame.Surface) -> None:
        """Draw detail popup for the selected character."""
        char = self.selected_char
        # Dim the background
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 200))
        screen.blit(dim, (0, 0))

        # Panel
        pw, ph = 720, 440
        px = (SCREEN_WIDTH - pw) // 2
        py = (SCREEN_HEIGHT - ph) // 2
        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((15, 28, 18, 250))
        pygame.draw.rect(panel, char["color"], (0, 0, pw, ph), 3, border_radius=10)
        # Accent bar
        pygame.draw.rect(panel, (*char["color"], 220), (0, 0, pw, 8),
                        border_radius=10)
        screen.blit(panel, (px, py))

        # Big sprite (centered left side)
        sprites = _get_sprite_cache()
        sprite = sprites.get(char["key"])
        if sprite:
            sw, sh = sprite.get_size()
            scale = min(200 / sw, 200 / sh)
            big = pygame.transform.scale(sprite,
                                        (int(sw * scale), int(sh * scale)))
            bw, bh = big.get_size()
            screen.blit(big, (px + 40 + (200 - bw) // 2,
                             py + 80 + (200 - bh) // 2))

        # Name (big)
        draw_text_shadow(screen, char["name"], 42, char["color"],
                        px + pw // 2, py + 40, bold=True)

        # Role tag
        role_font = get_font(14, bold=True)
        role_surf = role_font.render(char["role"], True, (30, 50, 30))
        rw, rh = role_surf.get_size()
        tag_bg = pygame.Surface((rw + 16, rh + 6), pygame.SRCALPHA)
        tag_bg.fill((*char["color"], 220))
        screen.blit(tag_bg, (px + pw // 2 - (rw + 16) // 2, py + 66))
        screen.blit(role_surf, (px + pw // 2 - rw // 2, py + 68))

        # Story (word-wrapped)
        story = char.get("story", char.get("desc", ""))
        body_font = get_font(16)
        story_x = px + 280
        story_y = py + 100
        max_w = pw - 280 - 40
        self._draw_wrapped(screen, story, body_font, (220, 235, 220),
                          story_x, story_y, max_w)

        # Close hint
        hint = get_font(14).render(
            "Click anywhere or press ESC to close", True, (180, 180, 180))
        screen.blit(hint, hint.get_rect(
            center=(px + pw // 2, py + ph - 20)))

    def _draw_wrapped(self, screen: pygame.Surface, text: str,
                     font: pygame.font.Font, color: tuple,
                     x: int, y: int, max_width: int) -> None:
        """Draw text with word wrapping + paragraph support."""
        for paragraph in text.split("\n\n"):
            words = paragraph.split(" ")
            line: list[str] = []
            for w in words:
                test = " ".join(line + [w])
                if font.size(test)[0] > max_width and line:
                    line_surf = font.render(" ".join(line), True, color)
                    screen.blit(line_surf, (x, y))
                    y += font.get_height() + 2
                    line = [w]
                else:
                    line.append(w)
            if line:
                line_surf = font.render(" ".join(line), True, color)
                screen.blit(line_surf, (x, y))
                y += font.get_height() + 2
            y += 8  # paragraph spacing


# ---------------------------------------------------------------------------
# Pause Overlay
# ---------------------------------------------------------------------------

class PauseOverlay:
    """Pause screen with compact enemy encyclopedia (read while waiting)."""

    def draw(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        draw_text_shadow(screen, "PAUSED", 42, COL_WHITE,
                         SCREEN_WIDTH // 2, 36, bold=True)
        draw_text(screen, "ESC to Resume  |  Q to Quit  |  O Accessibility  |  G: The Grove  |  L: Load Ghost (speedrun)", 14, (180, 180, 180),
                  SCREEN_WIDTH // 2, 62)

        # Mini enemy encyclopedia -- compact grid of all characters
        # Use 5 cols + smaller cards on dense + start_y / row_h calc + pixel wrap to avoid clip/overflow on 960x540
        sprites = _get_sprite_cache()
        n = len(_CHARACTERS)
        cols = 5 if n > 18 else 4
        margin_x = 22
        col_w = max(126, min(152, (SCREEN_WIDTH - 2 * margin_x) // cols))
        row_h = 54 if n > 20 else 76
        start_x = (SCREEN_WIDTH - cols * col_w) // 2
        start_y = 78
        # Prevent bottom overflow: shrink row_h if needed for total_h fit
        rows_needed = (n + cols - 1) // cols
        max_bottom = SCREEN_HEIGHT - 18
        if start_y + rows_needed * row_h > max_bottom:
            row_h = max(44, (max_bottom - start_y - 2) // max(1, rows_needed))
        font_name = get_font(11, bold=True)
        font_desc = get_font(9)
        text_left = 50   # after sprite area
        text_max_w = col_w - text_left - 8
        for i, char in enumerate(_CHARACTERS):
            col = i % cols
            row = i // cols
            x = start_x + col * col_w
            y = start_y + row * row_h
            # Compact card
            cw = col_w - 6
            ch = row_h - 6
            card = pygame.Surface((cw, ch), pygame.SRCALPHA)
            card.fill((14, 24, 14, 232))
            pygame.draw.rect(card, (*char["color"], 155),
                             (0, 0, cw, ch), 1, border_radius=4)
            screen.blit(card, (x, y))
            # Small sprite (scale down on tiny cards)
            sprite = sprites.get(char["key"])
            if sprite:
                ss = 36 if row_h < 56 else 40
                sm = pygame.transform.scale(sprite, (ss, ss))
                screen.blit(sm, (x + 6, y + 8))
            # Name + role
            name = font_name.render(char["name"], True, char["color"])
            screen.blit(name, (x + text_left, y + 6))
            role = font_desc.render(char["role"], True, (155, 195, 155))
            screen.blit(role, (x + text_left, y + 18))
            # Proper pixel-width wrap (prevents text spilling out of cards)
            desc = char["desc"]
            words = desc.split()
            lines = []
            cur = ""
            for w in words:
                test = (cur + " " + w).strip()
                if font_desc.size(test)[0] <= text_max_w and len(lines) < 2:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    cur = w
                    if len(lines) >= 2:
                        break
            if cur and len(lines) < 2:
                lines.append(cur)
            for li, ln in enumerate(lines[:2]):
                d = font_desc.render(ln, True, (195, 205, 195))
                screen.blit(d, (x + text_left, y + 32 + li * 10))

        # Simple scroll hint for dense lists (no real scroll; all visible via shrink)
        if rows_needed > 4:
            draw_text(screen, "encyclopedia • all visible", 9, (130, 150, 130),
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)


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
# Confetti for juicy non-gameplay victory (gradients, sparkles, leaves theme)
# ---------------------------------------------------------------------------

class _Confetto:
    def __init__(self, x: float, y: float) -> None:
        import random
        self.x = x
        self.y = y
        self.vx = random.uniform(-120, 120)
        self.vy = random.uniform(-80, 40)
        self.life = random.uniform(2.2, 3.8)
        self.max_life = self.life
        self.color = random.choice([
            (255, 215, 0), (76, 153, 0), (255, 120, 180), (140, 220, 255), (255, 180, 80)
        ])
        self.size = random.uniform(3, 7)
        self.rot = random.uniform(0, 360)
        self.rot_speed = random.uniform(-180, 180)
        self.shape = random.choice(["rect", "leaf", "spark"])

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 180 * dt  # gravity
        self.vx *= 0.995
        self.life -= dt
        self.rot += self.rot_speed * dt

    def draw(self, screen: pygame.Surface) -> None:
        if self.life <= 0:
            return
        a = max(30, int(255 * (self.life / self.max_life)))
        c = (*self.color, a) if len(self.color) == 3 else self.color
        cx, cy = int(self.x), int(self.y)
        s = max(2, int(self.size * (self.life / self.max_life + 0.2)))
        if self.shape == "spark":
            pygame.draw.circle(screen, self.color, (cx, cy), s)
            pygame.draw.circle(screen, (255,255,255), (cx-1, cy-1), max(1, s//2))
        elif self.shape == "leaf":
            surf = pygame.Surface((s+4, s+2), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (*self.color, a), (0, 0, s+4, max(1, s//2)))
            rot = pygame.transform.rotate(surf, self.rot)
            screen.blit(rot, (cx - rot.get_width()//2, cy - rot.get_height()//2))
        else:
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            surf.fill((*self.color, a))
            rot = pygame.transform.rotate(surf, self.rot)
            screen.blit(rot, (cx - rot.get_width()//2, cy - rot.get_height()//2))


class VictoryScreen:
    def __init__(self) -> None:
        self.timer: float = 0.0
        self.confetti: list[_Confetto] = []

    def update(self, dt: float) -> None:
        self.timer += dt
        # spawn juicy confetti + leaves + sparkles over time
        import random
        while len(self.confetti) < 42 and random.random() < 0.85:
            self.confetti.append(_Confetto(
                random.uniform(40, SCREEN_WIDTH-40),
                random.uniform(-20, SCREEN_HEIGHT * 0.45)
            ))
        for c in self.confetti[:]:
            c.update(dt)
            if c.life <= 0:
                self.confetti.remove(c)

    def draw(self, screen: pygame.Surface, final_score: int,
             is_high_score: bool,
             speedrun_time: float | None = None,
             best_time: float | None = None,
             has_ghost: bool = False) -> None:
        # Richer gradient + subtle leaves/sparkle bg
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(12 + 14 * (1 - t))
            g = int(38 + 22 * (1 - t))
            b = int(18 + 8 * (1 - t))
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        # ambient sparkles and leaves (non-gameplay juicy)
        import random, math as m
        for i in range(8):
            sx = (SCREEN_WIDTH * 0.2 + (i * 97) % (SCREEN_WIDTH * 0.6)) + m.sin(self.timer * 1.6 + i) * 12
            sy = 80 + ((i * 47) % 160) + m.cos(self.timer * 2 + i) * 8
            pygame.draw.circle(screen, (255, 235, 120), (int(sx), int(sy)), 2)
            if i % 2 == 0:
                lx = sx + 40
                ly = sy + 30 + m.sin(self.timer*3 + i)*4
                pygame.draw.polygon(screen, (70, 140, 50), [(lx, ly), (lx+7, ly-5), (lx+3, ly+4)])

        # draw falling confetti
        for c in self.confetti:
            c.draw(screen)

        bounce = math.sin(self.timer * 3) * 8
        draw_text_shadow(screen, "VICTORY!", 72, COL_GOLD,
                         SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.28 + bounce), bold=True)
        draw_text(screen, f"Final Score: {final_score}", 36, COL_WHITE,
                  SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.48))
        if is_high_score:
            alpha = int(128 + 127 * math.sin(self.timer * 5))
            font = get_font(28, bold=True)
            surf = font.render("NEW HIGH SCORE!", True, COL_GOLD)
            # Proper per-pixel alpha for antialiased text: draw on SRCALPHA then blit
            alpha_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            alpha_surf.blit(surf, (0, 0))
            alpha_surf.set_alpha(alpha)
            screen.blit(alpha_surf, alpha_surf.get_rect(center=(
                SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.56))))
        # Speedrun ghost feedback (polish)
        if speedrun_time is not None:
            m = int(speedrun_time // 60)
            s = speedrun_time % 60
            ts = f"{m}:{s:05.2f}" if m else f"{s:05.2f}"
            draw_text(screen, f"YOUR TIME: {ts}", 20, COL_GOLD, SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.58))
            if best_time is not None:
                bm = int(best_time // 60)
                bs = best_time % 60
                bts = f"{bm}:{bs:05.2f}" if bm else f"{bs:05.2f}"
                draw_text(screen, f"BEST: {bts}", 16, (200, 210, 170), SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.58) + 22)
            if has_ghost:
                draw_text(screen, "GHOST RECORDED  •  R to replay  •  Y save", 14, (170, 190, 160),
                          SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.78) - 22)
        draw_text(screen, "Press ENTER to Play Again", 24, (180, 180, 180),
                  SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.78))


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
        # Richer transition: deep gradient + sparkles + rising leaves (juicy non-gameplay)
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(8 + 12 * t)
            g = int(22 + 18 * t)
            b = int(12 + 6 * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        tt = self.timer / self.duration
        alpha = int(255 * (1 - abs(tt - 0.5) * 2))
        alpha = max(20, min(255, alpha))  # floor so first frame isn't pure black
        import math as m
        # drifting sparkles
        for i in range(12):
            sx = (80 + (i * 71) % (SCREEN_WIDTH - 160)) + m.sin(self.timer * 2.2 + i) * 18
            sy = 60 + ((i * 31) % 420) * (0.6 + 0.4 * m.sin(tt * 3))
            a = int(alpha * (0.6 + 0.4 * m.sin(self.timer * 7 + i)))
            pygame.draw.circle(screen, (255, 250, 180), (int(sx), int(sy)), 2)
        # rising leaves
        for i in range(6):
            lx = 100 + (i * 130) % (SCREEN_WIDTH - 200)
            ly = (SCREEN_HEIGHT - 80) - ((self.timer * 110 + i * 60) % 380)
            pygame.draw.polygon(screen, (65, 135, 45), [
                (lx, ly), (lx + 6, ly - 5), (lx + 2, ly + 3)
            ])

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


# ---------------------------------------------------------------------------
# Basic Accessibility Options overlay (keyboard driven, persistent profile)
# Reachable with O from title or pause. Simple +/- style.
# ---------------------------------------------------------------------------

class AccessibilityOptions:
    """Basic options screen. Game owns the live settings dict and selected index.
    Reachable via O on title/pause. Minimal: particle density, shake intensity, text scale, reduced motion.
    """

    OPTION_KEYS = [
        "particle_density",
        "shake_intensity",
        "text_scale",
        "reduced_motion",
    ]
    OPTION_TITLES = [
        "Particle Density",
        "Shake Intensity",
        "Text Scale",
        "Reduced Motion",
    ]

    def __init__(self) -> None:
        self.selected: int = 0

    def draw(self, screen: pygame.Surface, settings: dict) -> None:
        # Dim background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))

        draw_text_shadow(screen, "ACCESSIBILITY", 36, COL_WHITE,
                         SCREEN_WIDTH // 2, 48, bold=True)
        draw_text(screen, "Arrows: select + adjust   |   ESC: back", 14, (180, 200, 180),
                  SCREEN_WIDTH // 2, 78)

        start_y = 120
        for i, (key, title) in enumerate(zip(self.OPTION_KEYS, self.OPTION_TITLES)):
            y = start_y + i * 48
            is_sel = (i == self.selected)
            val = settings.get(key, 1.0 if "scale" in key or "intensity" in key or "speed" in key else 0)
            label = ACCESSIBILITY_LABELS.get(key, lambda v: str(v))(val)

            # Selection highlight bar
            if is_sel:
                bar = pygame.Surface((520, 38), pygame.SRCALPHA)
                bar.fill((30, 70, 30, 200))
                pygame.draw.rect(bar, (120, 200, 120), (0, 0, 520, 38), 2, border_radius=4)
                screen.blit(bar, ((SCREEN_WIDTH - 520) // 2, y - 8))

            col = (220, 255, 220) if is_sel else (170, 200, 170)
            draw_text_left(screen, title, 20, col, SCREEN_WIDTH // 2 - 200, y, bold=is_sel)
            draw_text(screen, label, 20, COL_GOLD if is_sel else COL_WHITE,
                      SCREEN_WIDTH // 2 + 120, y, bold=True)

        # Footer
        draw_text(screen, "Changes save automatically to profile", 13, (140, 160, 140),
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 36)


# ---------------------------------------------------------------------------
# Grove: full functional combine bench. Select 2-3 essences (biome keys),
# match exact recipe set from config.RECIPES, spend specifically, unlock graft,
# persist + apply immediately to player (glide_efficiency, lava_resist,
# dash_mastery, ice_armor + legacy). Nice UI: selection, bench slots, flash on craft, messages.
# Root and web/ kept identical for parity.
# ---------------------------------------------------------------------------

GRAFT_DEFS: dict[str, str] = {
    "glide_efficiency": "Glide Efficiency — slower fall while gliding (stronger lift)",
    "lava_resist": "Lava Resist — rising lava deals heavy damage instead of instant death",
    "dash_mastery": "Dash Mastery — shorter cooldown between dashes",
    "ice_armor": "Ice Armor — resist hazards + minor defense",
    "hp_boost": "+1 HP — start runs with an extra hit point",
    "weak_glide": "Weak Glide — permanent light slow-fall",
    "combo_bonus": "Combo Bonus — slightly stronger bamboo combos",
    "bamboo_yield": "Bamboo Yield — +10 score per bamboo collected",
}

# Nice labels for biome keys (used for display)
BIOME_LABELS: dict[str, str] = {
    "forest": "Bamboo Grove",
    "corrupted": "Corrupted Thicket",
    "lair": "Mutant Lair",
    "volcanic": "The Caldera",
    "basalt": "Basalt Columns",
    "desert": "The Arid Rift",
    "cave": "Karst Caves",
    "salt": "Salt Flats",
    "mushroom": "Fungal Hollows",
    "forge": "The Crucible",
    "tidal": "Tidal Locks",
    "void": "Phantom Corridor",
    "gravity": "The Gravity Engine",
}


class GroveUI:
    """Combine bench for Grove grafting.
    Pick 2-3 essences from available biome essences.
    Recipes in config.RECIPES define exact multisets -> graft id.
    Supports selection, bench slots (2-3), craft, flash success, messages.
    Keyboard driven. Spends exactly via spend_specific_essences.
    """

    def __init__(self) -> None:
        self.essences: dict[str, int] = {}
        self.grafts: list[str] = []
        self.cursor: int = 0
        self.bench: list[str] = []
        self.message: str = ""
        self.message_timer: float = 0.0
        self.craft_flash: float = 0.0  # >0 = visual success flash

    def refresh(self) -> None:
        self.essences, self.grafts = get_profile_essences_and_grafts()
        self.cursor = 0
        self.bench = []
        self.craft_flash = 0.0
        total = sum(self.essences.values())
        self.message = f"THE GROVE — Combine Bench. Essence: {total}. Pick 2-3 to craft."
        self.message_timer = 4.0

    def update(self, dt: float) -> None:
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
        if self.craft_flash > 0:
            self.craft_flash -= dt

    def _get_available(self) -> list[tuple[str, int]]:
        av = []
        for k in ESSENCE_BIOME_KEYS:
            c = self.essences.get(k, 0)
            if c > 0:
                av.append((k, c))
        return av

    def handle_key(self, key: int) -> str | None:
        """Handle input. Returns 'exit' or 'crafted'."""
        avail = self._get_available()
        n = len(avail)
        if key in (pygame.K_ESCAPE, pygame.K_g):
            return "exit"
        if n == 0:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                return "exit"
            return None

        if key in (pygame.K_UP, pygame.K_w):
            self.cursor = (self.cursor - 1) % n
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.cursor = (self.cursor + 1) % n
        elif key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_a):
            # add current to bench (if room + not duplicate)
            if len(self.bench) < 3:
                ek = avail[self.cursor][0]
                if ek not in self.bench:
                    self.bench.append(ek)
                    self.message = ""
        elif key in (pygame.K_r, pygame.K_BACKSPACE):
            if self.bench:
                self.bench.pop()
        elif key in (pygame.K_c, pygame.K_RETURN) and 2 <= len(self.bench) <= 3:
            return self._attempt_craft()
        return None

    def _attempt_craft(self) -> str | None:
        if len(self.bench) < 2 or len(self.bench) > 3:
            self.message = "Select exactly 2 or 3 essences."
            self.message_timer = 2.0
            return None
        chosen = sorted(self.bench)
        for rec in RECIPES:
            if sorted(rec.get("essences", [])) == chosen:
                gid = rec["graft"]
                if gid in self.grafts:
                    self.message = "Already unlocked that graft."
                    self.message_timer = 2.0
                    return None
                if not spend_specific_essences(chosen):
                    self.message = "Could not spend those essences."
                    self.message_timer = 2.0
                    return None
                if unlock_graft(gid):
                    self.craft_flash = 0.9
                    self.message = f"CRAFTED: {rec['name']} !"
                    self.message_timer = 3.0
                    self.essences, self.grafts = get_profile_essences_and_grafts()
                    self.bench = []
                    return "crafted"
                else:
                    self.message = "Unlock failed."
                    self.message_timer = 2.0
                    return None
        self.message = "No recipe matches that combination."
        self.message_timer = 2.5
        return None

    def draw(self, screen: pygame.Surface) -> None:
        # Dark grove backdrop
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 18, 12, 245))
        screen.blit(overlay, (0, 0))

        title_col = (255, 240, 180) if self.craft_flash > 0 else (140, 220, 160)
        draw_text_shadow(screen, "THE GROVE — COMBINE BENCH", 38, title_col,
                         SCREEN_WIDTH // 2, 28, bold=True)
        total_ess = sum(self.essences.values())
        draw_text(screen, f"Essence: {total_ess}  •  Select 2-3  •  A=add  R=remove  C=craft  ESC/G=leave", 13,
                  (160, 190, 160), SCREEN_WIDTH // 2, 54)

        avail = self._get_available()
        # Left column: available essences
        y = 85
        draw_text(screen, "AVAILABLE ESSENCES", 15, COL_GOLD, 110, y)
        y += 20
        if not avail:
            draw_text_left(screen, "(none — collect bamboo in runs)", 13, (130, 140, 130), 60, y)
            y += 18
        for i, (k, cnt) in enumerate(avail):
            prefix = ">" if i == self.cursor else " "
            col = (255, 255, 180) if i == self.cursor else (200, 230, 200)
            label = BIOME_LABELS.get(k, k)
            line = f"{prefix} {label} x{cnt}"
            draw_text_left(screen, line, 14, col, 60, y)
            y += 17

        # Bench (center-right)
        bx = SCREEN_WIDTH // 2 + 40
        by = 85
        draw_text(screen, "COMBINE BENCH (2-3)", 15, COL_GOLD, bx + 90, by)
        by += 22
        # slots
        for si in range(3):
            slot = self.bench[si] if si < len(self.bench) else None
            slot_label = BIOME_LABELS.get(slot, slot) if slot else "—"
            col = (120, 255, 140) if slot else (90, 110, 90)
            if self.craft_flash > 0 and slot:
                col = (255, 255, 200)
            draw_text_left(screen, f"[{si+1}] {slot_label}", 14, col, bx, by)
            by += 18
        # preview match
        if 2 <= len(self.bench) <= 3:
            ch = sorted(self.bench)
            match = None
            for rec in RECIPES:
                if sorted(rec.get("essences", [])) == ch:
                    match = rec
                    break
            if match:
                draw_text_left(screen, f"→ {match['name']}: {match['desc']}", 12, (180, 255, 180), bx, by)
            else:
                draw_text_left(screen, "→ no matching recipe", 12, (200, 160, 160), bx, by)
            by += 18

        # Owned grafts (right)
        rx = SCREEN_WIDTH - 260
        ry = 85
        draw_text(screen, "YOUR GRAFTS", 15, COL_GOLD, rx + 40, ry)
        ry += 18
        owned = [g for g in self.grafts if g in GRAFT_DEFS]
        if owned:
            for gid in owned[-7:]:
                draw_text_left(screen, f"✓ {GRAFT_DEFS.get(gid, gid)[:28]}", 11, (90, 210, 110), rx, ry)
                ry += 14
        else:
            draw_text_left(screen, "(none — craft some!)", 11, (120, 130, 120), rx, ry)

        # Controls
        cy = max(ry + 10, 280)
        draw_text(screen, "UP/DOWN: select essence   A/SPACE: add to bench   R: remove last   C/ENTER: craft   G/ESC: leave", 11,
                  (150, 180, 150), SCREEN_WIDTH // 2, cy + 8)

        # Flash banner on craft success
        if self.craft_flash > 0:
            a = int(200 * min(1.0, self.craft_flash / 0.3))
            flash_bg = pygame.Surface((340, 32), pygame.SRCALPHA)
            flash_bg.fill((40, 80, 30, a))
            pygame.draw.rect(flash_bg, (140, 255, 140), (0, 0, 340, 32), 2, border_radius=4)
            screen.blit(flash_bg, ((SCREEN_WIDTH - 340) // 2, SCREEN_HEIGHT - 92))
            draw_text(screen, "GRAFT UNLOCKED — APPLIED!", 16, (200, 255, 200),
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 78, bold=True)

        # Message
        if self.message and self.message_timer > 0:
            mcol = (255, 255, 200) if self.craft_flash <= 0 else (180, 255, 180)
            draw_text_shadow(screen, self.message, 16, mcol,
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT - 48)

        # Footer
        draw_text(screen, "Essence earned from bamboo + biome clears. Grafts are permanent.", 10,
                  (100, 130, 100), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 22)
