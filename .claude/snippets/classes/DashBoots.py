# From: sprites.py:1287
# Pickup that grants 30 seconds of dash ability.

class DashBoots(pygame.sprite.Sprite):
    """Pickup that grants 30 seconds of dash ability.

    Rendered as stylized winged boots with orange speed trails.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        W, H = 42, 42
        base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Boot sole (dark brown)
        pygame.draw.rect(base, (90, 50, 30), (6, H - 10, W - 12, 6))
        pygame.draw.rect(base, (60, 30, 15), (6, H - 4, W - 12, 2))
        # Boot body (orange-red leather)
        pygame.draw.polygon(base, (200, 80, 50), [
            (8, H - 10), (W - 8, H - 10),
            (W - 6, 20), (W - 14, 10),
            (10, 14), (6, 22),
        ])
        # Highlight
        pygame.draw.line(base, (255, 140, 90),
                         (10, 22), (W - 14, 14), 2)
        # Laces (dark X pattern)
        for i in range(3):
            y = 22 + i * 5
            pygame.draw.line(base, (40, 20, 10),
                             (12, y), (W - 12, y + 2), 1)
        # Wing detail (small feathers on the side)
        wing_col = (255, 180, 100)
        wing_pts = [(W - 4, 18), (W + 2, 10), (W + 2, 16),
                    (W + 4, 14), (W, 22)]
        pygame.draw.polygon(base, wing_col, wing_pts)
        pygame.draw.polygon(base, (255, 220, 140), wing_pts, 1)
        # Speed streak behind
        for i, a in [(0, 180), (3, 130), (6, 80)]:
            streak = pygame.Surface((10, 3), pygame.SRCALPHA)
            streak.fill((255, 200, 120, a))
            base.blit(streak, (i, H // 2))

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
            pygame.draw.circle(halo, (255, 160, 80, int(alpha * a_f)),
                              (r, r), r)
            img.blit(halo, (cx - r, cy - r),
                    special_flags=pygame.BLEND_RGBA_ADD)
        img.blit(self._base, (8, 8))
        self.image = img
