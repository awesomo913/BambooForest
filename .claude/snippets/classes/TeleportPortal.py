# From: biomes.py:1737
# Linked portal. Entering transports player to partner's position.

class TeleportPortal(pygame.sprite.Sprite):
    """Linked portal. Entering transports player to partner's position."""

    def __init__(self, x: int, y: int, pair_id: int) -> None:
        super().__init__()
        self.pair_id = pair_id
        self.color = _PORTAL_PAIR_COLORS[pair_id % len(_PORTAL_PAIR_COLORS)]
        self.partner: TeleportPortal | None = None
        self.active: bool = True
        self.cooldown: float = 0.0
        self._rot: float = 0.0
        self._w, self._h = 44, 64
        self.rect = pygame.Rect(0, 0, self._w, self._h)
        self.rect.midbottom = (x, y)
        self.image = self._make_surf()

    def _make_surf(self) -> pygame.Surface:
        W, H = self._w, self._h
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        alpha_scale = 1.0 if self.active else 0.4
        cr, cg, cb = self.color
        # Outer glowing ring
        for r, a_f in ((1.0, 80), (0.8, 140), (0.6, 200)):
            w2 = int(W * r)
            h2 = int(H * r)
            ox = (W - w2) // 2
            oy = (H - h2) // 2
            alpha = int(a_f * alpha_scale)
            pygame.draw.ellipse(surf, (cr, cg, cb, alpha),
                                (ox, oy, w2, h2), 2)
        # Swirl lines
        cx, cy = W // 2, H // 2
        for i in range(4):
            angle = self._rot + i * math.pi / 2
            x1 = cx + int(math.cos(angle) * W * 0.25)
            y1 = cy + int(math.sin(angle) * H * 0.25)
            x2 = cx + int(math.cos(angle) * W * 0.4)
            y2 = cy + int(math.sin(angle) * H * 0.4)
            pygame.draw.line(surf, (cr, cg, cb, int(220 * alpha_scale)),
                             (x1, y1), (x2, y2), 2)
        # Core
        pygame.draw.circle(surf, (255, 255, 255, int(200 * alpha_scale)),
                          (cx, cy), 5)
        return surf

    def teleport(self) -> None:
        self.active = False
        self.cooldown = PORTAL_COOLDOWN_SEC

    def update(self, dt: float) -> None:  # type: ignore[override]
        self._rot += dt * 3.0
        if self.cooldown > 0:
            self.cooldown -= dt
            if self.cooldown <= 0:
                self.active = True
        self.image = self._make_surf()
