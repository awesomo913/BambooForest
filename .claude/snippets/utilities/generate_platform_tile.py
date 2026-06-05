# From: sprites.py:133
# Asian-themed platform: polished wood grain + bamboo cross-sections.

def generate_platform_tile(width: int, height: int) -> pygame.Surface:
    """Asian-themed platform: polished wood grain + bamboo cross-sections.

    Evokes a temple walkway / wooden tea-house plank.
    """
    surf = pygame.Surface((width, height))
    # Deep earthy teak base with gradient
    for y in range(height):
        t = y / max(1, height)
        c = (int(110 - 30 * t), int(70 - 18 * t), int(35 - 10 * t))
        pygame.draw.line(surf, (max(0, c[0]), max(0, c[1]), max(0, c[2])),
                         (0, y), (width, y))
    # Wood grain lines
    for gy in range(6, height, 4):
        shade = random.randint(-20, 10)
        c = (max(0, min(255, 85 + shade)),
             max(0, min(255, 52 + shade)),
             max(0, min(255, 25 + shade)))
        pygame.draw.line(surf, c, (0, gy),
                         (width, gy + random.choice([-1, 0, 1])), 1)
    # Mossy green top (zen garden moss)
    moss_h = min(5, height)
    pygame.draw.rect(surf, (55, 130, 55), (0, 0, width, moss_h))
    pygame.draw.rect(surf, (40, 105, 40), (0, moss_h - 1, width, 1))
    # Short moss tufts
    for x in range(0, width - 1, 3):
        bh = random.randint(1, 3)
        shade = random.randint(-10, 25)
        gc = (min(255, 55 + shade), min(255, 130 + shade), min(255, 55 + shade))
        pygame.draw.line(surf, gc, (x, moss_h),
                         (x + random.randint(-1, 1), moss_h - bh), 1)
    # Bamboo cross-section decorations (every ~60px)
    spacing = 60
    for bx in range(spacing // 2, width - 10, spacing):
        by = height // 2 + random.randint(-2, 2)
        # Dark rim
        pygame.draw.circle(surf, (40, 80, 20), (bx, by), 4)
        # Pale bamboo interior
        pygame.draw.circle(surf, (180, 200, 130), (bx, by), 3)
        # Center node dot
        pygame.draw.circle(surf, (90, 130, 60), (bx, by), 1)
    # Dark edge trim (lacquered corners)
    pygame.draw.rect(surf, (40, 25, 15), (0, 0, 2, height))
    pygame.draw.rect(surf, (40, 25, 15), (width - 2, 0, 2, height))
    return surf
