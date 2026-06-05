# From: bamboo_app.py:22

class Bamboo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 55))
        self.image.fill((34, 139, 34)) # Green Bamboo
        self.rect = self.image.get_rect(topleft=(random.randint(50, 750), random.randint(50, 550)))
