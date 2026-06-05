# From: biomes.py:540
# Level 5. Crumbles after player stands on it, then respawns.

class CrumblingPlatform(pygame.sprite.Sprite):
    """Level 5. Crumbles after player stands on it, then respawns."""

    def __init__(self, x: int, y: int, w: int, h: int = 20,
                 platforms_group: pygame.sprite.Group | None = None) -> None:
        super().__init__()
        self.w, self.h = w, h
        self._img_solid = pygame.Surface((w, h))
        self._img_solid.fill(COL_BASALT)
        pygame.draw.rect(self._img_solid, (80, 80, 90), (0, 0, w, 4))
        self._img_crumbling = pygame.Surface((w, h), pygame.SRCALPHA)
        for bx in range(0, w, 6):
            by = random.randint(0, h - 4)
            pygame.draw.rect(self._img_crumbling, (70, 70, 80, 150), (bx, by, 5, 4))

        self.image = self._img_solid
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = True
        self.touched = False
        self.crumble_timer: float = 0.0
        self.respawn_timer: float = 0.0
        self._platforms_group = platforms_group
        self._origin = (x, y)

    def touch(self) -> None:
        if not self.touched and self.solid:
            self.touched = True
            self.crumble_timer = CRUMBLE_DELAY

    def update(self, dt: float) -> None:  # type: ignore[override]
        if self.touched and self.solid:
            self.crumble_timer -= dt
            # Flicker before crumbling
            if self.crumble_timer < 0.3 and int(self.crumble_timer * 20) % 2:
                self.image = self._img_crumbling
            else:
                self.image = self._img_solid
            if self.crumble_timer <= 0:
                self.solid = False
                self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
                self.rect = self.image.get_rect(topleft=self._origin)
                if self._platforms_group and self in self._platforms_group:
                    self._platforms_group.remove(self)
                self.respawn_timer = CRUMBLE_RESPAWN
        elif not self.solid:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.solid = True
                self.touched = False
                self.image = self._img_solid
                self.rect = self.image.get_rect(topleft=self._origin)
                if self._platforms_group and self not in self._platforms_group:
                    self._platforms_group.add(self)
