# From: sprites.py:1349
# Pickup that grants Pain-da the glide ability (hold JUMP while falling).

class GlideFeather(pygame.sprite.Sprite):
    """Pickup that grants Pain-da the glide ability (hold JUMP while falling).

    Rendered as a glowing cyan-white feather with sparkle halo.
    Floats gently and pulses to attract attention.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        W, H = 40, 44
        base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Feather quill (central spine)
        spine_col = (180, 230, 255)
        pygame.draw.line(base, spine_col, (W // 2, H - 4), (W // 2 - 2, 6), 2)
        # Left barbs (cyan-white gradient)
        barb_cols = [(140, 210, 255), (100, 190, 240), (160, 225, 255)]
        for i, frac in enumerate([0.2, 0.35, 0.5, 0.65, 0.8]):
            sy = int(H * (1.0 - frac))
            col = barb_cols[i % len(barb_cols)]
            # Left barb
            pygame.draw.line(base, col,
                             (W // 2 - 1, sy), (W // 2 - 14 + i, sy - 4), 2)
            # Right barb
            pygame.draw.line(base, col,
                             (W // 2 + 1, sy), (W // 2 + 14 - i, sy - 4), 2)
        # Feather tip (bright white)
        pygame.draw.circle(base, (255, 255, 255), (W // 2 - 2, 6), 3)
        # Small wing silhouette overlay
        wing_pts = [
            (W // 2 - 12, H // 2 + 2),
            (W // 2, H // 2 - 10),
            (W // 2 + 12, H // 2 + 2),
            (W // 2, H // 2 + 6),
        ]
        pygame.draw.polygon(base, (200, 240, 255, 140), wing_pts)
        pygame.draw.polygon(base, (255, 255, 255, 80), wing_pts, 1)

        self._base = base
        self.image = self._base.copy()
        self.rect = self.image.get_rect(center=(x, y - 22))
        self.base_y = float(self.rect.y)
        self.glow_timer: float = 0.0

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.glow_timer += dt * 3.0
        # Gentle float
        self.rect.y = _fl(self.base_y + math.sin(self.glow_timer) * 4)
        # Pulsing cyan halo
        alpha = int(100 + 50 * (math.sin(self.glow_timer * 1.8) + 1) * 0.5)
        W, H = self._base.get_size()
        img = pygame.Surface((W + 16, H + 16), pygame.SRCALPHA)
        cx, cy = (W + 16) // 2, (H + 16) // 2
        for r, a_f in ((24, 0.3), (18, 0.55), (12, 0.9)):
            halo = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(halo, (140, 220, 255, int(alpha * a_f)),
                              (r, r), r)
            img.blit(halo, (cx - r, cy - r),
                    special_flags=pygame.BLEND_RGBA_ADD)
        img.blit(self._base, (8, 8))
        self.image = img
