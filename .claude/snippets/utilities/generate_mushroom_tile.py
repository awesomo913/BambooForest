# From: biomes.py:175
# Bioluminescent fungal soil -- dark purple with glowing spores.

def generate_mushroom_tile(width: int, height: int) -> pygame.Surface:
    """Bioluminescent fungal soil -- dark purple with glowing spores."""
    surf = pygame.Surface((width, height))
    # Base: deep moss purple
    for y in range(height):
        t = y / max(1, height)
        c = (int(55 - 20 * t), int(30 - 10 * t), int(65 - 20 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Top moss
    pygame.draw.rect(surf, (80, 160, 110), (0, 0, width, 3))
    pygame.draw.rect(surf, (120, 200, 140), (0, 0, width, 1))
    # Glowing spores (pink/cyan pixels)
    for _ in range(width // 6):
        sx = random.randint(1, width - 2)
        sy = random.randint(3, height - 2)
        col = random.choice([(220, 100, 200), (100, 220, 220), (200, 220, 100)])
        surf.set_at((sx, sy), col)
    # Tiny mushroom stems along top
    for _ in range(width // 30):
        mx = random.randint(2, width - 4)
        pygame.draw.line(surf, (200, 220, 200), (mx, 3), (mx, 6), 1)
        pygame.draw.circle(surf, (220, 100, 180), (mx, 2), 2)
    return surf
