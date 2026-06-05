# From: web/sprites.py:1372

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        W, H = 44, 44
        base = pygame.Surface((W, H), pygame.SRCALPHA)
        cx, cy = W // 2, H // 2
        # Large bamboo leaf shape (wide oval with pointed tip)
        leaf_pts = [
            (cx, 4),               # top tip
            (cx + 18, cy - 4),     # right edge
            (cx + 14, cy + 8),     # right lower
            (cx, H - 6),           # bottom tip
            (cx - 14, cy + 8),     # left lower
            (cx - 18, cy - 4),     # left edge
        ]
        pygame.draw.polygon(base, (70, 165, 55), leaf_pts)
        # Inner lighter area
        inner_pts = [
            (cx, 8), (cx + 12, cy - 2), (cx + 8, cy + 4),
            (cx, H - 10), (cx - 8, cy + 4), (cx - 12, cy - 2),
        ]
        pygame.draw.polygon(base, (100, 195, 75), inner_pts)
        # Central vein (stem)
        pygame.draw.line(base, (50, 120, 35), (cx, 4), (cx, H - 6), 2)
        # Side veins
        for vy_off in range(-8, 12, 5):
            pygame.draw.line(base, (55, 135, 42),
                             (cx, cy + vy_off), (cx - 10, cy + vy_off + 6), 1)
            pygame.draw.line(base, (55, 135, 42),
                             (cx, cy + vy_off), (cx + 10, cy + vy_off + 6), 1)
        # Bright highlight dot (dew drop)
        pygame.draw.circle(base, (200, 255, 180), (cx + 4, cy - 6), 3)
        pygame.draw.circle(base, (255, 255, 230), (cx + 4, cy - 7), 1)
        # Small bamboo stem at bottom
        pygame.draw.rect(base, (90, 140, 55), (cx - 2, H - 8, 4, 8))
        pygame.draw.rect(base, (60, 110, 40), (cx - 3, H - 5, 6, 2))

        self._base = base
        self.image = self._base.copy()
        self.rect = self.image.get_rect(center=(x, y - 22))
        self.base_y = float(self.rect.y)
        self.glow_timer: float = 0.0
