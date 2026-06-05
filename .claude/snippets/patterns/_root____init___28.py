# From: biomes.py:1178

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_size = 16
        self.size_scale: float = 1.0
        self._regen_image()
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.base_y = y
        self.alive_flag = True
