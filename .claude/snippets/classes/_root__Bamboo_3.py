# From: sprites.py:1146
# Collectible bamboo with pulsing golden glow aura (affordance).

class Bamboo(pygame.sprite.Sprite):
    """Collectible bamboo with pulsing golden glow aura (affordance)."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_image = generate_bamboo_surface()
        # Pre-render a composite with a glow halo around the stalk
        w, h = self.base_image.get_size()
        self._composite = pygame.Surface((w + 12, h + 12), pygame.SRCALPHA)
        self._stalk_offset = (6, 6)
        self.image = self._composite.copy()
        # Blit stalk on top
        self.image.blit(self.base_image, self._stalk_offset)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.base_y = float(self.rect.y)
        self.bob_timer: float = random.uniform(0, 6.28)
        self.glow_timer: float = random.uniform(0, 6.28)

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.bob_timer += dt * 2
        self.glow_timer += dt * 3
        self.rect.y = _fl(self.base_y + math.sin(self.bob_timer) * 1.5)
        # Pulsing golden glow
        alpha = int(60 + 60 * (math.sin(self.glow_timer) + 1) * 0.5)
        w, h = self._composite.get_size()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        # Soft glow circles (layered for halo effect)
        cx, cy = w // 2, h // 2
        for r, a_frac in ((16, 0.4), (12, 0.6), (8, 1.0)):
            glow = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 230, 120, int(alpha * a_frac)),
                              (r, r), r)
            self.image.blit(glow, (cx - r, cy - r),
                          special_flags=pygame.BLEND_RGBA_ADD)
        self.image.blit(self.base_image, self._stalk_offset)
