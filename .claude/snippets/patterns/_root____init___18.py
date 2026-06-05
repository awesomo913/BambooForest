# From: biomes.py:632

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
