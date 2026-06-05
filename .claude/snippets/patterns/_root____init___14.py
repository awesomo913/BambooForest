# From: biomes.py:518

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((22, 8), pygame.SRCALPHA)
        # Goo puddle with bubbles
        pygame.draw.ellipse(self.image, (100, 160, 40), (0, 2, 22, 6))
        pygame.draw.ellipse(self.image, (160, 220, 60), (2, 3, 18, 3))
        # Bubbles
        pygame.draw.circle(self.image, (220, 255, 120), (6, 3), 1)
        pygame.draw.circle(self.image, (220, 255, 120), (14, 4), 1)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.lifetime: float = SULFUR_TRAIL_LIFE
