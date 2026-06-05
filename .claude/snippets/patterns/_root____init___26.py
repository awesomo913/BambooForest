# From: biomes.py:1082

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((28, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (60, 50, 50), (4, 2, 20, 16))
        for lx in (2, 8, 16, 22):
            pygame.draw.line(self.image, (50, 40, 40), (lx, 10), (lx - 2, 18), 1)
        pygame.draw.circle(self.image, (200, 40, 40), (11, 7), 2)
        pygame.draw.circle(self.image, (200, 40, 40), (17, 7), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.state = "hanging"
        self.origin_y = y
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.pos_x = float(x)
        self.direction: float = 1.0
