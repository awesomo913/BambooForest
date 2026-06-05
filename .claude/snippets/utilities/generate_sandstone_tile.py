# From: biomes.py:92
# Layered tan sandstone with erosion marks.

def generate_sandstone_tile(width: int, height: int) -> pygame.Surface:
    """Layered tan sandstone with erosion marks."""
    surf = pygame.Surface((width, height))
    # Layered bands of varying tan
    band_colors = [
        (210, 175, 120), (195, 160, 105), (180, 145, 90),
        (170, 135, 85), (160, 125, 80),
    ]
    band_h = max(2, height // len(band_colors))
    for i, c in enumerate(band_colors):
        pygame.draw.rect(surf, c, (0, i * band_h, width, band_h))
    # Top lighter stripe (wind-polished)
    pygame.draw.rect(surf, (225, 195, 140), (0, 0, width, 3))
    # Erosion divots
    for _ in range(width // 15):
        ex = random.randint(2, width - 4)
        ey = random.randint(4, height - 2)
        pygame.draw.ellipse(surf, (150, 115, 75), (ex, ey, 4, 2))
    # Specks
    for _ in range(width * height // 60):
        nx = random.randint(1, width - 2)
        ny = random.randint(3, height - 2)
        shade = random.randint(-15, 15)
        surf.set_at((nx, ny),
                    (max(0, min(255, 180 + shade)),
                     max(0, min(255, 145 + shade)),
                     max(0, min(255, 90 + shade))))
    pygame.draw.rect(surf, (120, 95, 60), (0, 0, 2, height))
    pygame.draw.rect(surf, (120, 95, 60), (width - 2, 0, 2, height))
    return surf
