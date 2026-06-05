# From: ui.py:59
# Small 10x16 bamboo with optional checkmark.

def _draw_bamboo_icon(screen: pygame.Surface, x: int, y: int,
                      checked: bool = False) -> None:
    """Small 10x16 bamboo with optional checkmark."""
    c = COL_BAMBOO if not checked else (180, 180, 180)
    pygame.draw.rect(screen, c, (x + 3, y, 4, 16))
    pygame.draw.rect(screen, (50, 120, 0), (x + 2, y + 5, 6, 2))
    pygame.draw.rect(screen, (50, 120, 0), (x + 2, y + 11, 6, 2))
    if checked:
        # Green checkmark overlay
        pygame.draw.line(screen, (50, 220, 50), (x + 1, y + 8), (x + 4, y + 12), 2)
        pygame.draw.line(screen, (50, 220, 50), (x + 4, y + 12), (x + 9, y + 3), 2)
