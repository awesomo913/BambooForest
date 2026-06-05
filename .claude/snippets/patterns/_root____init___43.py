# From: biomes.py:2072

    def __init__(self, x, y, patrol_width=0.0):
        super().__init__()
        W, H = 60, 40
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.rect(self._base, (50, 50, 60), (4, 4, W - 8, H - 8))
        pygame.draw.rect(self._base, (90, 90, 110), (6, 6, W - 12, 4))
        pygame.draw.rect(self._base, (30, 30, 40), (4, H - 8, W - 8, 4))
        pygame.draw.circle(self._base, (160, 120, 60), (W // 2, 12), 4)
        pygame.draw.circle(self._base, (220, 180, 100), (W // 2, 12), 2)
        for i, j in [(8, 8), (W - 12, 8), (8, H - 12), (W - 12, H - 12)]:
            pygame.draw.circle(self._base, (20, 20, 25), (i, j), 2)
        self.image = self._base
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.base_x = float(x)
        self._top_y = 0.0
        self._bottom_y = float(y)
        self._py = self._top_y
        self.state = "holding"
        self.timer = random.uniform(1.0, 3.0)
        self.alive_flag = True
        self.flash = 0.0
