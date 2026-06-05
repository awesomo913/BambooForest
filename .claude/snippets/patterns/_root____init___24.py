# From: biomes.py:873

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_dormant = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.rect(self._img_dormant, COL_BASALT, (0, 0, 30, 50), border_radius=3)
        self._img_active = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.rect(self._img_active, (90, 80, 80), (0, 0, 30, 50), border_radius=3)
        pygame.draw.circle(self._img_active, (255, 80, 40), (10, 15), 4)
        pygame.draw.circle(self._img_active, (255, 80, 40), (20, 15), 4)
        self.image = self._img_dormant
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.state = "dormant"
        self.state_timer: float = 0.0
        self.strike_dir: float = 0.0
        self.origin_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
