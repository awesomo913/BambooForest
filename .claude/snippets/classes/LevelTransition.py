# From: ui.py:832

class LevelTransition:
    def __init__(self, level_number: int) -> None:
        self.level_number = level_number
        self.timer: float = 0.0
        self.duration: float = 2.0

    def update(self, dt: float) -> bool:
        self.timer += dt
        return self.timer >= self.duration

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COL_BLACK)
        t = self.timer / self.duration
        alpha = int(255 * (1 - abs(t - 0.5) * 2))
        alpha = max(0, min(255, alpha))

        font = get_font(56, bold=True)
        text = font.render(f"LEVEL {self.level_number}", True, COL_WHITE)
        text.set_alpha(alpha)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        idx = self.level_number - 1
        if 0 <= idx < len(LEVEL_NAMES):
            name_font = get_font(28)
            name = name_font.render(LEVEL_NAMES[idx], True, (180, 220, 180))
            name.set_alpha(alpha)
            screen.blit(name, name.get_rect(center=(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))
