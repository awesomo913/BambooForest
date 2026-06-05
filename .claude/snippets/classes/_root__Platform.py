# From: sprites.py:1101

class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int = 20) -> None:
        super().__init__()
        self.image = generate_platform_tile(w, h)
        self.rect = self.image.get_rect(topleft=(x, y))
