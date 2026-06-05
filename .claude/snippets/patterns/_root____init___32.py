# From: biomes.py:1341

    def __init__(self, x: int, y: int, drift_x: float) -> None:
        super().__init__()
        W, H = 22, 22
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Fuzzy sickly-green orb
        for r, a in [(10, 80), (7, 140), (4, 200)]:
            surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (160, 220, 120, a), (r, r), r)
            self._base.blit(surf, (W // 2 - r, H // 2 - r))
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self._px, self._py = float(x), float(y)
        self._vx = drift_x
        self._vy = -SPORE_DRIFT
        self.lifetime: float = SPORE_LIFETIME
        self.damage: int = SPORE_DAMAGE
