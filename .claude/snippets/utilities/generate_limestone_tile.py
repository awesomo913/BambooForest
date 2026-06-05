# From: biomes.py:124
# Pale gray-tan limestone cave floor with fossil marks.

def generate_limestone_tile(width: int, height: int) -> pygame.Surface:
    """Pale gray-tan limestone cave floor with fossil marks."""
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height)
        c = (int(170 - 30 * t), int(165 - 30 * t), int(150 - 30 * t))
        pygame.draw.line(surf, c, (0, y), (width, y))
    pygame.draw.rect(surf, (190, 180, 165), (0, 0, width, 3))
    # Fossil impressions (small curved lines)
    for _ in range(width // 25):
        fx = random.randint(4, width - 8)
        fy = random.randint(6, height - 4)
        pygame.draw.arc(surf, (120, 115, 100), (fx, fy, 6, 4), 0, 3.14, 1)
    # Specks
    for _ in range(width * height // 70):
        nx = random.randint(1, width - 2)
        ny = random.randint(3, height - 2)
        shade = random.randint(-15, 10)
        surf.set_at((nx, ny),
                    (max(0, min(255, 155 + shade)),
                     max(0, min(255, 150 + shade)),
                     max(0, min(255, 135 + shade))))
    pygame.draw.rect(surf, (90, 85, 75), (0, 0, 2, height))
    pygame.draw.rect(surf, (90, 85, 75), (width - 2, 0, 2, height))
    return surf
