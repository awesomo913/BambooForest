# From: biomes.py:515
# Level 4. Damage zone left by SulfurSlime.

class ToxicTrail(pygame.sprite.Sprite):
    """Level 4. Damage zone left by SulfurSlime."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((22, 8), pygame.SRCALPHA)
        # Goo puddle with bubbles
        pygame.draw.ellipse(self.image, (100, 160, 40), (0, 2, 22, 6))
        pygame.draw.ellipse(self.image, (160, 220, 60), (2, 3, 18, 3))
        # Bubbles
        pygame.draw.circle(self.image, (220, 255, 120), (6, 3), 1)
        pygame.draw.circle(self.image, (220, 255, 120), (14, 4), 1)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.lifetime: float = SULFUR_TRAIL_LIFE

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.lifetime -= dt
        # Fade as it ages
        if self.lifetime < 1.0:
            alpha = int(255 * self.lifetime)
            self.image.set_alpha(alpha)
        if self.lifetime <= 0:
            self.kill()
