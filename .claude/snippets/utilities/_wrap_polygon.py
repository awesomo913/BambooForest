# From: backgrounds.py:40
# Draw polygon with horizontal wrap at tile edges.

    def _wrap_polygon(self, surf: pygame.Surface, color: tuple,
                     pts: list[tuple[int, int]]) -> None:
        """Draw polygon with horizontal wrap at tile edges."""
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, color, [(x - self.w, y) for x, y in pts])
        pygame.draw.polygon(surf, color, [(x + self.w, y) for x, y in pts])
