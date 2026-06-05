# From: biomes.py:285
# Corrupted boss-lair ground -- crimson shadow with dark veins.

def generate_lair_tile(width: int, height: int) -> pygame.Surface:
    """Corrupted boss-lair ground -- crimson shadow with dark veins."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height)
        c = (int(50 - 15 * t), int(20 - 5 * t), int(35 - 10 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Top crust (dark red-purple)
    pygame.draw.rect(surf, (80, 30, 50), (0, 0, width, 3))
    pygame.draw.rect(surf, (130, 40, 70), (0, 0, width, 1))
    # Crimson veins
    for _ in range(width // 14):
        vx = random.randint(2, width - 10)
        vy = random.randint(5, height - 4)
        vlen = random.randint(5, 14)
        pygame.draw.line(surf, (180, 50, 70), (vx, vy),
                        (vx + vlen, vy + random.randint(-2, 2)), 1)
    # Pulsing ember spots
    for _ in range(width // 25):
        ex = random.randint(2, width - 4)
        ey = random.randint(5, height - 3)
        pygame.draw.circle(surf, (220, 80, 50), (ex, ey), 1)
        pygame.draw.circle(surf, (255, 150, 100), (ex, ey), 1, 1)
    # Dark specks
    for _ in range(width // 8):
        sx = random.randint(1, width - 2)
        sy = random.randint(3, height - 2)
        surf.set_at((sx, sy), (30, 10, 20))
    return surf
