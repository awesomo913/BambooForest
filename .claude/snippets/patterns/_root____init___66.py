# From: sprites.py:1854

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        height = FLOOR_Y - y + (540 - FLOOR_Y)
        self.image = generate_safe_zone(max(80, height))
        self.rect = self.image.get_rect(bottomleft=(x, 540))
