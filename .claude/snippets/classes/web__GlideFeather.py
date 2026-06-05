# From: web/sprites.py:1365
# Pickup that grants Pain-da the glide ability (hold JUMP while falling).

class GlideFeather(pygame.sprite.Sprite):
    """Pickup that grants Pain-da the glide ability (hold JUMP while falling).

    Rendered as a large bamboo leaf -- thematic parasol for a panda.
    Floats gently and pulses with a green glow.
    """

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

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.glow_timer += dt * 3.0
        self.rect.y = _fl(self.base_y + math.sin(self.glow_timer) * 4)
        alpha = int(100 + 50 * (math.sin(self.glow_timer * 1.8) + 1) * 0.5)
        W, H = self._base.get_size()
        img = pygame.Surface((W + 16, H + 16), pygame.SRCALPHA)
        cx, cy = (W + 16) // 2, (H + 16) // 2
        for r, a_f in ((24, 0.3), (18, 0.55), (12, 0.9)):
            halo = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(halo, (100, 210, 100, int(alpha * a_f)),
                              (r, r), r)
            img.blit(halo, (cx - r, cy - r),
                    special_flags=pygame.BLEND_RGBA_ADD)
        img.blit(self._base, (8, 8))
        self.image = img
