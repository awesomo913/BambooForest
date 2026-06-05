# From: biomes.py:1294

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._base = self._make_surf(False)
        self._compressed = self._make_surf(True)
        self.image = self._base
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.compress_timer: float = 0.0
