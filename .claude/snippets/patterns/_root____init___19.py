# From: biomes.py:668

    def __init__(self, x: int, y: int, w: int, h: int = 20) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(COL_ICE)
        pygame.draw.rect(self.image, (200, 235, 255), (0, 0, w, 4))
        # Ice shine
        for sx in range(0, w, 8):
            pygame.draw.rect(self.image, (220, 240, 255), (sx, 1, 3, 2))
        self.rect = self.image.get_rect(topleft=(x, y))
