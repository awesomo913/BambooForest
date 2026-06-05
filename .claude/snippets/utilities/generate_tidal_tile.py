# From: biomes.py:201
# Barnacled coastal stone with teal water stains.

def generate_tidal_tile(width: int, height: int) -> pygame.Surface:
    """Barnacled coastal stone with teal water stains."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height)
        c = (int(90 - 30 * t), int(110 - 30 * t), int(130 - 30 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Wet top strip
    pygame.draw.rect(surf, (60, 130, 150), (0, 0, width, 3))
    pygame.draw.rect(surf, (90, 170, 190), (0, 0, width, 1))
    # Barnacle clusters
    for _ in range(width // 15):
        bx = random.randint(2, width - 4)
        by = random.randint(4, height - 4)
        pygame.draw.circle(surf, (240, 230, 210), (bx, by), 2)
        pygame.draw.circle(surf, (180, 160, 140), (bx, by), 2, 1)
    # Teal drips
    for _ in range(width // 25):
        dx = random.randint(0, width - 2)
        pygame.draw.line(surf, (80, 180, 180), (dx, 3),
                         (dx, random.randint(5, height - 2)), 1)
    return surf
