# From: biomes.py:1502

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 30, 30
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.ellipse(self._base, (220, 80, 30), (0, 0, W, H))
        pygame.draw.ellipse(self._base, (255, 150, 50), (4, 2, W - 8, H - 8))
        pygame.draw.circle(self._base, (255, 240, 120), (W // 2, H // 2), 6)
        # Fiery eyes
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 - 5, H // 2 - 2), 2)
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 + 5, H // 2 - 2), 2)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 - 5, H // 2 - 2), 1)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 + 5, H // 2 - 2), 1)
        self.image = self._base
        # Spawn far below, then leap periodically
        self.start_x = float(x)
        self.start_y = float(y)
        self.rect = self.image.get_rect(center=(x, y + 200))  # submerged
        self._px, self._py = self.start_x, self.start_y + 200
        self._vy = 0.0
        self.state = "submerged"  # submerged / leaping / falling
        self.leap_timer: float = random.uniform(1.0, LEAPER_INTERVAL)
        self.alive_flag = True
        self.flash: float = 0.0
