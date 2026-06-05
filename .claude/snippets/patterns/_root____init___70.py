# From: ui.py:454

    def __init__(self) -> None:
        self.title_y: float = -60.0
        self.title_target_y: float = SCREEN_HEIGHT * 0.09
        self.prompt_timer: float = 0.0
        self._bg: pygame.Surface | None = None
        # Interactive character selection
        self._card_rects: list[tuple[pygame.Rect, dict]] = []
        self.selected_char: dict | None = None
        # Dropdown state: gallery is HIDDEN by default to keep menu clean
        self.gallery_open: bool = False
        self._gallery_button_rect: pygame.Rect | None = None
