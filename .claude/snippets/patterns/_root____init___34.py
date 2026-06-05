# From: biomes.py:1438

    def __init__(self, world_width: int, pause_ys: list[int] | None = None) -> None:
        super().__init__()
        self.world_width = world_width
        self.pause_ys = sorted(pause_ys or [], reverse=False)  # ascending (top-most first after sort)
        # Actually we want highest-y first (deepest), then pause higher as we rise
        # pause_ys are Y values where lava pauses. Lower Y = higher on screen.
        # So after rising past y=450 (pause #1), next is y=400, then y=350.
        self.pause_ys = sorted(pause_ys or [], reverse=True)  # e.g. [450, 400, 350]
        self._next_pause_idx: int = 0
        self.current_y: float = float(LAVA_START_Y)  # starts below screen
        self.paused: bool = False
        self.pause_timer: float = 0.0
        self._base = self._make_surf()
        self.image = self._base
        self.rect = self.image.get_rect(topleft=(0, int(self.current_y)))
        self._wave_timer: float = 0.0
