# From: biomes.py:1367
# Stationary fungus that releases drifting poison spores.

class SporePuffer(pygame.sprite.Sprite):
    """Stationary fungus that releases drifting poison spores."""

    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 32, 38
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Stalk
        pygame.draw.rect(self._base, (240, 230, 210), (W // 2 - 4, 12, 8, H - 12))
        # Cap (rounded fungus head)
        pygame.draw.ellipse(self._base, (100, 160, 100), (2, 0, W - 4, 22))
        pygame.draw.ellipse(self._base, (150, 200, 140), (6, 2, W - 12, 10))
        # Dark spots
        for dx, dy in [(W // 3, 10), (W * 2 // 3, 12), (W // 2, 6)]:
            pygame.draw.circle(self._base, (60, 90, 60), (dx, dy), 2)
        # Eyes
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 - 4, 14), 2)
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 + 4, 14), 2)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 - 4, 14), 1)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 + 4, 14), 1)
        self.image = self._base.copy()
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.puff_timer: float = random.uniform(0.5, SPORE_INTERVAL)
        self.pending_spores: list[PoisonSpore] = []
        self.alive_flag: bool = True
        self.flash: float = 0.0

    def update(self, dt: float, platforms=None, player=None) -> None:  # type: ignore[override]
        if not self.alive_flag:
            return
        self.puff_timer -= dt
        if self.flash > 0:
            self.flash -= dt
            img = self._base.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img
        else:
            self.image = self._base
        if self.puff_timer <= 0:
            self.puff_timer = SPORE_INTERVAL
            # Emit 2 spores drifting in opposite horizontal directions
            sx = self.rect.centerx
            sy = self.rect.top + 4
            self.pending_spores.append(PoisonSpore(sx, sy, -SPORE_DRIFT * 0.6))
            self.pending_spores.append(PoisonSpore(sx, sy, SPORE_DRIFT * 0.6))

    def get_new_spores(self) -> list[PoisonSpore]:
        spores = self.pending_spores
        self.pending_spores = []
        return spores

    def die(self) -> None:
        self.alive_flag = False
        self.kill()

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
