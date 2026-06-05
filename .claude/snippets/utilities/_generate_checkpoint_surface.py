# From: sprites.py:1861
# A wooden signpost with a flag -- gray when inactive, green when hit.

def _generate_checkpoint_surface(activated: bool = False) -> pygame.Surface:
    """A wooden signpost with a flag -- gray when inactive, green when hit."""
    surf = pygame.Surface((28, 60), pygame.SRCALPHA)
    # Pole
    pole_c = (100, 70, 40) if not activated else (110, 85, 50)
    pygame.draw.rect(surf, pole_c, (12, 10, 4, 50))
    # Base
    pygame.draw.rect(surf, (80, 55, 30), (6, 54, 16, 6), border_radius=2)
    # Flag
    if activated:
        flag_c = (50, 200, 80)
        flag_c2 = (40, 170, 60)
        # Checkmark on flag
        pygame.draw.polygon(surf, flag_c, [(16, 5), (28, 14), (16, 23)])
        pygame.draw.polygon(surf, flag_c2, [(16, 14), (28, 14), (16, 23)])
        pygame.draw.line(surf, COL_WHITE, (18, 15), (21, 19), 2)
        pygame.draw.line(surf, COL_WHITE, (21, 19), (26, 10), 2)
    else:
        flag_c = (160, 160, 160)
        flag_c2 = (130, 130, 130)
        pygame.draw.polygon(surf, flag_c, [(16, 5), (28, 14), (16, 23)])
        pygame.draw.polygon(surf, flag_c2, [(16, 14), (28, 14), (16, 23)])
    # Pole top knob
    pygame.draw.circle(surf, pole_c, (14, 8), 3)
    return surf
