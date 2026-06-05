# From: biomes.py:1936
# Hovering mech sphere that pulls the player toward itself.

class GravityDrone(pygame.sprite.Sprite):
    """Hovering mech sphere that pulls the player toward itself."""

    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 32, 32
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Metal sphere body
        pygame.draw.circle(self._base, (100, 110, 130), (W // 2, H // 2), W // 2 - 2)
        pygame.draw.circle(self._base, (140, 150, 180),
                          (W // 2 - 3, H // 2 - 3), W // 3)
        # Glowing core
        pygame.draw.circle(self._base, (180, 120, 255), (W // 2, H // 2), 5)
        pygame.draw.circle(self._base, (230, 200, 255), (W // 2, H // 2), 3)
        # Ring
        pygame.draw.ellipse(self._base, (180, 150, 220),
                           (2, H // 2 - 2, W - 4, 4), 2)
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self.base_y = float(y)
        self.alive_flag = True
        self.flash: float = 0.0
        self._bob: float = random.uniform(0, 6.28)

    def update(self, dt: float, platforms=None, player=None) -> None:  # type: ignore[override]
        if not self.alive_flag:
            return
        if self.flash > 0:
            self.flash -= dt
        self._bob += dt * 2.0
        self.rect.y = int(self.base_y + math.sin(self._bob) * 6)
        if self.flash > 0:
            img = self._base.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img
        else:
            self.image = self._base

    def die(self) -> None:
        self.alive_flag = False
        self.kill()

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
