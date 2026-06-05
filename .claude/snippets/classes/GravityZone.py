# From: biomes.py:1871
# Rectangular zone that alters player gravity while inside.

class GravityZone(pygame.sprite.Sprite):
    """Rectangular zone that alters player gravity while inside.

    Types: 'low' (0.3x), 'high' (2.0x), 'reverse' (-1.0x).
    """

    def __init__(self, x: int, y: int, w: int, h: int, gravity_type: str) -> None:
        super().__init__()
        self.gravity_type = gravity_type
        self.rect = pygame.Rect(x, y, w, h)
        self.image = self._make_surf(w, h, gravity_type)
        self._wave_timer: float = 0.0

    @staticmethod
    def _make_surf(w: int, h: int, gtype: str) -> pygame.Surface:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        if gtype == "low":
            # Pale blue with upward lines
            surf.fill((100, 180, 255, 30))
            pygame.draw.rect(surf, (140, 220, 255, 120), (0, 0, w, h), 2)
            for i in range(0, w, 20):
                pygame.draw.line(surf, (160, 230, 255, 80),
                                 (i + 10, h), (i + 10, h - 20), 2)
                # Arrow up
                pygame.draw.line(surf, (160, 230, 255, 120),
                                 (i + 10, h - 20), (i + 6, h - 16), 2)
                pygame.draw.line(surf, (160, 230, 255, 120),
                                 (i + 10, h - 20), (i + 14, h - 16), 2)
        elif gtype == "reverse":
            # Purple with inverted arrows
            surf.fill((180, 100, 220, 40))
            pygame.draw.rect(surf, (220, 140, 255, 140), (0, 0, w, h), 2)
            for i in range(0, w, 30):
                # Arrow pointing UP (player falls up)
                pygame.draw.line(surf, (220, 140, 255, 120),
                                 (i + 15, h - 10), (i + 15, 10), 2)
                pygame.draw.line(surf, (220, 140, 255, 140),
                                 (i + 15, 10), (i + 10, 18), 2)
                pygame.draw.line(surf, (220, 140, 255, 140),
                                 (i + 15, 10), (i + 20, 18), 2)
        else:  # high
            # Dark red with downward lines
            surf.fill((180, 40, 40, 35))
            pygame.draw.rect(surf, (220, 70, 70, 130), (0, 0, w, h), 2)
            for i in range(0, w, 20):
                pygame.draw.line(surf, (255, 100, 80, 120),
                                 (i + 10, 0), (i + 10, 20), 3)
                pygame.draw.line(surf, (255, 100, 80, 140),
                                 (i + 10, 20), (i + 6, 16), 2)
                pygame.draw.line(surf, (255, 100, 80, 140),
                                 (i + 10, 20), (i + 14, 16), 2)
        return surf

    def get_multiplier(self) -> float:
        if self.gravity_type == "low":
            return GRAVITY_LOW_MULT
        if self.gravity_type == "high":
            return GRAVITY_HIGH_MULT
        return GRAVITY_REVERSE_MULT

    def update(self, dt: float) -> None:  # type: ignore[override]
        # Static zone; no state to update
        pass
