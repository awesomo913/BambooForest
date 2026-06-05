# From: backgrounds.py:47

    def _wrap_rect(self, surf: pygame.Surface, color: tuple,
                   rect: tuple[int, int, int, int]) -> None:
        x, y, w, h = rect
        pygame.draw.rect(surf, color, rect)
        pygame.draw.rect(surf, color, (x - self.w, y, w, h))
        pygame.draw.rect(surf, color, (x + self.w, y, w, h))
