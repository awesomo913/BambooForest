# From: biomes.py:151
# Pale blue-white salt crystal surface, reflective.

def generate_salt_tile(width: int, height: int) -> pygame.Surface:
    """Pale blue-white salt crystal surface, reflective."""
    surf = pygame.Surface((width, height))
    # Near-white body with pale blue hint
    for y in range(height):
        t = y / max(1, height)
        c = (int(220 - 20 * t), int(235 - 15 * t), int(250 - 10 * t))
        pygame.draw.line(surf, c, (0, y), (width, y))
    # Bright top
    pygame.draw.rect(surf, (245, 250, 255), (0, 0, width, 4))
    # Crystal facet lines
    for cx in range(0, width, random.randint(20, 35)):
        pygame.draw.line(surf, (180, 210, 235), (cx, 4),
                         (cx + random.randint(-3, 3), height), 1)
    # Sparkle highlights
    for _ in range(width // 10):
        sx = random.randint(1, width - 2)
        sy = random.randint(3, height - 2)
        surf.set_at((sx, sy), (255, 255, 255))
    pygame.draw.rect(surf, (160, 190, 220), (0, 0, 2, height))
    pygame.draw.rect(surf, (160, 190, 220), (width - 2, 0, 2, height))
    return surf
