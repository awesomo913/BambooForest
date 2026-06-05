# From: biomes.py:1650
# Patrols on gates. Falls when its gate vanishes, relocates on landing.

class TidalCrab(pygame.sprite.Sprite):
    """Patrols on gates. Falls when its gate vanishes, relocates on landing."""

    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 150.0) -> None:
        super().__init__()
        W, H = 30, 22
        self._left = pygame.Surface((W, H), pygame.SRCALPHA)
        # Teal body
        pygame.draw.ellipse(self._left, (80, 140, 160), (3, 4, W - 6, H - 6))
        # Orange claws
        pygame.draw.circle(self._left, (220, 130, 60), (3, H // 2), 4)
        pygame.draw.circle(self._left, (220, 130, 60), (W - 3, H // 2), 4)
        # Eye stalks
        pygame.draw.line(self._left, (80, 140, 160),
                         (W // 2 - 3, 5), (W // 2 - 3, 1), 1)
        pygame.draw.line(self._left, (80, 140, 160),
                         (W // 2 + 3, 5), (W // 2 + 3, 1), 1)
        pygame.draw.circle(self._left, COL_BLACK, (W // 2 - 3, 1), 1)
        pygame.draw.circle(self._left, COL_BLACK, (W // 2 + 3, 1), 1)
        self._right = pygame.transform.flip(self._left, True, False)
        self.image = self._left
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self._px = float(x)
        self._py = float(y - H)
        self.vx = -TIDAL_CRAB_SPEED
        self.vy = 0.0
        self.start_x = x
        self.patrol_width = patrol_width
        self.alive_flag = True
        self.flash: float = 0.0

    def update(self, dt: float, platforms, player) -> None:  # type: ignore[override]
        if not self.alive_flag:
            return
        if self.flash > 0:
            self.flash -= dt
        # Gravity
        self.vy += GRAVITY * dt
        if self.vy > TERMINAL_VELOCITY:
            self.vy = TERMINAL_VELOCITY
        # X movement + patrol bounds
        self._px += self.vx * dt
        if self._px < self.start_x - self.patrol_width:
            self._px = self.start_x - self.patrol_width
            self.vx = abs(self.vx)
        elif self._px > self.start_x + self.patrol_width:
            self._px = self.start_x + self.patrol_width
            self.vx = -abs(self.vx)
        self.image = self._left if self.vx < 0 else self._right
        # Y movement
        self._py += self.vy * dt
        self.rect.x = int(self._px)
        self.rect.y = int(self._py)
        # Floor collision (via platforms group)
        hit = pygame.sprite.spritecollideany(self, platforms)
        if hit and self.vy > 0:
            self.rect.bottom = hit.rect.top
            self._py = float(self.rect.y)
            self.vy = 0.0
        # Fall off screen if gate vanishes
        if self.rect.top > 600:
            self._py = -40.0  # respawn up top, re-fall
            self.rect.y = int(self._py)
        if self.flash > 0:
            img = self.image.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img

    def die(self) -> None:
        self.alive_flag = False
        self.kill()

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
