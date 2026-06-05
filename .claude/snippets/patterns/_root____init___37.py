# From: biomes.py:1655

    def __init__(self, x: int, y: int, patrol_width: float = 150.0) -> None:
        super().__init__()
        W, H = 30, 22
        self._left = pygame.Surface((W, H), pygame.SRCALPHA)
        # Teal body
        pygame.draw.ellipse(self._left, (80, 140, 160), (3, 4, W - 6, H - 6))
        # Orange claws
        pygame.draw.circle(self._left, (220, 130, 60), (3, H // 2), 4)
        pygame.draw.circle(self._left, (220, 130, 60), (W - 3, H // 2), 4)
        # Eye stalks
        pygame.draw.line(self._left, (80, 140, 160),
                         (W // 2 - 3, 5), (W // 2 - 3, 1), 1)
        pygame.draw.line(self._left, (80, 140, 160),
                         (W // 2 + 3, 5), (W // 2 + 3, 1), 1)
        pygame.draw.circle(self._left, COL_BLACK, (W // 2 - 3, 1), 1)
        pygame.draw.circle(self._left, COL_BLACK, (W // 2 + 3, 1), 1)
        self._right = pygame.transform.flip(self._left, True, False)
        self.image = self._left
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self._px = float(x)
        self._py = float(y - H)
        self.vx = -TIDAL_CRAB_SPEED
        self.vy = 0.0
        self.start_x = x
        self.patrol_width = patrol_width
        self.alive_flag = True
        self.flash: float = 0.0
