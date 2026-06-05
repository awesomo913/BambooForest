# From: sprites.py:368
# Two-frame mushroom patrol enemy -- cleaner design.

def _generate_mushroom_frames() -> list[pygame.Surface]:
    """Two-frame mushroom patrol enemy -- cleaner design."""
    frames = []
    for dy in (0, 1):
        surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        # Cap (red dome with white spots)
        pygame.draw.ellipse(surf, (180, 40, 40), (2, 2 + dy, 32, 20))
        pygame.draw.ellipse(surf, (200, 55, 55), (4, 4 + dy, 28, 16))
        for sx, sy in ((10, 6), (20, 4), (26, 10), (8, 12)):
            pygame.draw.circle(surf, COL_WHITE, (sx, sy + dy), 2)
        # Stem
        pygame.draw.rect(surf, (230, 210, 180), (12, 18 + dy, 12, 12), border_radius=3)
        # Eyes (angry)
        pygame.draw.circle(surf, COL_WHITE, (15, 22 + dy), 3)
        pygame.draw.circle(surf, COL_WHITE, (21, 22 + dy), 3)
        pygame.draw.circle(surf, COL_BLACK, (16, 22 + dy), 2)
        pygame.draw.circle(surf, COL_BLACK, (20, 22 + dy), 2)
        # Angry brows
        pygame.draw.line(surf, COL_BLACK, (12, 18 + dy), (17, 20 + dy), 2)
        pygame.draw.line(surf, COL_BLACK, (24, 18 + dy), (19, 20 + dy), 2)
        # Feet
        pygame.draw.ellipse(surf, (200, 180, 150), (10, 30 + dy, 8, 6))
        pygame.draw.ellipse(surf, (200, 180, 150), (18, 30 + dy, 8, 6))
        frames.append(surf)
    return frames
