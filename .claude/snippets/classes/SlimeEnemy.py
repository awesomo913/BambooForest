# From: sprites.py:1616
# Bouncing slime blob. Stompable.

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
