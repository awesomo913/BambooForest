"""Bamboo Forest - Main game entry point and loop."""

from __future__ import annotations

import sys

import pygame

from config import (
    COL_GOLD, DOUBLE_JUMP_LEVEL, ENEMY_STOMP_BOUNCE, FPS, FLOOR_Y,
    HEAL_AMOUNT, LEVEL_COUNT, PLAYER_DAMAGE, PLAYER_MAX_HP,
    SCREEN_HEIGHT, SCREEN_WIDTH, STARTING_LIVES, STOMP_SCORE,
    ST_GAME_OVER, ST_LEVEL_TRANS, ST_MENU, ST_PAUSED, ST_PLAYING,
    ST_VICTORY, TITLE, BOSS_KILL_SCORE,
)
from audio import AudioManager
from engine import Camera, ParallaxBackground, ParticleSystem, ScreenShake
from levels import build_level_state, LevelState
from save import save_high_score
from sprites import Player
from ui import (
    DeathAnimation, GameOverScreen, HUD, LevelTransition,
    PauseOverlay, TitleScreen, VictoryScreen,
)


class Game:
    """Main game class -- owns the loop and state machine."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.audio = AudioManager()
        self.background = ParallaxBackground()
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

        # Lives + checkpoint state
        self.lives: int = STARTING_LIVES
        self.respawn_x: int = 100
        self.respawn_y: int = FLOOR_Y
        self._total_score: int = 0  # score preserved across respawns

        self._carry_score: int = 0
        self._carry_health: int = 0
        self._was_on_ground: bool = False
        self._is_high_score: bool = False
        self._jump_pressed: bool = False

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
                self._on_key_down(event.key)
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._jump_pressed = False

    def _on_key_down(self, key: int) -> None:
        if self.state == ST_MENU:
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
    # Game start / level management
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

        # Respawn at level start (checkpoint resets per level)
        self.respawn_x = self.level.player_start[0]
        self.respawn_y = self.level.player_start[1]

        self.player = Player(self.respawn_x, self.respawn_y)
        if level_num >= DOUBLE_JUMP_LEVEL:
            self.player.has_double_jump = True
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
        self.state = ST_PLAYING

    def _respawn_at_checkpoint(self) -> None:
        """Respawn player at last checkpoint (or level start). Lose 1 life."""
        self.lives -= 1
        if self.lives <= 0:
            # Game over
            save_high_score(self._total_score, self.current_level + 1)
            self.game_over_screen = GameOverScreen()
            self.state = ST_GAME_OVER
            self.death_anim = None
            return

        # Rebuild level but keep checkpoint activations
        activated_xs = set()
        if self.level:
            for cp in self.level.checkpoints:
                if cp.activated:
                    activated_xs.add(cp.spawn_x)

        self.level = build_level_state(self.current_level)
        self.camera = Camera(self.level.world_width, SCREEN_HEIGHT)

        # Re-activate previously hit checkpoints
        for cp in self.level.checkpoints:
            if cp.spawn_x in activated_xs:
                cp.activate()

        # Create player at respawn point
        self.player = Player(self.respawn_x, self.respawn_y)
        if self.current_level >= DOUBLE_JUMP_LEVEL:
            self.player.has_double_jump = True
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

        # Death animation slowdown
        effective_dt = dt
        if self.death_anim:
            effective_dt = dt * self.death_anim.get_time_scale()
            if self.death_anim.update(dt):
                self._total_score = self.player.score
                self._respawn_at_checkpoint()
                return

        # Moving platforms
        for mp in self.level.moving_platforms:
            pdelta = mp.update_moving(effective_dt)
            if self.player.is_on_ground:
                feet = self.player.get_stomp_rect()
                if feet.colliderect(mp.rect.inflate(4, 8)):
                    self.player.rect.x += int(pdelta[0])
                    self.player.rect.y += int(pdelta[1])

        # Player
        keys = pygame.key.get_pressed()
        self.player.update(effective_dt, keys, self.level.platforms)

        # Landing dust
        if self.player.is_on_ground and not self._was_on_ground:
            self.particles.emit_dust(
                self.player.rect.centerx, self.player.rect.bottom)
        self._was_on_ground = self.player.is_on_ground

        # Enemies
        for enemy in list(self.level.enemies):
            enemy.update(effective_dt, self.level.platforms, self.player)

        # Boss
        if self.level.boss and self.level.boss.alive():
            self.level.boss.update(effective_dt, self.player, self.level.platforms)

        # --- Collisions ---

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
        for bamboo in pygame.sprite.spritecollide(self.player, self.level.bamboos, True):
            points = self.player.collect_bamboo()
            self.hud.on_bamboo_collected()
            suffix = f" x{self.player.combo_count}!" if self.player.combo_count > 1 else ""
            self.hud.add_floating_text(
                f"+{points}{suffix}", bamboo.rect.centerx, bamboo.rect.top, COL_GOLD)
            self.particles.emit_sparkle(bamboo.rect.centerx, bamboo.rect.centery)
            self.audio.play("collect")

        # Heals
        for heal in pygame.sprite.spritecollide(self.player, self.level.heals, True):
            self.player.heal(HEAL_AMOUNT)
            self.hud.add_floating_text(
                f"+{HEAL_AMOUNT} HP", heal.rect.centerx, heal.rect.top, (100, 255, 100))
            self.particles.emit_sparkle(heal.rect.centerx, heal.rect.centery)
            self.audio.play("collect")

        # Enemy collisions
        for enemy in pygame.sprite.spritecollide(self.player, self.level.enemies, False):
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

        # Boss collision
        if self.level.boss and self.level.boss.alive():
            if pygame.sprite.collide_rect(self.player, self.level.boss):
                stomp_rect = self.player.get_stomp_rect()
                if (self.level.boss.stunned
                        and self.player.velocity_y > 0
                        and stomp_rect.colliderect(self.level.boss.rect)):
                    killed = self.level.boss.take_hit()
                    self.player.velocity_y = ENEMY_STOMP_BOUNCE
                    self.audio.play("boss_hit")
                    self.shake.trigger(12, 0.3)
                    if killed:
                        self.particles.emit_death(
                            self.level.boss.rect.centerx,
                            self.level.boss.rect.centery, 30)
                        self.player.score += BOSS_KILL_SCORE
                        self.hud.add_floating_text(
                            f"+{BOSS_KILL_SCORE}", self.level.boss.rect.centerx,
                            self.level.boss.rect.top, COL_GOLD)
                else:
                    if self.player.take_damage(PLAYER_DAMAGE):
                        self.shake.trigger()
                        self.particles.emit_damage(
                            self.player.rect.centerx, self.player.rect.centery)
                        self.audio.play("hit")

        # Goal
        if self.level.goal and pygame.sprite.collide_rect(
                self.player, self.level.goal):
            boss_blocking = (self.level.boss is not None
                             and self.level.boss.alive())
            if not boss_blocking:
                self._advance_level()

        # Player death -> start death anim (respawn happens when anim ends)
        if self.player.dead and self.death_anim is None:
            self.death_anim = DeathAnimation()
            self.audio.play("death")

        # Camera + effects
        self.camera.update(self.player, effective_dt)
        self.shake.update(effective_dt)
        self.particles.emit_ambient_leaves(self.camera.get_visible_rect())
        self.particles.update(effective_dt)

        # Collectible animations
        self.level.bamboos.update(effective_dt)
        self.level.heals.update(effective_dt)

        # HUD
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

        # Cast camera float to int at RENDER TIME ONLY -- single conversion
        cam_x = int(self.camera.offset_x) + shake_off[0]
        cam_y = int(self.camera.offset_y) + shake_off[1]
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
        self.hud.draw(self.screen, self.player, self.current_level + 1, self.camera)

        if self.state == ST_PAUSED:
            self.pause_overlay.draw(self.screen)
        elif self.state == ST_GAME_OVER:
            self.game_over_screen.draw(self.screen, self.player.score)


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
