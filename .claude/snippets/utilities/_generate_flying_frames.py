# From: sprites.py:434
# Two-frame bat with spikes -- cleaner wing shape.

def _generate_flying_frames() -> list[pygame.Surface]:
    """Two-frame bat with spikes -- cleaner wing shape."""
    frames = []
    for wing_up in (True, False):
        surf = pygame.Surface((34, 28), pygame.SRCALPHA)
        body_c = (80, 30, 120)
        pygame.draw.ellipse(surf, body_c, (11, 9, 12, 14))
        if wing_up:
            pygame.draw.polygon(surf, (110, 50, 150), [(11, 14), (0, 3), (15, 11)])
            pygame.draw.polygon(surf, (110, 50, 150), [(23, 14), (34, 3), (19, 11)])
        else:
            pygame.draw.polygon(surf, (110, 50, 150), [(11, 14), (0, 21), (15, 17)])
            pygame.draw.polygon(surf, (110, 50, 150), [(23, 14), (34, 21), (19, 17)])
        # Eyes
        pygame.draw.circle(surf, (255, 50, 50), (14, 13), 2)
        pygame.draw.circle(surf, (255, 50, 50), (20, 13), 2)
        pygame.draw.circle(surf, (255, 200, 200), (14, 12), 1)
        pygame.draw.circle(surf, (255, 200, 200), (20, 12), 1)
        # Spikes
        for sx in (13, 17, 21):
            pygame.draw.polygon(surf, (200, 60, 60),
                                [(sx, 9), (sx - 2, 3), (sx + 2, 3)])
        frames.append(surf)
    return frames
