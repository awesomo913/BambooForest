# From: ui.py:470
# Handle mouse click. Returns True if consumed (don't start game).

    def handle_click(self, pos: tuple[int, int]) -> bool:
        """Handle mouse click. Returns True if consumed (don't start game)."""
        # If detail panel open, click anywhere closes it
        if self.selected_char is not None:
            self.selected_char = None
            return True
        # Gallery toggle button
        if (self._gallery_button_rect is not None
                and self._gallery_button_rect.collidepoint(pos)):
            self.gallery_open = not self.gallery_open
            return True
        # Click a character card -> detail popup (only if gallery is open)
        if self.gallery_open:
            for rect, char in self._card_rects:
                if rect.collidepoint(pos):
                    self.selected_char = char
                    return True
        return False
