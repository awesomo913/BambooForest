# From: sprites.py:1620

    def __init__(self, x: int, y: int, patrol_width: float = 180.0) -> None:
        super().__init__()
        self._frames = _generate_slime_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.patrol_width = patrol_width
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.on_ground = False
        self.hop_timer: float = 0.0
