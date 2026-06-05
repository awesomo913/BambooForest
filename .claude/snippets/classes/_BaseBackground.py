# From: backgrounds.py:18
# Base class: produces a seamless-tileable surface.

class _BaseBackground:
    """Base class: produces a seamless-tileable surface.

    Uses .convert() for performance on low-end hardware (Pi 1).
    Opaque parallax layer -- no per-pixel alpha lookups.
    """

    def __init__(self) -> None:
        self.w: int = SCREEN_WIDTH
        self.scroll_factor: float = 0.18
        surface = self._build()
        # Convert to display format for faster blits (Pi 1 optimization).
        # Fallback if display not initialized yet.
        try:
            self.surface: pygame.Surface = surface.convert()
        except pygame.error:
            self.surface = surface

    def _build(self) -> pygame.Surface:
        """Subclasses override to paint the biome."""
        raise NotImplementedError

    def _wrap_polygon(self, surf: pygame.Surface, color: tuple,
                     pts: list[tuple[int, int]]) -> None:
        """Draw polygon with horizontal wrap at tile edges."""
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, color, [(x - self.w, y) for x, y in pts])
        pygame.draw.polygon(surf, color, [(x + self.w, y) for x, y in pts])

    def _wrap_rect(self, surf: pygame.Surface, color: tuple,
                   rect: tuple[int, int, int, int]) -> None:
        x, y, w, h = rect
        pygame.draw.rect(surf, color, rect)
        pygame.draw.rect(surf, color, (x - self.w, y, w, h))
        pygame.draw.rect(surf, color, (x + self.w, y, w, h))

    def _sky_gradient(self, surf: pygame.Surface, top: tuple,
                      bottom: tuple) -> None:
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(surf, c, (0, y), (self.w, y))

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:
        parallax_x = camera_x * self.scroll_factor
        offset = -(parallax_x % self.w)
        draw_x = math.floor(offset)
        screen.blit(self.surface, (draw_x, 0))
        screen.blit(self.surface, (draw_x + self.w, 0))
