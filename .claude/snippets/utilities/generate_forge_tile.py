# From: biomes.py:317
# Industrial iron forge -- rivets, soot, ember glow.

def generate_forge_tile(width: int, height: int) -> pygame.Surface:
    """Industrial iron forge -- rivets, soot, ember glow."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height)
        c = (int(75 - 25 * t), int(65 - 20 * t), int(65 - 20 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Hot metal top edge
    pygame.draw.rect(surf, (200, 100, 60), (0, 0, width, 3))
    pygame.draw.rect(surf, (255, 180, 100), (0, 0, width, 1))
    # Rivets (darker circles) along the top edge
    for rx in range(8, width, 16):
        pygame.draw.circle(surf, (30, 30, 35), (rx, height // 2), 2)
        pygame.draw.circle(surf, (80, 80, 90), (rx - 1, height // 2 - 1), 1)
    # Ember cracks
    for _ in range(width // 15):
        cx = random.randint(2, width - 10)
        cy = random.randint(5, height - 4)
        pygame.draw.line(surf, (255, 120, 40),
                        (cx, cy), (cx + 6, cy + random.randint(-2, 2)), 1)
    # Soot specks
    for _ in range(width * height // 40):
        sx = random.randint(1, width - 2)
        sy = random.randint(2, height - 2)
        surf.set_at((sx, sy), (20, 18, 18))
    return surf
