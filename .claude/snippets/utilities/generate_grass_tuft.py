# From: sprites.py:355
# Small decorative grass blades.

def generate_grass_tuft() -> pygame.Surface:
    """Small decorative grass blades."""
    surf = pygame.Surface((12, 10), pygame.SRCALPHA)
    greens = [(30, 130, 30), (45, 155, 45), (25, 115, 25)]
    for i, gx in enumerate((2, 5, 8)):
        c = greens[i % len(greens)]
        bh = random.randint(5, 9)
        pygame.draw.line(surf, c, (gx, 9), (gx + random.randint(-2, 2), 9 - bh), 2)
    return surf
