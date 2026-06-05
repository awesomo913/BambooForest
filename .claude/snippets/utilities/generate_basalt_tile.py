# From: biomes.py:69
# Hexagonal basalt columns -- dark gray with top lip.

def generate_basalt_tile(width: int, height: int) -> pygame.Surface:
    """Hexagonal basalt columns -- dark gray with top lip."""
    surf = pygame.Surface((width, height))
    # Deep gray body
    for y in range(height):
        t = y / max(1, height)
        c = (int(70 - 20 * t), int(75 - 20 * t), int(90 - 20 * t))
        pygame.draw.line(surf, c, (0, y), (width, y))
    # Hex top stripe (lighter)
    pygame.draw.rect(surf, (100, 105, 120), (0, 0, width, 3))
    # Vertical column lines (every 40px)
    for cx in range(0, width, 40):
        pygame.draw.line(surf, (40, 45, 55), (cx, 3), (cx, height), 1)
        pygame.draw.line(surf, (90, 95, 110), (cx + 1, 3), (cx + 1, height), 1)
    # Subtle horizontal banding
    for by in range(8, height, 12):
        pygame.draw.line(surf, (55, 60, 75), (0, by), (width, by), 1)
    # Edge
    pygame.draw.rect(surf, (30, 30, 40), (0, 0, 2, height))
    pygame.draw.rect(surf, (30, 30, 40), (width - 2, 0, 2, height))
    return surf
