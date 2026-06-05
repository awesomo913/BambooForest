# From: biomes.py:595
# Level 6. Pushes player sideways.

class WindZone(pygame.sprite.Sprite):
    """Level 6. Pushes player sideways."""

    def __init__(self, x: int, y: int, w: int, h: int,
                 direction: float = 1.0) -> None:
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        col = (*COL_SANDSTONE, 40)
        self.image.fill(col)
        # Arrow indicators
        for ay in range(10, h - 10, 30):
            ax = w // 2 + (10 if direction > 0 else -10)
            pygame.draw.polygon(self.image, (*COL_SANDSTONE, 80), [
                (ax - 8, ay), (ax + 8, ay + 8), (ax - 8, ay + 16)])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction

    def get_push(self) -> float:
        return WIND_PUSH * self.direction
