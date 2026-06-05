# From: biomes.py:1133

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_lure = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self._img_lure, (150, 255, 100), (8, 8), 8)
        pygame.draw.circle(self._img_lure, (200, 255, 180), (8, 8), 4)
        self._img_snap = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self._img_snap, (255, 60, 40), (8, 8), 8)
        pygame.draw.circle(self._img_snap, (255, 120, 100), (8, 8), 4)
        self.image = self._img_lure
        self.rect = self.image.get_rect(center=(x, y))
        self.state = "luring"
        self.state_timer: float = 0.0
        self.alive_flag = True
