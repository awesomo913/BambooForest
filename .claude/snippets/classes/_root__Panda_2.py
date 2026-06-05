# From: module_auto.py:43

class Panda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("panda.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 6
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.is_on_ground = False
        self.health = 100
        self.score = 0
        self.invincible_timer = 0

    def update(self, keys, platforms):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if keys[pygame.K_LEFT]: self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed_x

        # Horizontal Collision
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if keys[pygame.K_RIGHT]: self.rect.right = hit.rect.left
            elif keys[pygame.K_LEFT]: self.rect.left = hit.rect.right

        # Vertical Movement
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.is_on_ground:
            self.speed_y = self.jump_power
            self.is_on_ground = False

        self.speed_y += self.gravity
        if self.speed_y > 12: self.speed_y = 12
        self.rect.y += self.speed_y

        # Vertical Collision
        self.is_on_ground = False
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.speed_y > 0: # Landing
                self.rect.bottom = hit.rect.top
                self.speed_y = 0
                self.is_on_ground = True
            elif self.speed_y < 0: # Hitting head
                self.rect.top = hit.rect.bottom
                self.speed_y = 0
