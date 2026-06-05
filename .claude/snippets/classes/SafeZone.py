# From: sprites.py:1852
# Forest clearing that acts as the level goal (replaces the old flag).

class SafeZone(pygame.sprite.Sprite):
    """Forest clearing that acts as the level goal (replaces the old flag)."""
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        height = FLOOR_Y - y + (540 - FLOOR_Y)
        self.image = generate_safe_zone(max(80, height))
        self.rect = self.image.get_rect(bottomleft=(x, 540))
