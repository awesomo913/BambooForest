# From: biomes.py:679
# Level 6. 45-degree thorn from CactusScorpion.

class ScorpionProjectile(pygame.sprite.Sprite):
    """Level 6. 45-degree thorn from CactusScorpion."""

    def __init__(self, x: int, y: int, direction: float) -> None:
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 180, 60), (4, 4), 4)
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.radians(45)
        self.vx = SCORPION_PROJ_SPEED * direction * math.cos(angle)
        self.vy = -SCORPION_PROJ_SPEED * math.sin(angle)
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.pos_x += self.vx * dt
        self.pos_y += self.vy * dt
        self.vy += GRAVITY * 0.3 * dt  # slight arc
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(self.pos_y)
        if self.rect.y > FLOOR_Y + 100 or self.rect.x < -50 or self.rect.x > 8000:
            self.kill()
