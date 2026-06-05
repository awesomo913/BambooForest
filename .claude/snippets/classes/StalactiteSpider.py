# From: biomes.py:1078
# Level 7. Drops from ceiling when player passes below.

class StalactiteSpider(pygame.sprite.Sprite):
    """Level 7. Drops from ceiling when player passes below."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((28, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (60, 50, 50), (4, 2, 20, 16))
        for lx in (2, 8, 16, 22):
            pygame.draw.line(self.image, (50, 40, 40), (lx, 10), (lx - 2, 18), 1)
        pygame.draw.circle(self.image, (200, 40, 40), (11, 7), 2)
        pygame.draw.circle(self.image, (200, 40, 40), (17, 7), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.state = "hanging"
        self.origin_y = y
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.pos_x = float(x)
        self.direction: float = 1.0

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag or player is None:
            return
        if self.state == "hanging":
            if (abs(player.rect.centerx - self.rect.centerx) < SPIDER_DROP_RANGE
                    and player.rect.centery > self.rect.centery):
                self.state = "dropping"
                self.velocity_y = 0
        elif self.state == "dropping":
            self.velocity_y += GRAVITY * dt
            if self.velocity_y > SPIDER_DROP_SPEED:
                self.velocity_y = SPIDER_DROP_SPEED
            self.rect.y += _fl(self.velocity_y * dt)
            for hit in pygame.sprite.spritecollide(self, platforms, False):
                if self.velocity_y > 0:
                    self.rect.bottom = hit.rect.top
                    self.velocity_y = 0
                    self.state = "grounded"
                    self.pos_x = float(self.rect.x)
        elif self.state == "grounded":
            self.pos_x += ENEMY_PATROL_SPEED * 0.6 * self.direction * dt
            if abs(self.pos_x - self.rect.x) > 80:
                self.direction *= -1
            self.rect.x = _fl(self.pos_x)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
