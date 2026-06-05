# From: biomes.py:2133

class VoidEater(pygame.sprite.Sprite):
    is_stompable: bool = False

    def __init__(self, x, y, patrol_width=0.0):
        super().__init__()
        self._base = self._make_surf(False)
        self._open = self._make_surf(True)
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self.base_x, self.base_y = float(x), float(y)
        self.alive_flag = True
        self.flash = 0.0
        self._pulse = 0.0
        self.open_timer = random.uniform(1.5, 3.0)
        self.state = "closed"

    @staticmethod
    def _make_surf(open_mouth):
        W, H = 36, 36
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        for r, a in [(16, 120), (14, 180), (12, 230)]:
            pygame.draw.circle(surf, (20, 5, 40, a), (W // 2, H // 2), r)
        pygame.draw.circle(surf, (140, 60, 180), (W // 2, H // 2), 16, 2)
        if open_mouth:
            pygame.draw.circle(surf, COL_BLACK, (W // 2, H // 2), 10)
            for ang in range(0, 360, 45):
                t = math.radians(ang)
                tx = int(W // 2 + math.cos(t) * 10)
                ty = int(H // 2 + math.sin(t) * 10)
                pygame.draw.circle(surf, (220, 220, 255), (tx, ty), 2)
        else:
            pygame.draw.line(surf, (80, 20, 100),
                           (W // 2 - 6, H // 2), (W // 2 + 6, H // 2), 2)
        pygame.draw.circle(surf, (220, 100, 255),
                         (W // 2 - 4, H // 2 - 4), 2)
        return surf

    def update(self, dt, platforms=None, player=None):
        if not self.alive_flag:
            return
        if self.flash > 0:
            self.flash -= dt
        self._pulse += dt * 2.0
        self.open_timer -= dt
        if self.open_timer <= 0:
            if self.state == "closed":
                self.state = "open"
                self.open_timer = 1.0
                self.image = self._open
            else:
                self.state = "closed"
                self.open_timer = random.uniform(2.0, 3.5)
                self.image = self._base
        self.rect.x = int(self.base_x)
        self.rect.y = int(self.base_y + math.sin(self._pulse) * 8)
        if self.flash > 0:
            img = self.image.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img

    def is_dangerous(self):
        return self.state == "open"

    def die(self):
        self.alive_flag = False
        self.kill()

    def alive(self):
        return self.alive_flag
