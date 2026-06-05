# From: game.py:147
# Toggle fullscreen using pygame.display.toggle_fullscreen().

    def _toggle_fullscreen(self) -> None:
        """Toggle fullscreen using pygame.display.toggle_fullscreen().

        This only works because the window was initialised with pygame.SCALED
        flag. Preserves the same Surface reference -- no set_mode reinit.
        """
        try:
            pygame.display.toggle_fullscreen()
            self._fullscreen = not self._fullscreen
        except pygame.error:
            # Fallback: explicit set_mode reinit
            self._fullscreen = not self._fullscreen
            flags = pygame.SCALED | pygame.DOUBLEBUF
            if self._fullscreen:
                flags |= pygame.FULLSCREEN
            try:
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)
            except pygame.error:
                self._fullscreen = False
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
