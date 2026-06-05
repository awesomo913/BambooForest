# From: sprites.py:1528
# Mushroom that walks back and forth. Stompable.

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
