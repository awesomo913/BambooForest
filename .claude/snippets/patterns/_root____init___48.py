# From: engine.py:221

    def __init__(self) -> None:
        self.w = SCREEN_WIDTH
        self.combined = self._build_combined()
        self.layers: list[tuple[pygame.Surface, float]] = [
            (self.combined, 0.18),
        ]
        # Sky is drawn first (static, no scroll)
        self.sky = self._build_sky()
