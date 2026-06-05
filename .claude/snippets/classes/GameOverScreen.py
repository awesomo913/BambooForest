# From: ui.py:772

class GameOverScreen:
    def __init__(self) -> None:
        self.fade_alpha: float = 0.0

    def update(self, dt: float) -> None:
        self.fade_alpha = min(200, self.fade_alpha + 300 * dt)

    def draw(self, screen: pygame.Surface, final_score: int) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(self.fade_alpha)))
        screen.blit(overlay, (0, 0))
        if self.fade_alpha > 100:
            draw_text_shadow(screen, "GAME OVER", 64, COL_RED,
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, bold=True)
            draw_text(screen, f"Score: {final_score}", 32, COL_WHITE,
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            draw_text(screen, "Press ENTER to Try Again", 24, (180, 180, 180),
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
