# From: ui.py:106

    def __init__(self) -> None:
        self.displayed_hp: float = 100.0
        self.floating_texts: list[FloatingText] = []
        self.combo_display_timer: float = 0.0
        self.combo_scale: float = 1.0
        self.total_bamboos: int = 0
        self.collected_bamboos: int = 0
        self.lives: int = 3
