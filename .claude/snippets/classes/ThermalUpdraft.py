# From: biomes.py:616
# Level 6. Vertical column giving upward boost.

class ThermalUpdraft(pygame.sprite.Sprite):
    """Level 6. Vertical column giving upward boost."""

    def __init__(self, x: int, y: int, w: int = 60, h: int = 200) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image.fill((220, 180, 100, 30))
        for uy in range(0, h, 15):
            pygame.draw.line(self.image, (240, 200, 120, 50),
                             (w // 2 - 5, uy), (w // 2 + 5, uy - 8), 1)
        self.rect = self.image.get_rect(bottomleft=(x, y))
