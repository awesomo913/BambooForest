# From: backgrounds.py:25

    def __init__(self) -> None:
        self.w: int = SCREEN_WIDTH
        self.scroll_factor: float = 0.18
        surface = self._build()
        # Convert to display format for faster blits (Pi 1 optimization).
        # Fallback if display not initialized yet.
        try:
            self.surface: pygame.Surface = surface.convert()
        except pygame.error:
            self.surface = surface
