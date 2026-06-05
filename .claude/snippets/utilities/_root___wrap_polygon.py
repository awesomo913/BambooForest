# From: engine.py:267
# Draw a polygon that wraps seamlessly at x=0 and x=self.w.

    def _wrap_polygon(self, surf: pygame.Surface, color: tuple,
                      pts: list[tuple[int, int]]) -> None:
        """Draw a polygon that wraps seamlessly at x=0 and x=self.w."""
        pygame.draw.polygon(surf, color, pts)
        # Also draw shifted copies so edges wrap cleanly
        shifted_left = [(x - self.w, y) for x, y in pts]
        shifted_right = [(x + self.w, y) for x, y in pts]
        pygame.draw.polygon(surf, color, shifted_left)
        pygame.draw.polygon(surf, color, shifted_right)
