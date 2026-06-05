# From: module_auto.py:116

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
