# From: web/game.py:1193
# Draw speed afterimages behind the panda while dashing.

    def _draw_dash_trail(self, cam_x: int, cam_y: int) -> None:
        """Draw speed afterimages behind the panda while dashing."""
        if not self.player.image:
            return
        direction = self.player.dash_direction
        for i in range(3):
            offset_x = int(-direction * (16 + i * 14))
            alpha = 120 - i * 40
            ghost = self.player.image.copy()
            # Tint green for bamboo-chi feel
            tint = pygame.Surface(ghost.get_size(), pygame.SRCALPHA)
            tint.fill((80, 200, 80, alpha))
            ghost.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            gx = self.player.rect.x + cam_x + offset_x
            gy = self.player.rect.y + cam_y
            self.screen.blit(ghost, (gx, gy))
        # Speed lines
        for i in range(4):
            import random as _r
            ly = self.player.rect.centery + cam_y + _r.randint(-12, 12)
            lx = self.player.rect.centerx + cam_x - int(direction * 20)
            llen = _r.randint(10, 25)
            streak = pygame.Surface((llen, 2), pygame.SRCALPHA)
            streak.fill((180, 255, 140, 140))
            self.screen.blit(streak, (lx - int(direction * llen), ly))
