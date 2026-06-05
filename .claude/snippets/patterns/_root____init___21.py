# From: biomes.py:711

    def __init__(self, x: int, y: int, patrol_width: float = 150.0) -> None:
        super().__init__()
        self.image = pygame.Surface((30, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (180, 200, 40), (0, 4, 30, 24))
        pygame.draw.circle(self.image, COL_WHITE, (10, 12), 3)
        pygame.draw.circle(self.image, COL_WHITE, (20, 12), 3)
        pygame.draw.circle(self.image, COL_BLACK, (11, 12), 2)
        pygame.draw.circle(self.image, COL_BLACK, (19, 12), 2)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.trail_timer: float = 0.0
        self._pending_trails: list[ToxicTrail] = []
