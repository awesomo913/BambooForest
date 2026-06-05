# From: sprites.py:1888
# Checkpoint signpost. Saves player progress when touched.

class Checkpoint(pygame.sprite.Sprite):
    """Checkpoint signpost. Saves player progress when touched."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._img_off = _generate_checkpoint_surface(False)
        self._img_on = _generate_checkpoint_surface(True)
        self.image = self._img_off
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.activated = False
        self.spawn_x = x
        self.spawn_y = y

    def activate(self) -> bool:
        """Activate this checkpoint. Returns True if newly activated."""
        if self.activated:
            return False
        self.activated = True
        self.image = self._img_on
        return True
