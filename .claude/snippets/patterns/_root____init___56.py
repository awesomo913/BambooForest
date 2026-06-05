# From: sprites.py:1229

    def __init__(self, x: int, y: int, direction: float) -> None:
        super().__init__()
        self._base = self._make_shard()
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vx = 800.0 * direction  # faster than shuriken
        self.vy = 0.0  # travels straight (no gravity)
        self.rotation: float = 0.0
        self.lifetime: float = 1.5  # ~1200px travel range
        self.damage: int = 999  # instant-kill vs non-boss enemies
        # Trail buffer
        self._trail: list[tuple[float, float]] = []
