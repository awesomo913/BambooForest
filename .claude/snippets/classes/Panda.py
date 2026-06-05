# From: bamboo_app.py:6

class Panda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 0)) # Black Panda
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 6
        self.health = 100
        self.xp = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800: self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600: self.rect.y += self.speed
