# From: sprites.py:1510

class HealingItem(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_image = generate_heal_surface()
        self.image = self.base_image
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.pulse_timer: float = random.uniform(0, 6.28)

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.pulse_timer += dt * 4
        scale = 1.0 + 0.1 * math.sin(self.pulse_timer)
        w = int(25 * scale)
        h = int(25 * scale)
        cx, cy = self.rect.center
        self.image = pygame.transform.scale(self.base_image, (w, h))
        self.rect = self.image.get_rect(center=(cx, cy))
