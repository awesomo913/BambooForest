# From: biomes.py:1129
# Level 7. Looks like light source, snaps shut as trap.

class FalseGlowworm(pygame.sprite.Sprite):
    """Level 7. Looks like light source, snaps shut as trap."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_lure = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self._img_lure, (150, 255, 100), (8, 8), 8)
        pygame.draw.circle(self._img_lure, (200, 255, 180), (8, 8), 4)
        self._img_snap = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self._img_snap, (255, 60, 40), (8, 8), 8)
        pygame.draw.circle(self._img_snap, (255, 120, 100), (8, 8), 4)
        self.image = self._img_lure
        self.rect = self.image.get_rect(center=(x, y))
        self.state = "luring"
        self.state_timer: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if player is None:
            return
        dist = math.hypot(player.rect.centerx - self.rect.centerx,
                          player.rect.centery - self.rect.centery)
        if self.state == "luring":
            self.image = self._img_lure
            if dist < GLOWWORM_SNAP_RANGE:
                self.state = "snapping"
                self.state_timer = 0.5
        elif self.state == "snapping":
            self.image = self._img_snap
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "cooldown"
                self.state_timer = 3.0
        elif self.state == "cooldown":
            self.image = self._img_lure
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "luring"

    def die(self) -> None:
        pass  # invincible
