# From: sprites.py:1670
# Flying bat. NOT stompable.

class FlyingEnemy(pygame.sprite.Sprite):
    """Flying bat. NOT stompable."""
    is_stompable: bool = False

    def __init__(self, x: int, y: int, flight_range: float = 200.0) -> None:
        super().__init__()
        self._frames = _generate_flying_frames()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.flight_range = flight_range
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.time: float = random.uniform(0, 6.28)
        self.alive_flag = True
        self.anim_timer: float = 0.0

    def update(self, dt: float, platforms: pygame.sprite.Group | None = None,  # type: ignore[override]
               player: Player | None = None) -> None:
        if not self.alive_flag:
            return
        # Slower, smoother horizontal drift
        self.pos_x += ENEMY_PATROL_SPEED * 0.6 * self.direction * dt
        if abs(self.pos_x - self.origin_x) > self.flight_range:
            self.direction *= -1
        # Slower frequency for organic feel + slight horizontal wobble
        self.time += dt * FLYING_ENEMY_FREQ * 0.6 * 2 * math.pi
        self.rect.x = _fl(self.pos_x + math.sin(self.time * 0.3) * 8)
        self.rect.y = _fl(self.origin_y + math.sin(self.time) * FLYING_ENEMY_AMP)
        self.anim_timer += dt
        idx = int(self.anim_timer * 5) % 2
        frame = self._frames[idx]
        self.image = frame if self.direction > 0 else pygame.transform.flip(frame, True, False)

    def die(self) -> None:
        self.alive_flag = False
        self.kill()
