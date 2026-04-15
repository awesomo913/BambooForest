import random
import pygame
import sys

# --- HARDWARE ACCELERATED SPRITES ---
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

class Bamboo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 55))
        self.image.fill((34, 139, 34)) # Green Bamboo
        self.rect = self.image.get_rect(topleft=(random.randint(50, 750), random.randint(50, 550)))

class MutantPanda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill((255, 0, 0)) # Red Boss
        self.rect = self.image.get_rect(topleft=(random.randint(400, 750), random.randint(50, 550)))

# --- MAIN ENGINE ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Bamboo Forest: Hardware Accelerated")
    clock = pygame.time.Clock()
    
    # Initialize Sprite Groups for massive performance gains
    all_sprites = pygame.sprite.Group()
    bamboos = pygame.sprite.Group()
    
    panda = Panda(100, 300)
    mutant = MutantPanda()
    all_sprites.add(panda, mutant)
    
    for _ in range(18):
        b = Bamboo()
        bamboos.add(b)
        all_sprites.add(b)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

        # Input & Movement
        keys = pygame.key.get_pressed()
        panda.update(keys)

        # Collision Logic 1: Eating Bamboo
        # True flag tells Pygame to instantly delete the bamboo sprite from RAM when touched
        eaten_bamboo = pygame.sprite.spritecollide(panda, bamboos, True)
        for b in eaten_bamboo:
            panda.xp += 10

        # Collision Logic 2: Boss Fight
        if pygame.sprite.collide_rect(panda, mutant):
            panda.health -= 1

        # Rendering
        screen.fill((200, 255, 200)) 
        all_sprites.draw(screen) # Draws everything in 1 optimized hardware call
        
        # UI Health Bar overlay
        if panda.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (10, 10, panda.health * 2, 20))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
