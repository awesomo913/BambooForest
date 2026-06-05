# From: sprites.py:1845

class GrassTuft(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = generate_grass_tuft()
        self.rect = self.image.get_rect(bottomleft=(x, y))
