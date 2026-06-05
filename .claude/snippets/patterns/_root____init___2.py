# From: bamboo_app.py:7

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 0)) # Black Panda
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 6
        self.health = 100
        self.xp = 0
