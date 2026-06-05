# From: sprites.py:1674

    def __init__(self, x: int, y: int, flight_range: float = 200.0) -> None:
        super().__init__()
        self._frames = _generate_flying_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.flight_range = flight_range
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.time: float = random.uniform(0, 6.28)
        self.alive_flag = True
        self.anim_timer: float = 0.0
