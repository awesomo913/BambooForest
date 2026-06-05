# From: biomes.py:1877

    def __init__(self, x: int, y: int, w: int, h: int, gravity_type: str) -> None:
        super().__init__()
        self.gravity_type = gravity_type
        self.rect = pygame.Rect(x, y, w, h)
        self.image = self._make_surf(w, h, gravity_type)
        self._wave_timer: float = 0.0
