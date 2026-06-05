# From: biomes.py:1372

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 32, 38
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Stalk
        pygame.draw.rect(self._base, (240, 230, 210), (W // 2 - 4, 12, 8, H - 12))
        # Cap (rounded fungus head)
        pygame.draw.ellipse(self._base, (100, 160, 100), (2, 0, W - 4, 22))
        pygame.draw.ellipse(self._base, (150, 200, 140), (6, 2, W - 12, 10))
        # Dark spots
        for dx, dy in [(W // 3, 10), (W * 2 // 3, 12), (W // 2, 6)]:
            pygame.draw.circle(self._base, (60, 90, 60), (dx, dy), 2)
        # Eyes
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 - 4, 14), 2)
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 + 4, 14), 2)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 - 4, 14), 1)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 + 4, 14), 1)
        self.image = self._base.copy()
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.puff_timer: float = random.uniform(0.5, SPORE_INTERVAL)
        self.pending_spores: list[PoisonSpore] = []
        self.alive_flag: bool = True
        self.flash: float = 0.0
