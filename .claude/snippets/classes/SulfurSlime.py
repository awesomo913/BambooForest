# From: biomes.py:707
# Level 4. Slow patrol, leaves toxic trail.

class SulfurSlime(pygame.sprite.Sprite):
    """Level 4. Slow patrol, leaves toxic trail."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 150.0) -> None:
        super().__init__()
        self.image = pygame.Surface((30, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (180, 200, 40), (0, 4, 30, 24))
        pygame.draw.circle(self.image, COL_WHITE, (10, 12), 3)
        pygame.draw.circle(self.image, COL_WHITE, (20, 12), 3)
        pygame.draw.circle(self.image, COL_BLACK, (11, 12), 2)
        pygame.draw.circle(self.image, COL_BLACK, (19, 12), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.trail_timer: float = 0.0
        self._pending_trails: list[ToxicTrail] = []

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self._pending_trails.clear()
        self.pos_x += SULFUR_SPEED * self.direction * dt
        if self.pos_x > self.origin_x + self.patrol_width:
            self.pos_x = self.origin_x + self.patrol_width
            self.direction = -1.0
        elif self.pos_x < self.origin_x - self.patrol_width:
            self.pos_x = self.origin_x - self.patrol_width
            self.direction = 1.0
        self.rect.x = _fl(self.pos_x)
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0
        self.trail_timer += dt
        if self.trail_timer >= 0.5:
            self.trail_timer = 0.0
            self._pending_trails.append(ToxicTrail(self.rect.centerx - 10, self.rect.bottom))

    def get_new_trails(self) -> list[ToxicTrail]:
        return self._pending_trails

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
