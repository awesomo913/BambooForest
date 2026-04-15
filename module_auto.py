import random
import pygame
import sys
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load images
def load_image(filename):
    try:
        return pygame.image.load(filename).convert_alpha()
    except FileNotFoundError:
        print(f"Error: No file '{filename}' found in working directory.")
        return None

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - SCREEN_WIDTH), x)  # Right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)

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

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h)).convert()
        self.image.fill((101, 67, 33)) # Dark Brown Dirt
        self.rect = self.image.get_rect(topleft=(x, y))

class Bamboo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("bamboo.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (20, 55))
        self.rect = self.image.get_rect(bottomleft=(x, y))

class HealingItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("heal.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(bottomleft=(x, y))

def build_level(world_width):
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bamboos = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    heals = pygame.sprite.Group()

    # Solid Continuous Floor
    floor = Platform(0, 550, world_width, 50)
    platforms.add(floor)
    all_sprites.add(floor)

    # Elevated Platforms
    plat_coords = [
        (400, 420, 200), (800, 350, 150), (1200, 420, 250), 
        (1600, 280, 150), (2000, 400, 200), (2400, 300, 250)
    ]
    
    for cx, cy, cw in plat_coords:
        p = Platform(cx, cy, cw, 20)
        platforms.add(p)
        all_sprites.add(p)

        # Always spawn a Bamboo score item on platforms
        b = Bamboo(cx + (cw // 2), cy)
        bamboos.add(b)
        all_sprites.add(b)

        # 60% chance to spawn an enemy guarding it
        if random.random() > 0.4:
            m = MutantPanda(cx + 20, cy - 10)
            enemies.add(m)
            all_sprites.add(m)
            
        # 30% chance to spawn a heal item
        if random.random() > 0.7:
            h = HealingItem(cx + cw - 30, cy)
            heals.add(h)
            all_sprites.add(h)

    # End Goal Flag/Block
    goal = Platform(2950, 400, 50, 200)
    platforms.add(goal)
    all_sprites.add(goal)

    return all_sprites, platforms, bamboos, enemies, heals

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bamboo Forest: Uncensored")
    clock = pygame.time.Clock()
    
    bg_image = load_image("background.png")
    world_width = 3000
    camera = Camera(world_width, SCREEN_HEIGHT)
    state = "MENU"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and state in ["MENU", "GAME_OVER", "VICTORY"]:
                    all_sprites, platforms, bamboos, enemies, heals = build_level(world_width)
                    panda = Panda(100, 400)
                    all_sprites.add(panda)
                    state = "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    running = False

        if state == "PLAYING":
            keys = pygame.key.get_pressed()
            panda.update(keys, platforms)
            enemies.update(panda, platforms)
            camera.update(panda)

            # Mechanics
            eaten = pygame.sprite.spritecollide(panda, bamboos, True)
            for b in eaten: 
                panda.score += 100

            healed = pygame.sprite.spritecollide(panda, heals, True)
            for h in healed:
                panda.health = min(100, panda.health + 25)

            # Enemy Combat (With Invincibility Frames)
            hits = pygame.sprite.spritecollide(panda, enemies, False)
            if hits and panda.invincible_timer == 0:
                panda.health -= 25
                panda.invincible_timer = 30 # Half a second of safety

            if panda.health <= 0:
                state = "GAME_OVER"
            if panda.rect.x > 2900:
                state = "VICTORY"

        # --- DRAWING PHASE ---
        screen.blit(bg_image, (0, 0))

        if state == "PLAYING":
            for sprite in all_sprites:
                # Make panda blink if invincible
                if sprite == panda and panda.invincible_timer % 4 > 1:
                    continue
                screen.blit(sprite.image, camera.apply(sprite))
            
            # --- HIGH CONTRAST HUD ---
            pygame.draw.rect(screen, (30, 30, 30), (10, 10, 220, 70), border_radius=5) # Dark Backing
            
            # Health Bar
            draw_text(screen, "HP", 24, (255, 255, 255), 30, 25)
            pygame.draw.rect(screen, (100, 0, 0), (55, 15, 150, 20)) # Red Background
            pygame.draw.rect(screen, (0, 255, 0), (55, 15, max(0, panda.health) * 1.5, 20)) # Green Fill
            
            # Score System
            draw_text(screen, f"SCORE: {panda.score}", 32, (255, 215, 0), 100, 55)

        elif state == "MENU":
            draw_text(screen, "Bamboo Forest", 72, (0, 0, 0), 400, 200)
            draw_text(screen, "Press ENTER to Start", 36, (50, 50, 50), 400, 300)

        elif state == "GAME_OVER":
            draw_text(screen, "Game Over", 72, (255, 0, 0), 400, 200)
            draw_text(screen, "Press ENTER to Try Again", 36, (0, 0, 0), 400, 300)

        elif state == "VICTORY":
            draw_text(screen, "Victory!", 72, (34, 139, 34), 400, 200)
            draw_text(screen, f"Final Score: {panda.score}", 48, (0, 0, 0), 400, 280)
            draw_text(screen, "Press ENTER to Play Again", 36, (50, 50, 50), 400, 360)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()