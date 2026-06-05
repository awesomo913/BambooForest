# From: biomes.py:1997

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 34, 28
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        body_pts = [(W // 2, 2), (W - 2, H // 2),
                    (W - 6, H - 2), (W // 2, H - 6),
                    (6, H - 2), (2, H // 2)]
        pygame.draw.polygon(self._base, (180, 100, 200, 180), body_pts)
        pygame.draw.polygon(self._base, (230, 160, 255, 220), body_pts, 2)
        pygame.draw.circle(self._base, (255, 80, 80),
                          (W // 2 - 5, H // 2), 3)
        pygame.draw.circle(self._base, (255, 80, 80),
                          (W // 2 + 5, H // 2), 3)
        pygame.draw.circle(self._base, COL_WHITE,
                          (W // 2 - 5, H // 2 - 1), 1)
        pygame.draw.circle(self._base, COL_WHITE,
                          (W // 2 + 5, H // 2 - 1), 1)
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self._px, self._py = float(x), float(y)
        self._vx, self._vy = 0.0, 0.0
        self.alive_flag = True
        self.flash: float = 0.0
        self._base_speed = 90.0
        self._chase_speed = 180.0
