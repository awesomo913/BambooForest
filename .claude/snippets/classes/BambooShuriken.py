# From: sprites.py:1183
# Thrown bamboo shuriken projectile. Travels horizontally, rotating.

class BambooShuriken(pygame.sprite.Sprite):
    """Thrown bamboo shuriken projectile. Travels horizontally, rotating."""

    def __init__(self, x: int, y: int, direction: float) -> None:
        super().__init__()
        self._base = pygame.Surface((20, 20), pygame.SRCALPHA)
        # 4-point bamboo star
        cx = 10
        for angle in (0, 90, 180, 270):
            import math as _m
            dx = _m.cos(_m.radians(angle)) * 9
            dy = _m.sin(_m.radians(angle)) * 9
            pygame.draw.polygon(self._base, (130, 200, 90),
                                [(cx, cx), (cx + dx, cx + dy),
                                 (cx + _m.cos(_m.radians(angle + 30)) * 4,
                                  cx + _m.sin(_m.radians(angle + 30)) * 4)])
        pygame.draw.circle(self._base, (70, 140, 50), (cx, cx), 4)
        pygame.draw.circle(self._base, (180, 230, 120), (cx, cx), 2)
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vx = 600.0 * direction
        self.vy = 0.0
        self.rotation: float = 0.0
        self.lifetime: float = 2.5

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.pos_x += self.vx * dt
        self.pos_y += self.vy * dt
        self.vy += GRAVITY * 0.15 * dt  # slight drop
        self.rotation += 720 * dt * (1 if self.direction > 0 else -1)
        self.image = pygame.transform.rotate(self._base, self.rotation % 360)
        old_center = (_fl(self.pos_x), _fl(self.pos_y))
        self.rect = self.image.get_rect(center=old_center)
        self.lifetime -= dt
        if self.lifetime <= 0 or self.pos_y > 600:
            self.kill()
