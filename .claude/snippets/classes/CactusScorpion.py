# From: biomes.py:1019
# Level 6. Fires 45-degree projectiles.

class CactusScorpion(pygame.sprite.Sprite):
    """Level 6. Fires 45-degree projectiles."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 100.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (160, 120, 60), (4, 8, 28, 18))
        pygame.draw.rect(self.image, (140, 100, 40), (28, 2, 6, 10))
        pygame.draw.circle(self.image, (200, 180, 60), (32, 2), 3)
        pygame.draw.circle(self.image, COL_WHITE, (12, 14), 3)
        pygame.draw.circle(self.image, COL_WHITE, (22, 14), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 14), 2)
        pygame.draw.circle(self.image, COL_BLACK, (21, 14), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.fire_timer: float = SCORPION_FIRE_RATE
        self._pending_proj: list[ScorpionProjectile] = []

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag:
            return
        self._pending_proj.clear()
        self.pos_x += ENEMY_PATROL_SPEED * 0.5 * self.direction * dt
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
        self.fire_timer -= dt
        if self.fire_timer <= 0:
            self.fire_timer = SCORPION_FIRE_RATE
            self._pending_proj.append(
                ScorpionProjectile(self.rect.centerx, self.rect.top, self.direction))

    def get_new_projectiles(self) -> list[ScorpionProjectile]:
        return self._pending_proj

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
