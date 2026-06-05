# From: biomes.py:763
# Level 4. Swoops when player is mid-air.

class AshBat(pygame.sprite.Sprite):
    """Level 4. Swoops when player is mid-air."""
    is_stompable: bool = True

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((34, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (80, 60, 60), (10, 8, 14, 16))
        pygame.draw.polygon(self.image, (100, 70, 70), [(10, 14), (0, 4), (14, 10)])
        pygame.draw.polygon(self.image, (100, 70, 70), [(24, 14), (34, 4), (20, 10)])
        pygame.draw.circle(self.image, (255, 120, 40), (14, 13), 2)
        pygame.draw.circle(self.image, (255, 120, 40), (20, 13), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.state = "hover"
        self.swoop_tx: float = 0.0
        self.swoop_ty: float = 0.0
        self.alive_flag = True
        self.hover_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        if not self.alive_flag or player is None:
            return
        if self.state == "hover":
            self.hover_timer += dt
            self.rect.y = _fl(self.origin_y + math.sin(self.hover_timer * 3) * 8)
            dist = math.hypot(player.rect.centerx - self.rect.centerx,
                              player.rect.centery - self.rect.centery)
            if not player.is_on_ground and dist < ASH_BAT_RANGE:
                self.state = "swoop"
                self.swoop_tx = float(player.rect.centerx)
                self.swoop_ty = float(player.rect.centery)
        elif self.state == "swoop":
            dx = self.swoop_tx - self.rect.centerx
            dy = self.swoop_ty - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 5:
                self.rect.x += _fl(dx / dist * ASH_BAT_SWOOP * dt)
                self.rect.y += _fl(dy / dist * ASH_BAT_SWOOP * dt)
            else:
                self.state = "return"
        elif self.state == "return":
            dx = self.origin_x - self.rect.centerx
            dy = self.origin_y - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 5:
                self.rect.x += _fl(dx / dist * ASH_BAT_SWOOP * 0.5 * dt)
                self.rect.y += _fl(dy / dist * ASH_BAT_SWOOP * 0.5 * dt)
            else:
                self.state = "hover"

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
