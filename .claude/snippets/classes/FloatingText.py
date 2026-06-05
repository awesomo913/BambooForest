# From: ui.py:76

class FloatingText:
    def __init__(self, text: str, x: float, y: float, color: tuple) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life: float = 1.0
        self.max_life: float = 1.0

    def update(self, dt: float) -> bool:
        self.y -= 60 * dt
        self.life -= dt
        return self.life > 0

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        sx, sy = camera.apply_pos(self.x, self.y)
        alpha = max(0, int(255 * (self.life / self.max_life)))
        font = get_font(22, bold=True)
        surf = font.render(self.text, True, self.color)
        alpha_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        alpha_surf.blit(surf, (0, 0))
        alpha_surf.set_alpha(alpha)
        screen.blit(alpha_surf, alpha_surf.get_rect(center=(int(sx), int(sy))))
