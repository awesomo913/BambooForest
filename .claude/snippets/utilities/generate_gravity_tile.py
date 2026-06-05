# From: biomes.py:226
# Arcane metal with glowing circuit veins.

def generate_gravity_tile(width: int, height: int) -> pygame.Surface:
    """Arcane metal with glowing circuit veins."""
    surf = pygame.Surface((width, height))
    # Dark metallic base
    for y in range(height):
        t = y / max(1, height)
        c = (int(40 - 10 * t), int(30 - 10 * t), int(55 - 15 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Top ridge
    pygame.draw.rect(surf, (120, 90, 160), (0, 0, width, 3))
    pygame.draw.rect(surf, (180, 150, 220), (0, 0, width, 1))
    # Circuit lines
    for _ in range(width // 12):
        cx = random.randint(2, width - 10)
        cy = random.randint(5, height - 3)
        cw = random.randint(6, 14)
        pygame.draw.line(surf, (150, 120, 220), (cx, cy), (cx + cw, cy), 1)
        pygame.draw.circle(surf, (220, 180, 255), (cx, cy), 1)
        pygame.draw.circle(surf, (220, 180, 255), (cx + cw, cy), 1)
    # Rivets
    for _ in range(width // 25):
        rx = random.randint(2, width - 4)
        pygame.draw.circle(surf, (80, 60, 100), (rx, height // 2), 1)
    return surf
