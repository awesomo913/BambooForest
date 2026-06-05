# From: module_auto.py:109

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("heal.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(bottomleft=(x, y))
