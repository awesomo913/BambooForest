# From: bamboo_forest.py:91

class MutantPanda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("mutant.png", 45, 45, (255, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.velocity_y = 0
        self.gravity = 0.8
        self.speed_x = 3 # Sped up the enemy

    def update(self, player, platforms):
        self.velocity_y += self.gravity
        if self.velocity_y > 12: self.velocity_y = 12
        self.rect.y += self.velocity_y

        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0

        # AI: Chase player if within 600 pixels
        dist = player.rect.centerx - self.rect.centerx
        if abs(dist) < 600 and abs(player.rect.centery - self.rect.centery) < 300:
            if dist > 0: self.rect.x += self.speed_x
            elif dist < 0: self.rect.x -= self.speed_x
