# From: sprites.py:123
# 25x25 heart shape.

def generate_heal_surface() -> pygame.Surface:
    """25x25 heart shape."""
    surf = pygame.Surface((25, 25), pygame.SRCALPHA)
    pygame.draw.circle(surf, COL_HEAL_RED, (8, 8), 6)
    pygame.draw.circle(surf, COL_HEAL_RED, (17, 8), 6)
    pygame.draw.polygon(surf, COL_HEAL_RED, [(2, 10), (12, 23), (23, 10)])
    pygame.draw.circle(surf, COL_HEAL_PINK, (7, 6), 2)
    return surf
