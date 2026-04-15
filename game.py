"""Bamboo Forest - Main game entry point and loop."""

from __future__ import annotations

import math
import sys

import pygame

from config import (
    COL_GOLD, CRYSTAL_RADIUS, DARK_RADIUS, DOUBLE_JUMP_LEVEL,
    ENEMY_STOMP_BOUNCE, FPS, FLOOR_Y, GEYSER_LAUNCH, HEAL_AMOUNT,
    LEVEL_COUNT, PLAYER_DAMAGE, PLAYER_MAX_HP, SCREEN_HEIGHT,
    SCREEN_WIDTH, STARTING_LIVES, STOMP_SCORE, ST_GAME_OVER,
    ST_LEVEL_TRANS, ST_MENU, ST_PAUSED, ST_PLAYING, ST_VICTORY,
    SULFUR_TRAIL_DMG, THERMAL_FORCE, TITLE, BOSS_KILL_SCORE,
)
from audio import AudioManager
from backgrounds import BiomeBackground
from engine import Camera, ParticleSystem, ScreenShake
from levels import build_level_state, LevelState
from save import save_high_score
from sprites import BambooShuriken, BambooStaff, Player
from ui import (
    DeathAnimation, GameOverScreen, HUD, LevelTransition,
    PauseOverlay, TitleScreen, VictoryScreen,
)


class Game:
    """Main game class -- owns the loop and state machine."""

    def __init__(self) -> None:
        pygame.init()
        # SCALED is required for toggle_fullscreen(). Try with vsync first,
        # then without, then fall back to plain mode.
        for flags, vs in [
            (pygame.SCALED | pygame.DOUBLEBUF, 1),
            (pygame.SCALED, 0),
            (pygame.DOUBLEBUF, 0),
        ]:
            try:
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=vs)
                break
            except pygame.error:
                continue
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.audio = AudioManager()
        self.background: BiomeBackground = BiomeBackground("forest")
        self.shake = ScreenShake()

        self.title_screen = TitleScreen()
        self.pause_overlay = PauseOverlay()
        self.game_over_screen = GameOverScreen()
        self.victory_screen = VictoryScreen()

        self.state: str = ST_MENU
        self.player: Player | None = None
        self.level: LevelState | None = None
        self.current_level: int = 0
        self.camera: Camera | None = None
        self.particles: ParticleSystem = ParticleSystem()
        self.hud: HUD = HUD()
        self.level_transition: LevelTransition | None = None
        self.death_anim: DeathAnimation | None = None
        self.running = True

        self.lives: int = STARTING_LIVES
        self.respawn_x: int = 100
        self.respawn_y: int = FLOOR_Y
        self._total_score: int = 0

        self._carry_score: int = 0
        self._carry_health: int = 0
        self._was_on_ground: bool = False
        self._is_high_score: bool = False
        self._jump_pressed: bool = False
        self._boss_warning_timer: float = 0.0
        self._fullscreen: bool = False
        self._debug_mode: bool = False
        # Tutorial hints
        self._weapon_tutorial_timer: float = 0.0
        self._weapon_used: bool = False
        # Hitstop: brief pause on enemy hit for impact feel
        self._hitstop_timer: float = 0.0
        # Level-end outro: Pain-da auto-runs off screen after reaching goal
        self._outro_active: bool = False
        self._outro_timer: float = 0.0
        self._outro_speed: float = 240.0

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # Global toggles (work in any state)
                if event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                    continue
                if event.key == pygame.K_TAB:
                    self._debug_mode = not self._debug_mode
                    continue
                self._on_key_down(event.key)
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._jump_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.state == ST_MENU:
                    # Clicking a character card opens the detail popup
                    self.title_screen.handle_click(event.pos)
                elif event.button == 1 and self.state == ST_PLAYING:
                    if self.player and self.player.attack():
                        self.audio.play("stomp")
                        self._weapon_used = True
                        self._weapon_tutorial_timer = 0.0

    def _toggle_fullscreen(self) -> None:
        """Toggle fullscreen using pygame.display.toggle_fullscreen().

        This only works because the window was initialised with pygame.SCALED
        flag. Preserves the same Surface reference -- no set_mode reinit.
        """
        try:
            pygame.display.toggle_fullscreen()
            self._fullscreen = not self._fullscreen
        except pygame.error:
            # Fallback: explicit set_mode reinit
            self._fullscreen = not self._fullscreen
            flags = pygame.SCALED | pygame.DOUBLEBUF
            if self._fullscreen:
                flags |= pygame.FULLSCREEN
            try:
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)
            except pygame.error:
                self._fullscreen = False
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)

    def _on_key_down(self, key: int) -> None:
        if self.state == ST_MENU:
            # If title screen detail popup is open, ESC closes it (not app)
            if self.title_screen.handle_key(key):
                return
            if key == pygame.K_RETURN:
                self._start_game()
                self.audio.play("menu_select")
            elif key == pygame.K_ESCAPE:
                self.running = False
        elif self.state == ST_PLAYING:
            if key == pygame.K_ESCAPE:
                self.state = ST_PAUSED
                self.audio.play("menu_select")
            elif key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if not self._jump_pressed and self.player:
                    if self.player.jump():
                        self.audio.play("jump")
                    self._jump_pressed = True
            elif key in (pygame.K_e, pygame.K_x):
                if self.player and self.player.attack():
                    self.audio.play("stomp")
                    self._weapon_used = True
                    self._weapon_tutorial_timer = 0.0
            elif key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                if self.player and self.player.dash():
                    self.audio.play("jump")
                    self.particles.emit_dust(
                        self.player.rect.centerx, self.player.rect.bottom)
            elif key == pygame.K_DOWN or key == pygame.K_s:
                if self.player and self.player.slam():
                    self.audio.play("stomp")
            elif key in (pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_q):
                if self.player and self.player.throw_bamboo():
                    self.audio.play("stomp")
        elif self.state == ST_PAUSED:
            if key == pygame.K_ESCAPE:
                self.state = ST_PLAYING
            elif key == pygame.K_q:
                self.state = ST_MENU
                self.title_screen = TitleScreen()
        elif self.state in (ST_GAME_OVER, ST_VICTORY):
            if key == pygame.K_RETURN:
                self.state = ST_MENU
                self.title_screen = TitleScreen()

    # ------------------------------------------------------------------
    # Level management
    # ------------------------------------------------------------------

    def _start_game(self) -> None:
        self.lives = STARTING_LIVES
        self.current_level = 0
        self._total_score = 0
        self.respawn_x = 100
        self.respawn_y = FLOOR_Y
        self._load_level(0)

    def _load_level(self, level_num: int) -> None:
        self.level = build_level_state(level_num)
        self.camera = Camera(self.level.world_width, SCREEN_HEIGHT)
        self.background = BiomeBackground(self.level.biome)
        self.respawn_x = self.level.player_start[0]
        self.respawn_y = self.level.player_start[1]
        self.player = Player(self.respawn_x, self.respawn_y)
        if level_num >= DOUBLE_JUMP_LEVEL:
            self.player.has_double_jump = True
        # Glide unlocks at level 4+ (Caldera -- wider gap traversal)
        if level_num >= 3:
            self.player.has_glide = True
        if self.level.is_icy:
            self.player.friction_mode = "ice"
        else:
            self.player.friction_mode = "normal"
        self.player.reset_state()  # clear input locks, dash, attack flags
        self.player.score = self._total_score
        self.level.all_sprites.add(self.player)
        self.current_level = level_num
        self.particles = ParticleSystem()
        self.hud = HUD()
        self.hud.set_bamboo_count(len(self.level.bamboos))
        self.hud.lives = self.lives
        self.death_anim = None
        self._was_on_ground = False
        self._jump_pressed = False
        self._outro_active = False
        self._outro_timer = 0.0
        # If player already has weapon from previous level, keep tutorial hidden
        if self.player.has_bamboo_weapon:
            self._weapon_used = True
        self.state = ST_PLAYING

    def _respawn_at_checkpoint(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            save_high_score(self._total_score, self.current_level + 1)
            self.game_over_screen = GameOverScreen()
            self.state = ST_GAME_OVER
            self.death_anim = None
            return
        activated_xs = set()
        if self.level:
            for cp in self.level.checkpoints:
                if cp.activated:
                    activated_xs.add(cp.spawn_x)
        self.level = build_level_state(self.current_level)
        self.camera = Camera(self.level.world_width, SCREEN_HEIGHT)
        self.background = BiomeBackground(self.level.biome)
        for cp in self.level.checkpoints:
            if cp.spawn_x in activated_xs:
                cp.activate()
        self.player = Player(self.respawn_x, self.respawn_y)
        if self.current_level >= DOUBLE_JUMP_LEVEL:
            self.player.has_double_jump = True
        # Glide unlocks at level 4+ (Caldera -- wider gap traversal)
        if self.current_level >= 3:
            self.player.has_glide = True
        if self.level.is_icy:
            self.player.friction_mode = "ice"
        else:
            self.player.friction_mode = "normal"
        self.player.reset_state()
        self.player.score = self._total_score
        self.level.all_sprites.add(self.player)
        self.particles = ParticleSystem()
        self.hud = HUD()
        self.hud.set_bamboo_count(len(self.level.bamboos))
        self.hud.lives = self.lives
        self.death_anim = None
        self._was_on_ground = False
        self._jump_pressed = False
        self.state = ST_PLAYING

    def _advance_level(self) -> None:
        self._total_score = self.player.score
        next_lv = self.current_level + 1
        if next_lv >= LEVEL_COUNT:
            self._is_high_score = save_high_score(
                self.player.score, self.current_level + 1)
            self.victory_screen = VictoryScreen()
            self.state = ST_VICTORY
            self.audio.play("victory")
        else:
            self._carry_score = self.player.score
            self._carry_health = self.player.health
            self.level_transition = LevelTransition(next_lv + 1)
            self.state = ST_LEVEL_TRANS
            self.audio.play("menu_select")

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def _update(self, dt: float) -> None:
        if self.state == ST_MENU:
            self.title_screen.update(dt)
        elif self.state == ST_LEVEL_TRANS:
            if self.level_transition and self.level_transition.update(dt):
                next_num = self.current_level + 1
                self._total_score = self._carry_score
                self._load_level(next_num)
                self.player.score = self._carry_score
                self.player.health = self._carry_health
        elif self.state == ST_PLAYING:
            self._update_gameplay(dt)
        elif self.state == ST_GAME_OVER:
            self.game_over_screen.update(dt)
            self.particles.update(dt)
        elif self.state == ST_VICTORY:
            self.victory_screen.update(dt)

    def _update_gameplay(self, dt: float) -> None:
        if not self.player or not self.level or not self.camera:
            return

        # Hitstop freezes game briefly on impact for weight/juice
        if self._hitstop_timer > 0:
            self._hitstop_timer -= dt
            return

        # DEFENSIVE: Never let input_locked stay stuck forever.
        # If player is on ground + not dashing + not in knockback, clear it.
        if (self.player.input_locked
                and self.player.is_on_ground
                and not self.player.is_dashing
                and self.player.knockback_timer <= 0):
            self.player.input_locked = False

        effective_dt = dt
        if self.death_anim:
            effective_dt = dt * self.death_anim.get_time_scale()
            if self.death_anim.update(dt):
                self._total_score = self.player.score
                self._respawn_at_checkpoint()
                return

        # Moving platforms -- player inherits platform velocity when standing on it.
        # Critical: detect riding BEFORE the platform moves, then TELEPORT player
        # to stay on platform surface. Fixes vertical-platform fall-through.
        for mp in self.level.moving_platforms:
            old_mx, old_my = mp.rect.x, mp.rect.y
            # Broader riding test: player must be touching platform top within 6px
            feet_y = self.player.rect.bottom
            plat_top = old_my
            horiz_overlap = (self.player.rect.right > old_mx - 2
                             and self.player.rect.left < old_mx + mp.rect.w + 2)
            was_riding = (horiz_overlap and -6 <= (feet_y - plat_top) <= 6)
            mp.update_moving(effective_dt)
            if was_riding:
                dx = mp.rect.x - old_mx
                dy = mp.rect.y - old_my
                self.player.rect.x += dx
                # Snap player bottom to platform top exactly (anti-clip)
                self.player.rect.bottom = mp.rect.top
                # Kill any downward velocity so gravity doesn't fight the platform
                if self.player.velocity_y > 0:
                    self.player.velocity_y = 0
                self.player.is_on_ground = True

        # Player
        keys = pygame.key.get_pressed()
        self.player.update(effective_dt, keys, self.level.platforms)

        # Landing dust
        if self.player.is_on_ground and not self._was_on_ground:
            self.particles.emit_dust(self.player.rect.centerx, self.player.rect.bottom)
        self._was_on_ground = self.player.is_on_ground

        # Enemies
        for enemy in list(self.level.enemies):
            enemy.update(effective_dt, self.level.platforms, self.player)

        # Boss
        if self.level.boss and self.level.boss.alive():
            self.level.boss.update(effective_dt, self.player, self.level.platforms)

        # =============================================================
        # BIOME MECHANICS
        # =============================================================

        # --- Geysers (Level 4: Caldera) ---
        for geyser in self.level.geysers:
            geyser.update(effective_dt)
            if geyser.is_active() and pygame.sprite.collide_rect(self.player, geyser):
                self.player.velocity_y = GEYSER_LAUNCH
                self.player.is_on_ground = False
                self.player.jumps_remaining = 0
                self.particles.emit_sparkle(geyser.rect.centerx, geyser.rect.top)
                self.audio.play("geyser")

        # --- Toxic trails (Level 4: SulfurSlime) ---
        for enemy in self.level.enemies:
            if hasattr(enemy, "get_new_trails"):
                for trail in enemy.get_new_trails():
                    self.level.toxic_trails.add(trail)
                    self.level.all_sprites.add(trail)
        self.level.toxic_trails.update(effective_dt)
        for trail in pygame.sprite.spritecollide(
                self.player, self.level.toxic_trails, False):
            if self.player.take_damage(SULFUR_TRAIL_DMG):
                self.shake.trigger(4, 0.1)
                self.audio.play("hit")

        # --- Crumbling platforms (Level 5: Basalt) ---
        for cp in self.level.crumbling:
            if cp.solid and self.player.is_on_ground:
                feet = self.player.get_stomp_rect()
                test = pygame.Rect(cp.rect.x - 2, cp.rect.y - 4, cp.rect.w + 4, 8)
                if feet.colliderect(test):
                    cp.touch()
            cp.update(effective_dt)

        # --- Wind zones (Level 6: Desert) ---
        for wz in self.level.wind_zones:
            if pygame.sprite.collide_rect(self.player, wz):
                self.player.rect.x += math.floor(wz.get_push() * effective_dt)
                self.player.rect.x = max(
                    0, min(self.player.rect.x,
                           self.level.world_width - self.player.rect.width))

        # --- Thermal updrafts (Level 6: Desert) ---
        for tu in self.level.updrafts:
            if pygame.sprite.collide_rect(self.player, tu):
                self.player.velocity_y = max(
                    self.player.velocity_y + THERMAL_FORCE * effective_dt,
                    THERMAL_FORCE)

        # --- Projectiles (Level 6: CactusScorpion) ---
        for enemy in self.level.enemies:
            if hasattr(enemy, "get_new_projectiles"):
                for proj in enemy.get_new_projectiles():
                    self.level.projectiles.add(proj)
                    self.level.all_sprites.add(proj)
        self.level.projectiles.update(effective_dt)
        for proj in pygame.sprite.spritecollide(
                self.player, self.level.projectiles, True):
            if self.player.take_damage(PLAYER_DAMAGE):
                self.shake.trigger()
                self.audio.play("hit")

        # --- Crystal interaction (Level 7: Cave) ---
        for crystal in self.level.crystals:
            crystal.update(effective_dt)
            if (not crystal.is_lit()
                    and pygame.sprite.collide_rect(self.player, crystal)):
                crystal.strike()
                self.particles.emit_sparkle(crystal.rect.centerx, crystal.rect.centery)
                self.audio.play("crystal")

        # --- NPCs ---
        for npc in self.level.npcs:
            npc.update(effective_dt, self.player)

        # =============================================================
        # STANDARD COLLISIONS
        # =============================================================

        # Checkpoints
        for cp in self.level.checkpoints:
            if not cp.activated and pygame.sprite.collide_rect(self.player, cp):
                if cp.activate():
                    self.respawn_x = cp.spawn_x
                    self.respawn_y = cp.spawn_y
                    self._total_score = self.player.score
                    self.hud.add_floating_text(
                        "CHECKPOINT!", cp.rect.centerx, cp.rect.top - 10,
                        (100, 255, 100))
                    self.particles.emit_sparkle(cp.rect.centerx, cp.rect.centery)
                    self.audio.play("collect")

        # Bamboo
        for bamboo in pygame.sprite.spritecollide(
                self.player, self.level.bamboos, True):
            points = self.player.collect_bamboo()
            self.hud.on_bamboo_collected()
            suffix = f" x{self.player.combo_count}!" if self.player.combo_count > 1 else ""
            self.hud.add_floating_text(
                f"+{points}{suffix}", bamboo.rect.centerx, bamboo.rect.top, COL_GOLD)
            self.particles.emit_sparkle(bamboo.rect.centerx, bamboo.rect.centery)
            self.audio.play("collect")

        # Bamboo staff weapon pickup (limited duration)
        for weapon in pygame.sprite.spritecollide(
                self.player, self.level.weapons, True):
            self.player.has_bamboo_weapon = True
            self.player.weapon_time_remaining = 30.0  # 30 seconds
            self._weapon_tutorial_timer = 999.0
            self._weapon_used = False
            self.hud.add_floating_text(
                "BAMBOO STAFF! 30s",
                weapon.rect.centerx, weapon.rect.top - 10, (255, 220, 120))
            self.particles.emit_sparkle(weapon.rect.centerx, weapon.rect.centery, 14)
            self.audio.play("collect")

        # Update weapon sprite animations
        self.level.weapons.update(effective_dt)

        # Heals
        for heal in pygame.sprite.spritecollide(
                self.player, self.level.heals, True):
            self.player.heal(HEAL_AMOUNT)
            self.hud.add_floating_text(
                f"+{HEAL_AMOUNT} HP", heal.rect.centerx, heal.rect.top,
                (100, 255, 100))
            self.particles.emit_sparkle(heal.rect.centerx, heal.rect.centery)
            self.audio.play("collect")

        # Spawn pending thrown shurikens
        if self.player.pending_throws:
            for (sx, sy, sdir) in self.player.pending_throws:
                shur = BambooShuriken(sx, sy, sdir)
                self.level.projectiles.add(shur)
                self.level.all_sprites.add(shur)
            self.player.pending_throws.clear()

        # Shuriken hits enemies
        for shur in list(self.level.projectiles):
            if not isinstance(shur, BambooShuriken):
                continue
            for enemy in list(self.level.enemies):
                if (getattr(enemy, "alive_flag", True)
                        and shur.rect.colliderect(enemy.rect)):
                    if not getattr(enemy, "is_stompable", True):
                        continue
                    enemy.die()
                    self.player.score += STOMP_SCORE
                    self.particles.emit_death(enemy.rect.centerx, enemy.rect.centery)
                    self.audio.play("stomp")
                    shur.kill()
                    break

        # Bamboo staff attack hits enemies
        if self.player.is_attacking:
            atk_rect = self.player.get_attack_rect()
            if atk_rect.width > 0:
                for enemy in list(self.level.enemies):
                    if (getattr(enemy, "alive_flag", True)
                            and atk_rect.colliderect(enemy.rect)):
                        # Flying/invincible enemies ignore melee
                        if not getattr(enemy, "is_stompable", True):
                            continue
                        enemy.die()
                        self.player.score += STOMP_SCORE
                        self.hud.add_floating_text(
                            f"+{STOMP_SCORE}", enemy.rect.centerx,
                            enemy.rect.top, COL_GOLD)
                        self.particles.emit_death(
                            enemy.rect.centerx, enemy.rect.centery)
                        self.audio.play("stomp")
                        # Hitstop: freeze 60ms for impact punch
                        self._hitstop_timer = max(self._hitstop_timer, 0.06)
                        self.shake.trigger(5, 0.08)
                # Boss gets hit too (if stunned)
                if (self.level.boss and self.level.boss.alive()
                        and self.level.boss.stunned
                        and atk_rect.colliderect(self.level.boss.rect)):
                    killed = self.level.boss.take_hit()
                    self.audio.play("boss_hit")
                    self.shake.trigger(8, 0.2)
                    if killed:
                        self.particles.emit_death(
                            self.level.boss.rect.centerx,
                            self.level.boss.rect.centery, 30)
                        self.player.score += BOSS_KILL_SCORE

        # Enemy collisions (stomp or damage)
        for enemy in pygame.sprite.spritecollide(
                self.player, self.level.enemies, False):
            if not getattr(enemy, "alive_flag", True):
                continue
            stomp_rect = self.player.get_stomp_rect()
            is_stompable = getattr(enemy, "is_stompable", True)
            if (is_stompable and self.player.velocity_y > 0
                    and stomp_rect.colliderect(enemy.rect)):
                enemy.die()
                self.player.velocity_y = ENEMY_STOMP_BOUNCE
                self.player.score += STOMP_SCORE
                self.hud.add_floating_text(
                    f"+{STOMP_SCORE}", enemy.rect.centerx, enemy.rect.top, COL_GOLD)
                self.particles.emit_death(enemy.rect.centerx, enemy.rect.centery)
                self.audio.play("stomp")
            else:
                if self.player.take_damage(PLAYER_DAMAGE):
                    self.shake.trigger()
                    self.particles.emit_damage(
                        self.player.rect.centerx, self.player.rect.centery)
                    self.audio.play("hit")

        # Boss collision:
        #   - Landing on head (stomp) always bounces player off, never hurts.
        #     Damage to boss ONLY applied during stunned state.
        #   - Side/below collision damages player (as before).
        if self.level.boss and self.level.boss.alive():
            if pygame.sprite.collide_rect(self.player, self.level.boss):
                stomp_rect = self.player.get_stomp_rect()
                is_head_stomp = (self.player.velocity_y > 0
                                 and stomp_rect.colliderect(self.level.boss.rect))
                if is_head_stomp:
                    if self.level.boss.stunned:
                        # Damage boss during vulnerable window
                        self.player.velocity_y = ENEMY_STOMP_BOUNCE
                        self.player.rect.bottom = self.level.boss.rect.top
                        killed = self.level.boss.take_hit()
                        self.audio.play("boss_hit")
                        self.shake.trigger(12, 0.3)
                        if killed:
                            self.particles.emit_death(
                                self.level.boss.rect.centerx,
                                self.level.boss.rect.centery, 30)
                            self.player.score += BOSS_KILL_SCORE
                            self.hud.add_floating_text(
                                f"+{BOSS_KILL_SCORE}",
                                self.level.boss.rect.centerx,
                                self.level.boss.rect.top, COL_GOLD)
                    else:
                        # NON-STUNNED head-camp: boss shakes player off with
                        # a strong sideways knockback + damage. No free ride.
                        kb_dir = 1.0 if self.player.rect.centerx >= \
                            self.level.boss.rect.centerx else -1.0
                        self.player.velocity_x = 500.0 * kb_dir
                        self.player.velocity_y = -450.0
                        self.player.rect.bottom = self.level.boss.rect.top
                        if self.player.take_damage(
                                PLAYER_DAMAGE,
                                source_x=self.level.boss.rect.centerx):
                            self.shake.trigger(10, 0.2)
                            self.particles.emit_damage(
                                self.player.rect.centerx,
                                self.player.rect.centery)
                            self.audio.play("hit")
                        self.hud.add_floating_text(
                            "!!", self.level.boss.rect.centerx,
                            self.level.boss.rect.top - 10, (255, 60, 60))
                else:
                    # Side/below hit -- boss damages player
                    if self.player.take_damage(PLAYER_DAMAGE):
                        self.shake.trigger()
                        self.particles.emit_damage(
                            self.player.rect.centerx, self.player.rect.centery)
                        self.audio.play("hit")

        # Goal -- trigger "run off screen" outro instead of instant transition
        if (self.level.goal and not self._outro_active
                and pygame.sprite.collide_rect(self.player, self.level.goal)):
            boss_blocking = (self.level.boss is not None
                             and self.level.boss.alive())
            if not boss_blocking:
                self._outro_active = True
                self._outro_timer = 3.0
                # Lock player from damage during outro + clear any bad state
                self.player.invincible_timer = 999.0
                self.player.input_locked = True
                self.player.is_dashing = False
                self.player.is_slamming = False
                self.player.is_gliding = False
                self.player.knockback_timer = 0.0
                self.player.velocity_x = 0.0
                self.player.velocity_y = 0.0
                self.player.dead = False  # can't die during outro
            else:
                # Player reached goal but boss still alive -- give feedback
                if self._boss_warning_timer <= 0:
                    self._boss_warning_timer = 2.0
                    self.hud.add_floating_text(
                        "DEFEAT THE BOSS FIRST!",
                        self.player.rect.centerx,
                        self.player.rect.top - 20,
                        (255, 80, 80))
        if self._boss_warning_timer > 0:
            self._boss_warning_timer -= effective_dt

        # Death
        # Trench death (disabled during outro -- player is invincible there)
        from config import TRENCH_DEATH_Y
        if (self.player.rect.top > TRENCH_DEATH_Y and not self.player.dead
                and not self._outro_active):
            self.player.health = 0
            self.player.dead = True
            self.player.is_falling_trench = True
        if self.player.dead and self.death_anim is None:
            self.death_anim = DeathAnimation()
            self.audio.play("death")

        # --- Level end outro: victory dance then run off screen ---
        if self._outro_active:
            # Play dance sound ONCE when the dance starts (frame 0 of anim)
            if (self._outro_timer > 1.4 and not self.player.is_victory_dancing):
                self.audio.play("dance")
            self._outro_timer -= effective_dt
            if self._outro_timer > 1.4:
                self.player.is_victory_dancing = True
                self.player.velocity_x = 0
                # Confetti sparkles during dance
                if int(self._outro_timer * 10) % 2 == 0:
                    self.particles.emit_sparkle(
                        self.player.rect.centerx,
                        self.player.rect.centery, 3)
            else:
                self.player.is_victory_dancing = False
                self.player.rect.x += math.floor(self._outro_speed * effective_dt)
                self.player.facing_right = True
                self.player.velocity_x = self._outro_speed
                self.player.anim_state = "run"
            if self._outro_timer <= 0:
                self._outro_active = False
                self.player.is_victory_dancing = False
                self._advance_level()

        # Tutorial hint timer decrement (when not persistent)
        if self._weapon_tutorial_timer < 999 and self._weapon_tutorial_timer > 0:
            self._weapon_tutorial_timer -= effective_dt

        # Camera + effects
        self.camera.update(self.player, effective_dt)
        self.shake.update(effective_dt)
        self.particles.emit_ambient_leaves(self.camera.get_visible_rect())
        self.particles.update(effective_dt)

        self.level.bamboos.update(effective_dt)
        self.level.heals.update(effective_dt)

        self.hud.lives = self.lives
        self.hud.update(effective_dt, self.player)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def _draw(self) -> None:
        if self.state == ST_MENU:
            self.title_screen.draw(self.screen)
            return
        if self.state == ST_LEVEL_TRANS:
            if self.level_transition:
                self.level_transition.draw(self.screen)
            return
        if self.state == ST_VICTORY:
            score = self.player.score if self.player else 0
            self.victory_screen.draw(self.screen, score, self._is_high_score)
            return
        if not self.player or not self.level or not self.camera:
            return

        shake_off = self.shake.update(0)
        self.background.draw(self.screen, self.camera.offset_x)

        render_cam_x = math.floor(self.camera.offset_x)
        render_cam_y = math.floor(self.camera.offset_y)
        cam_x = render_cam_x + shake_off[0]
        cam_y = render_cam_y + shake_off[1]
        visible = self.camera.get_visible_rect().inflate(100, 100)

        for dec in self.level.decorations:
            if dec.rect.colliderect(visible):
                self.screen.blit(dec.image, dec.rect.move(cam_x, cam_y))

        for sprite in self.level.all_sprites:
            if not sprite.rect.colliderect(visible):
                continue
            if (sprite is self.player and self.player.invincible_timer > 0
                    and int(self.player.invincible_timer * 10) % 2):
                continue
            self.screen.blit(sprite.image, sprite.rect.move(cam_x, cam_y))

        self.particles.draw(self.screen, self.camera)

        # NPC friendly-indicator: bouncing "?" above head (universal UI affordance)
        t_ms = pygame.time.get_ticks()
        bounce = math.sin(t_ms / 200.0) * 5
        for npc in self.level.npcs:
            if not npc.rect.colliderect(visible):
                continue
            sx = npc.rect.centerx + cam_x
            sy = npc.rect.top + cam_y - 26 + bounce
            # Yellow bubble background
            bubble = pygame.Surface((20, 24), pygame.SRCALPHA)
            pygame.draw.circle(bubble, (255, 230, 80), (10, 12), 10)
            pygame.draw.circle(bubble, (255, 180, 40), (10, 12), 10, 2)
            self.screen.blit(bubble, (int(sx) - 10, int(sy) - 12))
            # "?" glyph
            font = pygame.font.SysFont("consolas", 18, bold=True)
            q = font.render("?", True, (70, 45, 0))
            self.screen.blit(q, q.get_rect(center=(int(sx), int(sy))))

        # Sword swing arc (rotational visual + hitbox glow)
        if self.player.is_attacking:
            self._draw_sword_arc(cam_x, cam_y)

        # --- Darkness overlay (Level 7: Karst Caves) ---
        if self.level.is_dark:
            darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darkness.fill((0, 0, 0))
            # Player light circle
            px = self.player.rect.centerx + cam_x
            py = self.player.rect.centery + cam_y
            pygame.draw.circle(darkness, (0, 0, 0), (px, py), DARK_RADIUS)
            # Lit crystal circles
            for crystal in self.level.crystals:
                if crystal.is_lit():
                    cx = crystal.rect.centerx + cam_x
                    cy = crystal.rect.centery + cam_y
                    pygame.draw.circle(darkness, (0, 0, 0), (cx, cy), CRYSTAL_RADIUS)
            darkness.set_colorkey((0, 0, 0))
            # Invert: fill screen-sized black, cut holes, then overlay
            dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 230))
            # Cut light holes by blitting the mask
            light_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            light_mask.fill((0, 0, 0, 0))
            pygame.draw.circle(light_mask, (0, 0, 0, 230), (px, py), DARK_RADIUS)
            for crystal in self.level.crystals:
                if crystal.is_lit():
                    cx = crystal.rect.centerx + cam_x
                    cy = crystal.rect.centery + cam_y
                    pygame.draw.circle(light_mask, (0, 0, 0, 230), (cx, cy), CRYSTAL_RADIUS)
            dark_overlay.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.screen.blit(dark_overlay, (0, 0))

        # --- Boss HP bar (above boss, world-space) ---
        if self.level.boss and self.level.boss.alive():
            boss = self.level.boss
            bar_w = 120
            bar_h = 8
            bx = boss.rect.centerx + cam_x - bar_w // 2
            by = boss.rect.top + cam_y - 16
            # Backing
            pygame.draw.rect(self.screen, (30, 0, 0), (bx - 2, by - 2, bar_w + 4, bar_h + 4))
            pygame.draw.rect(self.screen, (80, 20, 20), (bx, by, bar_w, bar_h))
            # Fill proportional to HP
            fill = int(bar_w * (boss.hp / max(1, boss.max_hp)))
            if fill > 0:
                pygame.draw.rect(self.screen, (220, 40, 40), (bx, by, fill, bar_h))
            pygame.draw.rect(self.screen, (255, 255, 255), (bx, by, bar_w, bar_h), 1)
            # "BOSS" label
            font = pygame.font.SysFont("consolas", 12, bold=True)
            label = font.render(f"BOSS  {boss.hp}/{boss.max_hp}", True, (255, 200, 200))
            self.screen.blit(label, (bx, by - 14))

        # --- Debug mode hitbox overlay ---
        if self._debug_mode:
            self._draw_debug_hitboxes(cam_x, cam_y)

        self.hud.draw(self.screen, self.player, self.current_level + 1, self.camera)

        # Weapon tutorial hint -- persistent banner until first use
        if (self.player.has_bamboo_weapon and not self._weapon_used):
            self._draw_weapon_hint()

        # --- NPC dialog box at bottom of screen ---
        active_npc = None
        for npc in self.level.npcs:
            if npc.show_dialog:
                active_npc = npc
                break
        if active_npc is not None:
            self._draw_npc_textbox(active_npc)

        if self.state == ST_PAUSED:
            self.pause_overlay.draw(self.screen)
        elif self.state == ST_GAME_OVER:
            self.game_over_screen.draw(self.screen, self.player.score)

    def _draw_sword_arc(self, cam_x: int, cam_y: int) -> None:
        """Draw a clearly sword-shaped bamboo katana with full swing arc."""
        total = 0.25
        t = 1.0 - (self.player.attack_timer / total)
        t = max(0.0, min(1.0, t))

        # Build a long sword-shaped surface (katana-style silhouette)
        SW, SH = 90, 18
        sword = pygame.Surface((SW, SH), pygame.SRCALPHA)
        # Pommel (dark brown ball)
        pygame.draw.circle(sword, (60, 35, 20), (5, SH // 2), 5)
        # Handle (wrapped dark red / diamond pattern)
        pygame.draw.rect(sword, (120, 45, 35), (8, 6, 20, 6))
        for i in range(10, 28, 3):
            pygame.draw.line(sword, (60, 20, 15), (i, 6), (i, 12), 1)
        # Guard (tsuba) -- round gold disk
        pygame.draw.circle(sword, (200, 170, 70), (30, SH // 2), 7)
        pygame.draw.circle(sword, (240, 210, 110), (30, SH // 2), 5)
        pygame.draw.circle(sword, (140, 100, 30), (30, SH // 2), 7, 1)
        # Blade (bright bamboo-green, tapered katana shape)
        blade_pts = [
            (36, 6),             # base top
            (SW - 10, 3),        # tip top
            (SW - 2, SH // 2),   # sharp tip
            (SW - 10, SH - 4),   # tip bottom
            (36, SH - 6),        # base bottom
        ]
        pygame.draw.polygon(sword, (150, 220, 110), blade_pts)
        # Blade highlight stripe (gives the "shine")
        pygame.draw.polygon(sword, (220, 255, 180), [
            (36, 7), (SW - 12, 5), (SW - 4, SH // 2 - 1), (36, SH // 2 - 1)])
        # Blade dark edge
        pygame.draw.polygon(sword, (80, 150, 60), [
            (36, SH // 2 + 1), (SW - 4, SH // 2 + 1),
            (SW - 12, SH - 5), (36, SH - 7)])
        # Bamboo joint rings on blade (every 15px)
        for jx in range(46, SW - 10, 14):
            pygame.draw.line(sword, (70, 140, 50),
                             (jx, 6), (jx, SH - 6), 1)
        # Leaf flourish at tip
        pygame.draw.polygon(sword, (80, 160, 55),
                            [(SW - 4, SH // 2 - 3),
                             (SW - 10, SH // 2 - 8),
                             (SW - 14, SH // 2 - 1)])

        # Swing angle: steep upward windup -> down-forward follow-through
        if self.player.facing_right:
            angle = -80 + 130 * t
        else:
            angle = 80 - 130 * t
            sword = pygame.transform.flip(sword, True, False)
        rotated = pygame.transform.rotate(sword, -angle)
        # Pivot at Pain-da's front hand (slight forward lean)
        off_x = 10 if self.player.facing_right else -10
        off_y = -4
        cx = self.player.rect.centerx + cam_x + off_x
        cy = self.player.rect.centery + cam_y + off_y
        rect = rotated.get_rect(center=(cx, cy))
        self.screen.blit(rotated, rect)

        # Arc trail (several faded copies for streak effect)
        for trail_i in range(3):
            trail_t = t - 0.04 * (trail_i + 1)
            if trail_t < 0:
                continue
            if self.player.facing_right:
                tangle = -80 + 130 * trail_t
            else:
                tangle = 80 - 130 * trail_t
            trail_surf = sword.copy()
            trail_surf.set_alpha(60 - trail_i * 18)
            trail_rot = pygame.transform.rotate(trail_surf, -tangle)
            trect = trail_rot.get_rect(center=(cx, cy))
            self.screen.blit(trail_rot, trect)

        # Bright sweep arc highlight
        streak = pygame.Surface((60, 5), pygame.SRCALPHA)
        streak.fill((255, 250, 200, 160))
        streak_rot = pygame.transform.rotate(streak, -angle + 8)
        srect = streak_rot.get_rect(center=(cx, cy))
        self.screen.blit(streak_rot, srect)

    def _draw_weapon_hint(self) -> None:
        """Persistent banner teaching the player how to attack."""
        # Pulsing alpha to draw attention
        t = pygame.time.get_ticks() / 200.0
        alpha = int(180 + 55 * math.sin(t))
        font_big = pygame.font.SysFont("consolas", 22, bold=True)
        font_small = pygame.font.SysFont("consolas", 14)
        title = font_big.render("BAMBOO STAFF EQUIPPED!", True, (255, 230, 120))
        hint = font_small.render("Press  [ E ]  or  LEFT CLICK  to swing",
                                 True, (230, 230, 230))
        w = max(title.get_width(), hint.get_width()) + 32
        h = 58
        bx = (SCREEN_WIDTH - w) // 2
        by = 96
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((20, 20, 30, alpha))
        pygame.draw.rect(bg, (255, 220, 120), (0, 0, w, h), 3, border_radius=6)
        self.screen.blit(bg, (bx, by))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, by + 18)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, by + 42)))

    def _draw_npc_textbox(self, npc) -> None:
        """Full-width text box at bottom of screen for NPC dialog."""
        box_h = 90
        box_y = SCREEN_HEIGHT - box_h - 8
        box_x = 20
        box_w = SCREEN_WIDTH - 40
        # Background panel with border
        bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg.fill((15, 15, 25, 230))
        pygame.draw.rect(bg, (255, 220, 120, 200), (0, 0, box_w, box_h), 3,
                         border_radius=8)
        self.screen.blit(bg, (box_x, box_y))
        # Name tab in corner
        name_font = pygame.font.SysFont("consolas", 18, bold=True)
        name_surf = name_font.render(npc.name, True, (255, 220, 120))
        name_bg = pygame.Surface((name_surf.get_width() + 20, 24), pygame.SRCALPHA)
        name_bg.fill((40, 30, 20, 240))
        pygame.draw.rect(name_bg, (255, 220, 120),
                        (0, 0, name_bg.get_width(), 24), 2, border_radius=4)
        self.screen.blit(name_bg, (box_x + 12, box_y - 12))
        self.screen.blit(name_surf, (box_x + 22, box_y - 8))
        # Dialog text (render all lines stacked)
        text_font = pygame.font.SysFont("consolas", 16)
        for i, line in enumerate(npc.dialog_lines):
            line_surf = text_font.render(line, True, (235, 235, 235))
            self.screen.blit(line_surf, (box_x + 24, box_y + 22 + i * 22))

    def _draw_debug_hitboxes(self, cam_x: int, cam_y: int) -> None:
        """Draw bright red rectangles around all hitboxes for collision verification."""
        R = (255, 0, 0)  # hitboxes
        G = (0, 255, 0)  # player
        C = (0, 255, 255)  # goal/checkpoint
        Y = (255, 255, 0)  # pickups
        # Platforms
        for p in self.level.platforms:
            pygame.draw.rect(self.screen, R,
                             p.rect.move(cam_x, cam_y), 2)
        # Enemies
        for e in self.level.enemies:
            pygame.draw.rect(self.screen, R,
                             e.rect.move(cam_x, cam_y), 2)
        # Boss
        if self.level.boss and self.level.boss.alive():
            pygame.draw.rect(self.screen, R,
                             self.level.boss.rect.move(cam_x, cam_y), 2)
        # Player (green)
        pygame.draw.rect(self.screen, G,
                         self.player.rect.move(cam_x, cam_y), 2)
        # Player stomp-rect (feet)
        pygame.draw.rect(self.screen, (255, 128, 0),
                         self.player.get_stomp_rect().move(cam_x, cam_y), 1)
        # Bamboo sword attack hitbox (during active swing)
        if self.player.is_attacking:
            atk = self.player.get_attack_rect()
            if atk.width > 0:
                pygame.draw.rect(self.screen, (255, 0, 180),
                                 atk.move(cam_x, cam_y), 2)
        # Goal
        if self.level.goal:
            pygame.draw.rect(self.screen, C,
                             self.level.goal.rect.move(cam_x, cam_y), 2)
        # Checkpoints
        for cp in self.level.checkpoints:
            pygame.draw.rect(self.screen, C,
                             cp.rect.move(cam_x, cam_y), 2)
        # Bamboos & heals
        for b in self.level.bamboos:
            pygame.draw.rect(self.screen, Y, b.rect.move(cam_x, cam_y), 1)
        for h in self.level.heals:
            pygame.draw.rect(self.screen, Y, h.rect.move(cam_x, cam_y), 1)
        # Biome: geysers, wind zones, crystals, crumbling, updrafts
        for g in self.level.geysers:
            pygame.draw.rect(self.screen, R, g.rect.move(cam_x, cam_y), 2)
        for wz in self.level.wind_zones:
            pygame.draw.rect(self.screen, (255, 0, 255),
                             wz.rect.move(cam_x, cam_y), 2)
        for tu in self.level.updrafts:
            pygame.draw.rect(self.screen, (255, 0, 255),
                             tu.rect.move(cam_x, cam_y), 2)
        for cr in self.level.crystals:
            pygame.draw.rect(self.screen, C, cr.rect.move(cam_x, cam_y), 2)
        for cp in self.level.crumbling:
            pygame.draw.rect(self.screen, (255, 165, 0),
                             cp.rect.move(cam_x, cam_y), 2)
        for np_ in self.level.npcs:
            pygame.draw.rect(self.screen, (100, 255, 255),
                             np_.rect.move(cam_x, cam_y), 2)
        # Debug overlay text
        font = pygame.font.SysFont("consolas", 14, bold=True)
        info = font.render("DEBUG [TAB] | RED=hitbox GREEN=player CYAN=goal YELLOW=pickup",
                           True, (255, 255, 255))
        info_bg = pygame.Surface((info.get_width() + 10, info.get_height() + 4),
                                pygame.SRCALPHA)
        info_bg.fill((0, 0, 0, 180))
        self.screen.blit(info_bg, (4, SCREEN_HEIGHT - 22))
        self.screen.blit(info, (8, SCREEN_HEIGHT - 20))


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
