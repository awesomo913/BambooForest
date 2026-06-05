# From: biomes.py:2136

    def __init__(self, x, y, patrol_width=0.0):
        super().__init__()
        self._base = self._make_surf(False)
        self._open = self._make_surf(True)
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self.base_x, self.base_y = float(x), float(y)
        self.alive_flag = True
        self.flash = 0.0
        self._pulse = 0.0
        self.open_timer = random.uniform(1.5, 3.0)
        self.state = "closed"
