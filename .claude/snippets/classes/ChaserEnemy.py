# From: sprites.py:1571
# Dark wolf that chases the player.

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
