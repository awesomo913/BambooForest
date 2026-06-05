# From: biomes.py:543

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
