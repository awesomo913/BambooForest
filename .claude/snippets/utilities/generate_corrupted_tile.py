# From: biomes.py:253
# Sickly forest ground -- dark green with purple corruption veins.

def generate_corrupted_tile(width: int, height: int) -> pygame.Surface:
    """Sickly forest ground -- dark green with purple corruption veins."""
    surf = pygame.Surface((width, height))
    # Darker moss base
    for y in range(height):
        t = y / max(1, height)
        c = (int(55 - 20 * t), int(85 - 30 * t), int(50 - 20 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Sickly grass top (darkened)
    pygame.draw.rect(surf, (70, 110, 60), (0, 0, width, 3))
    pygame.draw.rect(surf, (100, 150, 80), (0, 0, width, 1))
    # Purple corruption veins creeping through
    for _ in range(width // 15):
        vx = random.randint(2, width - 10)
        vy = random.randint(4, height - 4)
        vlen = random.randint(4, 12)
        pygame.draw.line(surf, (140, 60, 150), (vx, vy),
                        (vx + vlen, vy + random.randint(-2, 2)), 1)
    # Dead grass specks
    for _ in range(width // 8):
        sx = random.randint(1, width - 2)
        sy = random.randint(3, height - 2)
        surf.set_at((sx, sy), (60, 70, 40))
    # Rot spots
    for _ in range(width // 30):
        rx = random.randint(3, width - 6)
        ry = random.randint(5, height - 4)
        pygame.draw.circle(surf, (80, 40, 90), (rx, ry), 2)
    return surf
