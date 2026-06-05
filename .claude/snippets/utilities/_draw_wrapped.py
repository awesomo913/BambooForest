# From: ui.py:678
# Draw text with word wrapping + paragraph support.

    def _draw_wrapped(self, screen: pygame.Surface, text: str,
                     font: pygame.font.Font, color: tuple,
                     x: int, y: int, max_width: int) -> None:
        """Draw text with word wrapping + paragraph support."""
        for paragraph in text.split("\n\n"):
            words = paragraph.split(" ")
            line: list[str] = []
            for w in words:
                test = " ".join(line + [w])
                if font.size(test)[0] > max_width and line:
                    line_surf = font.render(" ".join(line), True, color)
                    screen.blit(line_surf, (x, y))
                    y += font.get_height() + 2
                    line = [w]
                else:
                    line.append(w)
            if line:
                line_surf = font.render(" ".join(line), True, color)
                screen.blit(line_surf, (x, y))
                y += font.get_height() + 2
            y += 8  # paragraph spacing
