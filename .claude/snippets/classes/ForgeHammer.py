# From: biomes.py:2067
# Ceiling-mounted iron hammer. Periodically slams to floor.

class ForgeHammer(pygame.sprite.Sprite):
    """Ceiling-mounted iron hammer. Periodically slams to floor."""

    is_stompable: bool = False

    def __init__(self, x, y, patrol_width=0.0):
        super().__init__()
        W, H = 60, 40
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.rect(self._base, (50, 50, 60), (4, 4, W - 8, H - 8))
        pygame.draw.rect(self._base, (90, 90, 110), (6, 6, W - 12, 4))
        pygame.draw.rect(self._base, (30, 30, 40), (4, H - 8, W - 8, 4))
        pygame.draw.circle(self._base, (160, 120, 60), (W // 2, 12), 4)
        pygame.draw.circle(self._base, (220, 180, 100), (W // 2, 12), 2)
        for i, j in [(8, 8), (W - 12, 8), (8, H - 12), (W - 12, H - 12)]:
            pygame.draw.circle(self._base, (20, 20, 25), (i, j), 2)
        self.image = self._base
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.base_x = float(x)
        self._top_y = 0.0
        self._bottom_y = float(y)
        self._py = self._top_y
        self.state = "holding"
        self.timer = random.uniform(1.0, 3.0)
        self.alive_flag = True
        self.flash = 0.0

    def update(self, dt, platforms=None, player=None):
        self.timer -= dt
        if self.state == "holding":
            if self.timer <= 0:
                self.state = "telegraph"
                self.timer = 0.5
        elif self.state == "telegraph":
            if self.timer <= 0:
                self.state = "slamming"
        elif self.state == "slamming":
            self._py += 1400 * dt
            if self._py >= self._bottom_y:
                self._py = self._bottom_y
                self.state = "rising"
                self.timer = 0.3
        elif self.state == "rising":
            if self.timer <= 0:
                self._py -= 200 * dt
                if self._py <= self._top_y:
                    self._py = self._top_y
                    self.state = "holding"
                    self.timer = random.uniform(2.5, 4.0)
        self.rect.x = int(self.base_x)
        self.rect.y = int(self._py)

    def is_lethal(self):
        return self.state == "slamming"

    def die(self):
        pass

    def alive(self):
        return True
