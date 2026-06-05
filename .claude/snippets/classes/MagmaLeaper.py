# From: biomes.py:1497
# Fiery creature that leaps out of the lava in arcs.

class MagmaLeaper(pygame.sprite.Sprite):
    """Fiery creature that leaps out of the lava in arcs."""

    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 30, 30
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.ellipse(self._base, (220, 80, 30), (0, 0, W, H))
        pygame.draw.ellipse(self._base, (255, 150, 50), (4, 2, W - 8, H - 8))
        pygame.draw.circle(self._base, (255, 240, 120), (W // 2, H // 2), 6)
        # Fiery eyes
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 - 5, H // 2 - 2), 2)
        pygame.draw.circle(self._base, COL_WHITE, (W // 2 + 5, H // 2 - 2), 2)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 - 5, H // 2 - 2), 1)
        pygame.draw.circle(self._base, COL_BLACK, (W // 2 + 5, H // 2 - 2), 1)
        self.image = self._base
        # Spawn far below, then leap periodically
        self.start_x = float(x)
        self.start_y = float(y)
        self.rect = self.image.get_rect(center=(x, y + 200))  # submerged
        self._px, self._py = self.start_x, self.start_y + 200
        self._vy = 0.0
        self.state = "submerged"  # submerged / leaping / falling
        self.leap_timer: float = random.uniform(1.0, LEAPER_INTERVAL)
        self.alive_flag = True
        self.flash: float = 0.0

    def update(self, dt: float, platforms=None, player=None) -> None:  # type: ignore[override]
        if not self.alive_flag:
            return
        if self.flash > 0:
            self.flash -= dt
        if self.state == "submerged":
            self.leap_timer -= dt
            if self.leap_timer <= 0:
                self.state = "leaping"
                self._vy = LEAPER_JUMP
                # Leap from current x position; slightly track toward player
                if player is not None:
                    dx = player.rect.centerx - self._px
                    self._px += max(-100, min(100, dx * 0.3))
                self._py = self.start_y
        elif self.state in ("leaping", "falling"):
            self._vy += GRAVITY * dt
            self._py += self._vy * dt
            if self._vy > 0:
                self.state = "falling"
            if self._py > self.start_y + 200:
                # Back under
                self.state = "submerged"
                self.leap_timer = LEAPER_INTERVAL
                self._py = self.start_y + 200
        self.rect.center = (int(self._px), int(self._py))
        # Flash on hit
        if self.flash > 0:
            img = self._base.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img
        else:
            self.image = self._base

    def die(self) -> None:
        self.alive_flag = False
        self.kill()

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
