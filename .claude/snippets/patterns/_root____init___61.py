# From: sprites.py:1575

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._frames = _generate_chaser_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.velocity_y: float = 0.0
        self.alive_flag = True
        self.facing_right = True
        self.anim_timer: float = 0.0
