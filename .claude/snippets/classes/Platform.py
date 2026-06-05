# From: module_auto.py:93

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h)).convert()
        self.image.fill((101, 67, 33)) # Dark Brown Dirt
        self.rect = self.image.get_rect(topleft=(x, y))
