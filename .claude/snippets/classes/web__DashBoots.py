# From: web/sprites.py:1303
# Pickup that grants 30 seconds of dash ability.

class DashBoots(pygame.sprite.Sprite):
    """Pickup that grants 30 seconds of dash ability.

    Rendered as a coiled bamboo spring scroll -- stored wind energy.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        W, H = 42, 42
        base = pygame.Surface((W, H), pygame.SRCALPHA)
        cx, cy = W // 2, H // 2
        # Bamboo scroll tube (horizontal cylinder)
        pygame.draw.rect(base, (110, 170, 70), (6, cy - 8, W - 12, 16),
                         border_radius=6)
        pygame.draw.rect(base, (140, 200, 90), (8, cy - 6, W - 16, 12),
                         border_radius=4)
        # Bamboo joints on the scroll tube
        for jx in (12, W // 2, W - 12):
            pygame.draw.line(base, (70, 130, 45), (jx, cy - 8), (jx, cy + 8), 2)
        # End caps (darker knots)
        pygame.draw.circle(base, (80, 130, 50), (8, cy), 6)
        pygame.draw.circle(base, (100, 155, 65), (8, cy), 4)
        pygame.draw.circle(base, (80, 130, 50), (W - 8, cy), 6)
        pygame.draw.circle(base, (100, 155, 65), (W - 8, cy), 4)
        # Wind swirl lines (green energy)
        for i, (sx, sy) in enumerate([(cx - 6, 6), (cx + 4, 8), (cx - 2, 4)]):
            arc_r = 8 + i * 3
            pygame.draw.arc(base, (130, 220, 100),
                           (sx - arc_r, sy, arc_r * 2, arc_r), 0.5, 2.5, 2)
        # Wind swirl below
        for i, (sx, sy) in enumerate([(cx + 6, H - 12), (cx - 4, H - 14)]):
            arc_r = 6 + i * 3
            pygame.draw.arc(base, (130, 220, 100),
                           (sx - arc_r, sy, arc_r * 2, arc_r), 3.5, 5.5, 2)
        # Small leaf accent
        pygame.draw.polygon(base, (85, 170, 55),
                            [(cx + 8, cy - 10), (cx + 16, cy - 16),
                             (cx + 14, cy - 8)])

        self._base = base
        self.image = self._base.copy()
        self.rect = self.image.get_rect(center=(x, y - 22))
        self.base_y = float(self.rect.y)
        self.glow_timer: float = 0.0

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.glow_timer += dt * 3.0
        self.rect.y = _fl(self.base_y + math.sin(self.glow_timer) * 4)
        alpha = int(100 + 50 * (math.sin(self.glow_timer * 1.5) + 1) * 0.5)
        W, H = self._base.get_size()
        img = pygame.Surface((W + 16, H + 16), pygame.SRCALPHA)
        cx, cy = (W + 16) // 2, (H + 16) // 2
        for r, a_f in ((24, 0.3), (18, 0.55), (12, 0.9)):
            halo = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(halo, (120, 210, 100, int(alpha * a_f)),
                              (r, r), r)
            img.blit(halo, (cx - r, cy - r),
                    special_flags=pygame.BLEND_RGBA_ADD)
        img.blit(self._base, (8, 8))
        self.image = img
