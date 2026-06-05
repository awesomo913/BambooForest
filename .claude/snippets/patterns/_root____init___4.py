# From: bamboo_app.py:30

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill((255, 0, 0)) # Red Boss
        self.rect = self.image.get_rect(topleft=(random.randint(400, 750), random.randint(50, 550)))
