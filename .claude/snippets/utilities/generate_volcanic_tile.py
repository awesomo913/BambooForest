# From: biomes.py:39
# Dark volcanic basalt with orange lava crack highlights.

def generate_volcanic_tile(width: int, height: int) -> pygame.Surface:
    """Dark volcanic basalt with orange lava crack highlights."""
    surf = pygame.Surface((width, height))
    # Dark rock base
    for y in range(height):
        t = y / max(1, height)
        c = (int(45 - 15 * t), int(30 - 10 * t), int(25 - 5 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Top crust (cooled lava)
    pygame.draw.rect(surf, (80, 50, 40), (0, 0, width, 4))
    pygame.draw.rect(surf, (120, 70, 40), (0, 0, width, 2))
    # Lava cracks (random horizontal squiggles)
    for _ in range(width // 20):
        cx = random.randint(0, width - 10)
        cy = random.randint(6, height - 4)
        cw = random.randint(6, 14)
        pygame.draw.line(surf, (220, 80, 30), (cx, cy), (cx + cw, cy + 2), 1)
        pygame.draw.line(surf, (255, 150, 60), (cx, cy), (cx + cw, cy + 2), 1)
    # Pumice specks
    for _ in range(width * height // 50):
        nx = random.randint(1, width - 2)
        ny = random.randint(5, height - 2)
        surf.set_at((nx, ny), (80, 60, 55))
    # Edge
    pygame.draw.rect(surf, (20, 15, 20), (0, 0, 2, height))
    pygame.draw.rect(surf, (20, 15, 20), (width - 2, 0, 2, height))
    return surf
