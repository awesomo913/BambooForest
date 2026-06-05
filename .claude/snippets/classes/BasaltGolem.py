# From: biomes.py:869
# Level 5. Disguised pillar that lunges when close.

class BasaltGolem(pygame.sprite.Sprite):
    """Level 5. Disguised pillar that lunges when close."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_dormant = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.rect(self._img_dormant, COL_BASALT, (0, 0, 30, 50), border_radius=3)
        self._img_active = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.rect(self._img_active, (90, 80, 80), (0, 0, 30, 50), border_radius=3)
        pygame.draw.circle(self._img_active, (255, 80, 40), (10, 15), 4)
        pygame.draw.circle(self._img_active, (255, 80, 40), (20, 15), 4)
        self.image = self._img_dormant
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.state = "dormant"
        self.state_timer: float = 0.0
        self.strike_dir: float = 0.0
        self.origin_x = float(x)
        self.velocity_y: float = 0.0
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag or player is None:
            return
        # Gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0

        dist = abs(player.rect.centerx - self.rect.centerx)
        if self.state == "dormant":
            self.image = self._img_dormant
            if dist < GOLEM_STRIKE_RANGE:
                self.state = "telegraph"
                self.state_timer = 0.3
                self.strike_dir = 1.0 if player.rect.centerx > self.rect.centerx else -1.0
        elif self.state == "telegraph":
            self.image = self._img_active
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "striking"
                self.state_timer = 0.4
        elif self.state == "striking":
            self.image = self._img_active
            self.rect.x += _fl(GOLEM_STRIKE_SPEED * self.strike_dir * dt)
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "cooldown"
                self.state_timer = GOLEM_COOLDOWN
        elif self.state == "cooldown":
            self.image = self._img_dormant
            # Return to origin
            dx = self.origin_x - self.rect.x
            if abs(dx) > 2:
                self.rect.x += _fl(dx * 2 * dt)
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "dormant"

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
