# From: ui.py:502
# Pre-render the static background.

    def _ensure_bg(self) -> pygame.Surface:
        """Pre-render the static background."""
        if self._bg is not None:
            return self._bg
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Gradient
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(15 + 8 * t)
            g = int(35 + 15 * t)
            b = int(15 + 8 * t)
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        # Bamboo stalks in background
        for bx in range(30, SCREEN_WIDTH, 80):
            bh = 80 + (bx * 37) % 60
            c = (20 + (bx % 12), 50 + (bx % 18), 18)
            pygame.draw.rect(bg, c, (bx, SCREEN_HEIGHT - bh, 5, bh))
            for jy in range(SCREEN_HEIGHT - bh + 12, SCREEN_HEIGHT, 18):
                pygame.draw.rect(bg, (16, 42, 14), (bx - 1, jy, 7, 2))
            # Tiny leaf
            pygame.draw.polygon(bg, (30, 65, 25),
                                [(bx + 5, SCREEN_HEIGHT - bh + 2),
                                 (bx + 14, SCREEN_HEIGHT - bh - 4),
                                 (bx + 5, SCREEN_HEIGHT - bh - 3)])
        self._bg = bg
        return bg
