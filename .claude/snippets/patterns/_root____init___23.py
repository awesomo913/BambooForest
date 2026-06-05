# From: biomes.py:825

    def __init__(self, x: int, y: int, patrol_width: float = 120.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (180, 80, 60), (2, 2, 32, 18))
        pygame.draw.rect(self.image, (160, 60, 40), (0, 6, 6, 4))
        pygame.draw.rect(self.image, (160, 60, 40), (30, 6, 6, 4))
        pygame.draw.circle(self.image, COL_WHITE, (12, 8), 3)
        pygame.draw.circle(self.image, COL_WHITE, (24, 8), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 8), 2)
        pygame.draw.circle(self.image, COL_BLACK, (23, 8), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
