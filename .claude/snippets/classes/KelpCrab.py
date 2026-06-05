# From: biomes.py:821
# Level 5. Armored patrol, stomp-only kill.

class KelpCrab(pygame.sprite.Sprite):
    """Level 5. Armored patrol, stomp-only kill."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 120.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (180, 80, 60), (2, 2, 32, 18))
        pygame.draw.rect(self.image, (160, 60, 40), (0, 6, 6, 4))
        pygame.draw.rect(self.image, (160, 60, 40), (30, 6, 6, 4))
        pygame.draw.circle(self.image, COL_WHITE, (12, 8), 3)
        pygame.draw.circle(self.image, COL_WHITE, (24, 8), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 8), 2)
        pygame.draw.circle(self.image, COL_BLACK, (23, 8), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self.pos_x += KELP_CRAB_SPEED * self.direction * dt
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

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
