# From: biomes.py:346
# Ethereal void -- deep purple with swirling stars.

def generate_void_tile(width: int, height: int) -> pygame.Surface:
    """Ethereal void -- deep purple with swirling stars."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height)
        c = (int(35 - 10 * t), int(15 - 5 * t), int(65 - 20 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Top ether-glow edge
    pygame.draw.rect(surf, (160, 100, 220), (0, 0, width, 3))
    pygame.draw.rect(surf, (220, 180, 255), (0, 0, width, 1))
    # Purple sparkle stars
    for _ in range(width // 8):
        sx = random.randint(1, width - 2)
        sy = random.randint(3, height - 2)
        col = random.choice([(220, 180, 255), (180, 140, 230), (255, 220, 255)])
        surf.set_at((sx, sy), col)
    # Vertical ether wisps
    for _ in range(width // 25):
        wx = random.randint(2, width - 4)
        pygame.draw.line(surf, (120, 80, 180),
                        (wx, 3), (wx + random.randint(-2, 2), height - 2), 1)
    return surf
