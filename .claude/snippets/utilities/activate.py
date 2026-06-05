# From: sprites.py:1901
# Activate this checkpoint. Returns True if newly activated.

    def activate(self) -> bool:
        """Activate this checkpoint. Returns True if newly activated."""
        if self.activated:
            return False
        self.activated = True
        self.image = self._img_on
        return True
