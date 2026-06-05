# From: biomes.py:1988
# Ghostly flier that always tracks the player. Stompable.

class HomingSpecter(pygame.sprite.Sprite):
    """Ghostly flier that always tracks the player. Stompable.

    Accelerates when player is airborne/gliding -- designed to punish
    air-cheese strategies.
    """

    is_stompable: bool = True

    def __init__(self, x: int, y: int, patrol_width: float = 0.0) -> None:
        super().__init__()
        W, H = 34, 28
        self._base = pygame.Surface((W, H), pygame.SRCALPHA)
        body_pts = [(W // 2, 2), (W - 2, H // 2),
                    (W - 6, H - 2), (W // 2, H - 6),
                    (6, H - 2), (2, H // 2)]
        pygame.draw.polygon(self._base, (180, 100, 200, 180), body_pts)
        pygame.draw.polygon(self._base, (230, 160, 255, 220), body_pts, 2)
        pygame.draw.circle(self._base, (255, 80, 80),
                          (W // 2 - 5, H // 2), 3)
        pygame.draw.circle(self._base, (255, 80, 80),
                          (W // 2 + 5, H // 2), 3)
        pygame.draw.circle(self._base, COL_WHITE,
                          (W // 2 - 5, H // 2 - 1), 1)
        pygame.draw.circle(self._base, COL_WHITE,
                          (W // 2 + 5, H // 2 - 1), 1)
        self.image = self._base
        self.rect = self.image.get_rect(center=(x, y))
        self._px, self._py = float(x), float(y)
        self._vx, self._vy = 0.0, 0.0
        self.alive_flag = True
        self.flash: float = 0.0
        self._base_speed = 90.0
        self._chase_speed = 180.0

    def update(self, dt, platforms=None, player=None):
        if not self.alive_flag:
            return
        if self.flash > 0:
            self.flash -= dt
        if player is not None:
            target = self._base_speed
            if not player.is_on_ground:
                target = self._chase_speed
            if getattr(player, 'is_gliding', False):
                target = self._chase_speed * 1.3
            dx = player.rect.centerx - self._px
            dy = player.rect.centery - self._py
            dist = math.hypot(dx, dy)
            if dist > 5:
                self._vx = (dx / dist) * target
                self._vy = (dy / dist) * target
            else:
                self._vx = self._vy = 0
        self._px += self._vx * dt
        self._py += self._vy * dt
        # Compute bob offset and apply in ONE rect.center assignment so the
        # collision rect always matches the final drawn position.
        bob = int(math.sin(pygame.time.get_ticks() / 180.0) * 2)
        self.rect.center = (int(self._px), int(self._py) + bob)
        if self.flash > 0:
            img = self._base.copy()
            img.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = img
        else:
            self.image = self._base

    def die(self):
        self.alive_flag = False
        self.kill()

    def alive(self):
        return self.alive_flag
