# From: game.py:1317
# Persistent banner teaching the player how to glide.

    def _draw_glide_hint(self) -> None:
        """Persistent banner teaching the player how to glide."""
        t = pygame.time.get_ticks() / 200.0
        alpha = int(180 + 55 * math.sin(t))
        font_big = pygame.font.SysFont("consolas", 22, bold=True)
        font_small = pygame.font.SysFont("consolas", 14)
        title = font_big.render("GLIDE UNLOCKED!", True, (140, 220, 255))
        hint = font_small.render(
            "Hold  [ JUMP ]  while falling to glide!", True, (230, 230, 230))
        w = max(title.get_width(), hint.get_width()) + 32
        h = 58
        bx = (SCREEN_WIDTH - w) // 2
        # Stack below weapon hint if both are showing
        by = 160 if (self.player.has_bamboo_weapon
                     and not self._weapon_used) else 96
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((15, 25, 40, alpha))
        pygame.draw.rect(bg, (140, 220, 255), (0, 0, w, h), 3, border_radius=6)
        self.screen.blit(bg, (bx, by))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, by + 18)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, by + 42)))
