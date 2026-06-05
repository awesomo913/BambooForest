# From: biomes.py:1023

    def __init__(self, x: int, y: int, patrol_width: float = 100.0) -> None:
        super().__init__()
        self.image = pygame.Surface((36, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (160, 120, 60), (4, 8, 28, 18))
        pygame.draw.rect(self.image, (140, 100, 40), (28, 2, 6, 10))
        pygame.draw.circle(self.image, (200, 180, 60), (32, 2), 3)
        pygame.draw.circle(self.image, COL_WHITE, (12, 14), 3)
        pygame.draw.circle(self.image, COL_WHITE, (22, 14), 3)
        pygame.draw.circle(self.image, COL_BLACK, (13, 14), 2)
        pygame.draw.circle(self.image, COL_BLACK, (21, 14), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.fire_timer: float = SCORPION_FIRE_RATE
        self._pending_proj: list[ScorpionProjectile] = []
