# From: sprites.py:109
# 20x55 bamboo stalk with joints and leaves.

def generate_bamboo_surface() -> pygame.Surface:
    """20x55 bamboo stalk with joints and leaves."""
    surf = pygame.Surface((20, 55), pygame.SRCALPHA)
    pygame.draw.rect(surf, COL_BAMBOO, (7, 0, 6, 55))
    # Gradient stripe on stalk
    pygame.draw.rect(surf, (90, 170, 20), (9, 0, 2, 55))
    for jy in (12, 27, 42):
        pygame.draw.rect(surf, COL_BAMBOO_JOINT, (6, jy, 8, 3))
    # Leaves
    pygame.draw.polygon(surf, (50, 160, 30), [(10, 0), (19, 6), (10, 8)])
    pygame.draw.polygon(surf, (40, 140, 20), [(10, 0), (1, 6), (10, 8)])
    return surf
