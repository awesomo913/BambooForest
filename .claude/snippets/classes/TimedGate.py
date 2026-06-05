# From: biomes.py:1572
# Platform that cycles between solid and intangible.

class TimedGate(pygame.sprite.Sprite):
    """Platform that cycles between solid and intangible.

    Gates in group A are solid while group B is intangible, then swap.
    Added/removed from platforms_group automatically.
    """

    # Shared class-level clock so all gates stay in sync
    _global_timer: float = 0.0

    def __init__(self, x: int, y: int, w: int, h: int,
                 group_id: str, platforms_group: pygame.sprite.Group) -> None:
        super().__init__()
        self.group_id = group_id  # "A" or "B"
        self._platforms_group = platforms_group
        self.rect = pygame.Rect(x, y, w, h)
        self._solid_img = self._make_surf(w, h, lit=True)
        self._intangible_img = self._make_surf(w, h, lit=False)
        self.solid: bool = (group_id == "A")  # A starts solid, B starts intangible
        self.image = self._solid_img if self.solid else self._intangible_img
        if self.solid:
            platforms_group.add(self)
        self._flicker: float = 0.0

    @staticmethod
    def _make_surf(w: int, h: int, lit: bool) -> pygame.Surface:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        if lit:
            # Solid stone with glowing cyan runes
            pygame.draw.rect(surf, (80, 100, 130), (0, 0, w, h))
            pygame.draw.rect(surf, (140, 180, 220), (0, 0, w, 3))
            pygame.draw.rect(surf, (60, 80, 110), (0, h - 3, w, 3))
            # Cyan rune dots
            for i in range(w // 24):
                rx = 12 + i * 24
                if rx < w - 6:
                    pygame.draw.circle(surf, (80, 220, 255),
                                      (rx, h // 2), 3)
        else:
            # Ghostly outline
            pygame.draw.rect(surf, (80, 100, 130, 60), (0, 0, w, h))
            pygame.draw.rect(surf, (140, 180, 220, 120), (0, 0, w, h), 2)
            for i in range(w // 24):
                rx = 12 + i * 24
                if rx < w - 6:
                    pygame.draw.circle(surf, (80, 180, 220, 80),
                                      (rx, h // 2), 3, 1)
        return surf

    @classmethod
    def tick_global(cls, dt: float) -> None:
        cls._global_timer += dt
        if cls._global_timer >= GATE_CYCLE_SEC:
            cls._global_timer = 0.0

    def update(self, dt: float) -> None:  # type: ignore[override]
        # Flicker during telegraph phase
        in_phase_a = TimedGate._global_timer < (GATE_CYCLE_SEC * 0.5)
        time_until_swap = (GATE_CYCLE_SEC * 0.5) - (
            TimedGate._global_timer % (GATE_CYCLE_SEC * 0.5))
        flickering = time_until_swap < GATE_TELEGRAPH_SEC

        should_be_solid = (self.group_id == "A") == in_phase_a
        if should_be_solid and not self.solid:
            self.solid = True
            self._platforms_group.add(self)
        elif not should_be_solid and self.solid:
            self.solid = False
            self._platforms_group.remove(self)
        # Choose image with flicker
        if flickering and self.solid:
            # Alternate between solid and intangible at 10Hz
            t = pygame.time.get_ticks()
            self.image = self._solid_img if (t // 100) % 2 == 0 else self._intangible_img
        else:
            self.image = self._solid_img if self.solid else self._intangible_img
