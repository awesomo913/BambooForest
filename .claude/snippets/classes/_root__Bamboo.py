# From: bamboo_forest.py:79

class Bamboo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("bamboo.png", 20, 55, (34, 139, 34))
        self.rect = self.image.get_rect(bottomleft=(x, y))
