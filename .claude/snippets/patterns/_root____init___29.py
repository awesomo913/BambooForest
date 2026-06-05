# From: biomes.py:1218

    def __init__(self, x: int, y: int, patrol_width: float = 200.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (*COL_WHITE, 60), (2, 2, 32, 32))
        pygame.draw.circle(self.image, (*COL_ICE, 80), (12, 14), 3)
        pygame.draw.circle(self.image, (*COL_ICE, 80), (24, 14), 3)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
