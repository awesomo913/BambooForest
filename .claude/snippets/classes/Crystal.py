# From: biomes.py:629
# Level 7. Strike to expand visibility in dark levels.

class Crystal(pygame.sprite.Sprite):
    """Level 7. Strike to expand visibility in dark levels."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_dim = pygame.Surface((20, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self._img_dim, (60, 100, 140),
                            [(10, 0), (20, 15), (10, 30), (0, 15)])
        self._img_lit = pygame.Surface((20, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self._img_lit, COL_CRYSTAL,
                            [(10, 0), (20, 15), (10, 30), (0, 15)])
        pygame.draw.polygon(self._img_lit, (180, 240, 255),
                            [(10, 4), (16, 15), (10, 26), (4, 15)])
        self.image = self._img_dim
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.lit = False
        self.light_timer: float = 0.0

    def strike(self) -> None:
        self.lit = True
        self.light_timer = CRYSTAL_LIGHT_TIME
        self.image = self._img_lit

    def update(self, dt: float) -> None:  # type: ignore[override]
        if self.lit:
            self.light_timer -= dt
            if self.light_timer <= 0:
                self.lit = False
                self.image = self._img_dim

    def is_lit(self) -> bool:
        return self.lit
