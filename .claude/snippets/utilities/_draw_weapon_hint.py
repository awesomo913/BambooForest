# From: game.py:1296
# Persistent banner teaching the player how to attack.

    def _draw_weapon_hint(self) -> None:
        """Persistent banner teaching the player how to attack."""
        # Pulsing alpha to draw attention
        t = pygame.time.get_ticks() / 200.0
        alpha = int(180 + 55 * math.sin(t))
        font_big = pygame.font.SysFont("consolas", 22, bold=True)
        font_small = pygame.font.SysFont("consolas", 14)
        title = font_big.render("BAMBOO STAFF EQUIPPED!", True, (255, 230, 120))
        hint = font_small.render("Press  [ E ]  or  LEFT CLICK  to swing",
                                 True, (230, 230, 230))
        w = max(title.get_width(), hint.get_width()) + 32
        h = 58
        bx = (SCREEN_WIDTH - w) // 2
        by = 96
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((20, 20, 30, alpha))
        pygame.draw.rect(bg, (255, 220, 120), (0, 0, w, h), 3, border_radius=6)
        self.screen.blit(bg, (bx, by))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, by + 18)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, by + 42)))
