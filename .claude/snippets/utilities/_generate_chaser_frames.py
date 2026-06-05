# From: sprites.py:395
# Two-frame shadow panther chaser -- sleek dark cat with glowing eyes.

def _generate_chaser_frames() -> list[pygame.Surface]:
    """Two-frame shadow panther chaser -- sleek dark cat with glowing eyes."""
    frames = []
    for dy in (0, 1):
        surf = pygame.Surface((44, 36), pygame.SRCALPHA)
        body_c = (50, 35, 60)
        belly_c = (70, 55, 80)
        # Body (sleek ellipse)
        pygame.draw.ellipse(surf, body_c, (8, 10 + dy, 28, 18))
        pygame.draw.ellipse(surf, belly_c, (12, 15 + dy, 20, 10))
        # Head (round)
        pygame.draw.circle(surf, body_c, (12, 12 + dy), 10)
        pygame.draw.circle(surf, belly_c, (12, 14 + dy), 6)
        # Ears (triangular, clean)
        pygame.draw.polygon(surf, body_c, [(5, 8 + dy), (3, 0), (10, 5 + dy)])
        pygame.draw.polygon(surf, body_c, [(15, 6 + dy), (18, 0), (11, 3 + dy)])
        # Inner ear
        pygame.draw.polygon(surf, (100, 70, 90), [(6, 6 + dy), (4, 2), (9, 5 + dy)])
        pygame.draw.polygon(surf, (100, 70, 90), [(15, 5 + dy), (17, 2), (12, 4 + dy)])
        # Eyes (bright yellow-green, menacing)
        pygame.draw.circle(surf, (180, 255, 50), (9, 11 + dy), 3)
        pygame.draw.circle(surf, (180, 255, 50), (16, 11 + dy), 3)
        # Slit pupils
        pygame.draw.rect(surf, COL_BLACK, (9, 9 + dy, 1, 4))
        pygame.draw.rect(surf, COL_BLACK, (16, 9 + dy, 1, 4))
        # Nose
        pygame.draw.circle(surf, (30, 20, 30), (12, 16 + dy), 2)
        # Legs (slim)
        for lx in (12, 18, 26, 30):
            pygame.draw.rect(surf, body_c, (lx, 26 + dy, 4, 10), border_radius=2)
            pygame.draw.ellipse(surf, (40, 25, 50), (lx - 1, 33 + dy, 6, 3))  # paw
        # Tail (smooth curve)
        pts = [(36, 14 + dy), (40, 10 + dy), (43, 8 + dy), (44, 6 + dy)]
        pygame.draw.lines(surf, body_c, False, pts, 3)
        pygame.draw.circle(surf, body_c, (44, 6 + dy), 2)
        frames.append(surf)
    return frames
