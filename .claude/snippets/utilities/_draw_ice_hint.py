# From: game.py:1339
# Persistent banner teaching the player how to cast ice.

    def _draw_ice_hint(self) -> None:
        """Persistent banner teaching the player how to cast ice."""
        t = pygame.time.get_ticks() / 200.0
        alpha = int(180 + 55 * math.sin(t))
        font_big = pygame.font.SysFont("consolas", 22, bold=True)
        font_small = pygame.font.SysFont("consolas", 14)
        title = font_big.render("ICE MAGIC UNLOCKED!", True, (140, 220, 255))
        hint = font_small.render(
            "Press  [ R ]  to cast Ice Shard  (10s cooldown)",
            True, (230, 230, 230))
        w = max(title.get_width(), hint.get_width()) + 32
        h = 58
        bx = (SCREEN_WIDTH - w) // 2
        # Stack below other hints if showing
        offset = 0
        if self.player.has_bamboo_weapon and not self._weapon_used:
            offset += 64
        if self.player.has_glide and not self._glide_used:
            offset += 64
        by = 96 + offset
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((15, 25, 40, alpha))
        pygame.draw.rect(bg, (140, 220, 255), (0, 0, w, h), 3, border_radius=6)
        self.screen.blit(bg, (bx, by))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, by + 18)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, by + 42)))
