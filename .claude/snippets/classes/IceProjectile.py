# From: sprites.py:1224
# Ice spell projectile. Travels in a straight line, pierces enemies,

class IceProjectile(pygame.sprite.Sprite):
    """Ice spell projectile. Travels in a straight line, pierces enemies,
    explodes at max range or on wall contact. Leaves a freeze particle trail.
    """

    def __init__(self, x: int, y: int, direction: float) -> None:
        super().__init__()
        self._base = self._make_shard()
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vx = 800.0 * direction  # faster than shuriken
        self.vy = 0.0  # travels straight (no gravity)
        self.rotation: float = 0.0
        self.lifetime: float = 1.5  # ~1200px travel range
        self.damage: int = 999  # instant-kill vs non-boss enemies
        # Trail buffer
        self._trail: list[tuple[float, float]] = []

    @staticmethod
    def _make_shard() -> pygame.Surface:
        """Glowing cyan-white diamond-shaped ice shard."""
        W, H = 36, 20
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        # Outer glow halo (concentric ellipses)
        for r_scale, alpha in [(1.0, 60), (0.8, 120), (0.6, 180)]:
            w2, h2 = int(W * r_scale), int(H * r_scale)
            ox, oy = (W - w2) // 2, (H - h2) // 2
            pygame.draw.ellipse(surf, (140, 220, 255, alpha),
                                (ox, oy, w2, h2))
        # Core ice shard (diamond shape)
        pts = [(2, H // 2), (W // 2, 3), (W - 3, H // 2),
               (W // 2, H - 3)]
        pygame.draw.polygon(surf, (200, 240, 255), pts)
        # Inner highlight
        pts2 = [(6, H // 2), (W // 2, 6), (W - 7, H // 2), (W // 2, H - 6)]
        pygame.draw.polygon(surf, (255, 255, 255), pts2)
        # Tip sparkles
        pygame.draw.circle(surf, (255, 255, 255), (W - 3, H // 2), 2)
        pygame.draw.circle(surf, (255, 255, 255), (2, H // 2), 2)
        return surf

    def update(self, dt: float) -> None:  # type: ignore[override]
        # Store trail point (for drawing)
        self._trail.append((self.pos_x, self.pos_y))
        if len(self._trail) > 8:
            self._trail.pop(0)
        self.pos_x += self.vx * dt
        self.pos_y += self.vy * dt
        # Flip image horizontally based on direction
        if self.direction < 0:
            self.image = pygame.transform.flip(self._base, True, False)
        else:
            self.image = self._base
        self.rect = self.image.get_rect(center=(_fl(self.pos_x),
                                                _fl(self.pos_y)))
        self.lifetime -= dt
        if self.lifetime <= 0 or self.pos_x < -50 or self.pos_x > 8000:
            self.kill()
