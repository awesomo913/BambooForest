# From: sprites.py:555
# Two-frame bouncing slime enemy -- green jelly blob.

def _generate_slime_frames() -> list[pygame.Surface]:
    """Two-frame bouncing slime enemy -- green jelly blob."""
    frames = []
    # Frame 0: normal shape
    s0 = pygame.Surface((30, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(s0, (50, 180, 80), (2, 6, 26, 22))
    pygame.draw.ellipse(s0, (70, 210, 100), (6, 10, 18, 14))  # highlight
    pygame.draw.circle(s0, COL_WHITE, (10, 14), 3)
    pygame.draw.circle(s0, COL_WHITE, (20, 14), 3)
    pygame.draw.circle(s0, COL_BLACK, (11, 14), 2)
    pygame.draw.circle(s0, COL_BLACK, (19, 14), 2)
    pygame.draw.arc(s0, COL_BLACK, (11, 18, 8, 5), 3.14, 6.28, 1)
    frames.append(s0)
    # Frame 1: squished (wider, shorter)
    s1 = pygame.Surface((30, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(s1, (50, 180, 80), (0, 10, 30, 18))
    pygame.draw.ellipse(s1, (70, 210, 100), (4, 13, 22, 12))
    pygame.draw.circle(s1, COL_WHITE, (10, 17), 3)
    pygame.draw.circle(s1, COL_WHITE, (20, 17), 3)
    pygame.draw.circle(s1, COL_BLACK, (11, 17), 2)
    pygame.draw.circle(s1, COL_BLACK, (19, 17), 2)
    pygame.draw.arc(s1, COL_BLACK, (11, 20, 8, 4), 3.14, 6.28, 1)
    frames.append(s1)
    return frames
