# From: ui.py:77

    def __init__(self, text: str, x: float, y: float, color: tuple) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life: float = 1.0
        self.max_life: float = 1.0
