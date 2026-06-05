# From: biomes.py:1795
# Patrols and teleports through nearby active portals.

class PhaseWraith(pygame.sprite.Sprite):
    """Patrols and teleports through nearby active portals."""

    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 150.0) -> None:
        super().__init__()
        W, H = 30, 40
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Ghostly translucent body
        body_pts = [(W // 2, 2), (W - 4, H // 2), (W - 6, H - 4),
                    (W // 2, H - 6), (6, H - 4), (4, H // 2)]
        pygame.draw.polygon(self._base, (180, 140, 220, 160), body_pts)
        pygame.draw.polygon(self._base, (220, 180, 255, 200), body_pts, 2)
        # Glowing eyes
        pygame.draw.circle(self._base, (255, 200, 255),
                          (W // 2 - 5, H // 2 - 2), 3)
        pygame.draw.circle(self._base, (255, 200, 255),
                          (W // 2 + 5, H // 2 - 2), 3)
        pygame.draw.circle(self._base, COL_BLACK,
                          (W // 2 - 5, H // 2 - 2), 1)
        pygame.draw.circle(self._base, COL_BLACK,
                          (W // 2 + 5, H // 2 - 2), 1)
        self.image = self._base
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self._px = float(x)
        self._py = float(y - H)
        self.vx = -WRAITH_SPEED
        self.start_x = x
        self.patrol_width = patrol_width
        self.alive_flag = True
        self.flash: float = 0.0
        self.teleport_cooldown: float = 0.0

    def update(self, dt: float, platforms, player) -> None:  # type: ignore[override]
        if not self.alive_flag:
            return
        if self.flash > 0:
            self.flash -= dt
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= dt
        self._px += self.vx * dt
        if self._px < self.start_x - self.patrol_width:
            self._px = self.start_x - self.patrol_width
            self.vx = abs(self.vx)
        elif self._px > self.start_x + self.patrol_width:
            self._px = self.start_x + self.patrol_width
            self.vx = -abs(self.vx)
        self.rect.x = int(self._px)
        self.rect.y = int(self._py)
        # Subtle float
        self._py += math.sin(pygame.time.get_ticks() / 200.0) * 0.3
        if self.flash > 0:
            img = self._base.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img
        else:
            self.image = self._base

    def teleport_to(self, x: int, y: int) -> None:
        self._px = float(x)
        self._py = float(y - self.rect.height)
        self.teleport_cooldown = 2.0

    def die(self) -> None:
        self.alive_flag = False
        self.kill()

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
