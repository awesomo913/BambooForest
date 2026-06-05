# From: biomes.py:1291
# Always-active bounce pad. Player landing on it gets launched upward.

class MushroomSpring(pygame.sprite.Sprite):
    """Always-active bounce pad. Player landing on it gets launched upward."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._base = self._make_surf(False)
        self._compressed = self._make_surf(True)
        self.image = self._base
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.compress_timer: float = 0.0

    @staticmethod
    def _make_surf(compressed: bool) -> pygame.Surface:
        W, H = 56, 32 if not compressed else 20
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        # Short stalk (white) at the bottom
        stalk_h = 6 if not compressed else 3
        pygame.draw.rect(surf, (230, 220, 210),
                         (W // 2 - 4, H - stalk_h, 8, stalk_h))
        # Cap (magenta with yellow spots)
        cap_h = H - stalk_h
        pygame.draw.ellipse(surf, (180, 60, 160), (0, 0, W, cap_h))
        # Highlight on top
        pygame.draw.ellipse(surf, (230, 130, 200),
                            (6, 2, W - 12, cap_h // 2))
        # Yellow spots
        for dx, dy in [(W // 4, cap_h // 2), (W * 3 // 4, cap_h // 2),
                       (W // 2, cap_h // 4)]:
            pygame.draw.circle(surf, (255, 240, 130), (dx, dy), 3)
            pygame.draw.circle(surf, (255, 255, 200), (dx - 1, dy - 1), 1)
        return surf

    def compress(self) -> None:
        self.compress_timer = MUSHROOM_COMPRESS_SEC
        self.image = self._compressed
        # Adjust rect so bottom stays in place when image shrinks
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self, dt: float) -> None:  # type: ignore[override]
        if self.compress_timer > 0:
            self.compress_timer -= dt
            if self.compress_timer <= 0:
                old_midbottom = self.rect.midbottom
                self.image = self._base
                self.rect = self.image.get_rect(midbottom=old_midbottom)
