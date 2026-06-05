# From: biomes.py:1432
# Lethal lava floor that rises steadily from below.

class RisingLava(pygame.sprite.Sprite):
    """Lethal lava floor that rises steadily from below.

    Pauses at configured Y values for a breathing period, then resumes.
    """

    def __init__(self, world_width: int, pause_ys: list[int] | None = None) -> None:
        super().__init__()
        self.world_width = world_width
        self.pause_ys = sorted(pause_ys or [], reverse=False)  # ascending (top-most first after sort)
        # Actually we want highest-y first (deepest), then pause higher as we rise
        # pause_ys are Y values where lava pauses. Lower Y = higher on screen.
        # So after rising past y=450 (pause #1), next is y=400, then y=350.
        self.pause_ys = sorted(pause_ys or [], reverse=True)  # e.g. [450, 400, 350]
        self._next_pause_idx: int = 0
        self.current_y: float = float(LAVA_START_Y)  # starts below screen
        self.paused: bool = False
        self.pause_timer: float = 0.0
        self._base = self._make_surf()
        self.image = self._base
        self.rect = self.image.get_rect(topleft=(0, int(self.current_y)))
        self._wave_timer: float = 0.0

    def _make_surf(self) -> pygame.Surface:
        W, H = self.world_width, 260
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        # Molten body gradient
        for y in range(H):
            t = y / H
            r = int(240 - 40 * t)
            g = int(90 - 70 * t)
            b = int(20 - 15 * t)
            pygame.draw.line(surf, (max(0, r), max(0, g), max(0, b)),
                             (0, y), (W, y))
        # Bright crust at top
        pygame.draw.rect(surf, (255, 220, 100), (0, 0, W, 4))
        pygame.draw.rect(surf, (255, 255, 180), (0, 0, W, 1))
        # Bubble specks
        for _ in range(W // 40):
            bx = random.randint(10, W - 10)
            by = random.randint(6, H - 4)
            pygame.draw.circle(surf, (255, 200, 80), (bx, by), 2)
        return surf

    def update(self, dt: float) -> None:  # type: ignore[override]
        self._wave_timer += dt
        if self.paused:
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self.paused = False
        else:
            self.current_y -= LAVA_RISE_SPEED * dt  # y decreases as lava rises
            # Check pause points
            if self._next_pause_idx < len(self.pause_ys):
                target = self.pause_ys[self._next_pause_idx]
                if self.current_y <= target:
                    self.current_y = float(target)
                    self.paused = True
                    self.pause_timer = LAVA_PAUSE_SEC
                    self._next_pause_idx += 1
        # Subtle wave offset on y
        wave_y = int(self.current_y) + int(math.sin(self._wave_timer * 3) * 2)
        self.rect.y = wave_y
