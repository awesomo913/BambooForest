# From: web/game.py:1162
# Draw a large bamboo leaf parasol above the panda while gliding.

    def _draw_glide_leaf(self, cam_x: int, cam_y: int) -> None:
        """Draw a large bamboo leaf parasol above the panda while gliding."""
        px = self.player.rect.centerx + cam_x
        py = self.player.rect.top + cam_y - 6
        t = pygame.time.get_ticks() / 400.0
        sway = math.sin(t) * 8
        # Leaf shape: wide ellipse with stem
        LW, LH = 52, 18
        leaf = pygame.Surface((LW, LH + 6), pygame.SRCALPHA)
        # Main leaf body
        pygame.draw.ellipse(leaf, (70, 160, 50), (0, 0, LW, LH))
        pygame.draw.ellipse(leaf, (90, 190, 65), (4, 2, LW - 8, LH - 4))
        # Central vein
        pygame.draw.line(leaf, (50, 120, 35), (LW // 2, 2), (LW // 2, LH - 2), 2)
        # Side veins
        for i in range(3):
            vx = 10 + i * 10
            pygame.draw.line(leaf, (55, 130, 40),
                             (LW // 2, 4 + i * 4), (vx, LH - 4), 1)
            pygame.draw.line(leaf, (55, 130, 40),
                             (LW // 2, 4 + i * 4), (LW - vx, LH - 4), 1)
        # Stem connecting to panda
        pygame.draw.line(leaf, (80, 130, 40),
                         (LW // 2, LH), (LW // 2, LH + 6), 2)
        # Sway rotation
        angle = sway * 0.6
        rotated = pygame.transform.rotate(leaf, angle)
        rw, rh = rotated.get_size()
        self.screen.blit(rotated, (int(px - rw // 2 + sway * 0.5),
                                   int(py - rh)))
