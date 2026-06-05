# From: module_auto.py:100

class Bamboo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("bamboo.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (20, 55))
        self.rect = self.image.get_rect(bottomleft=(x, y))
