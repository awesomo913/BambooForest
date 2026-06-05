# From: biomes.py:1174
# Level 8. Static crystal that grows when player stands still nearby.

class BrineShard(pygame.sprite.Sprite):
    """Level 8. Static crystal that grows when player stands still nearby."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_size = 16
        self.size_scale: float = 1.0
        self._regen_image()
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.base_y = y
        self.alive_flag = True

    def _regen_image(self) -> None:
        sz = max(8, int(self.base_size * self.size_scale))
        self.image = pygame.Surface((sz, sz * 2), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, COL_SALT,
                            [(sz // 2, 0), (sz, sz * 2), (0, sz * 2)])
        pygame.draw.polygon(self.image, COL_ICE,
                            [(sz // 2, sz // 2), (sz - 2, sz * 2), (2, sz * 2)])

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if player is None:
            return
        dist = math.hypot(player.rect.centerx - self.rect.centerx,
                          player.rect.centery - self.rect.centery)
        player_still = abs(player.velocity_x) < 10
        if dist < BRINE_DMG_RADIUS * 2 and player_still:
            self.size_scale = min(3.0, self.size_scale + BRINE_GROW_RATE * dt)
        else:
            self.size_scale = max(1.0, self.size_scale - BRINE_GROW_RATE * 0.5 * dt)
        old_center = self.rect.center
        self._regen_image()
        self.rect = self.image.get_rect(center=old_center)

    def die(self) -> None:
        pass
