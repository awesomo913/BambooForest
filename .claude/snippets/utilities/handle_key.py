# From: ui.py:489
# Returns True if the key was consumed (don't start game).

    def handle_key(self, key: int) -> bool:
        """Returns True if the key was consumed (don't start game)."""
        if self.selected_char is not None:
            if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN):
                self.selected_char = None
                return True
            return True  # any key closes
        # ESC closes the gallery (lets you see the clean title again)
        if self.gallery_open and key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.gallery_open = False
            return True
        return False
