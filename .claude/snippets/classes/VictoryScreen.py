# From: ui.py:796

class VictoryScreen:
    def __init__(self) -> None:
        self.timer: float = 0.0

    def update(self, dt: float) -> None:
        self.timer += dt

    def draw(self, screen: pygame.Surface, final_score: int,
             is_high_score: bool) -> None:
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(20 * (1 - t) + 5 * t)
            g = int(50 * (1 - t) + 20 * t)
            b = int(20 * (1 - t) + 5 * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        bounce = math.sin(self.timer * 3) * 8
        draw_text_shadow(screen, "VICTORY!", 72, COL_GOLD,
                         SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.3 + bounce), bold=True)
        draw_text(screen, f"Final Score: {final_score}", 36, COL_WHITE,
                  SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.5))
        if is_high_score:
            alpha = int(128 + 127 * math.sin(self.timer * 5))
            font = get_font(28, bold=True)
            surf = font.render("NEW HIGH SCORE!", True, COL_GOLD)
            surf.set_alpha(alpha)
            screen.blit(surf, surf.get_rect(center=(
                SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.58))))
        draw_text(screen, "Press ENTER to Play Again", 24, (180, 180, 180),
                  SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.75))
