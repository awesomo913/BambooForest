# From: game.py:1366
# Full-width text box at bottom of screen for NPC dialog.

    def _draw_npc_textbox(self, npc) -> None:
        """Full-width text box at bottom of screen for NPC dialog."""
        box_h = 90
        box_y = SCREEN_HEIGHT - box_h - 8
        box_x = 20
        box_w = SCREEN_WIDTH - 40
        # Background panel with border
        bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg.fill((15, 15, 25, 230))
        pygame.draw.rect(bg, (255, 220, 120, 200), (0, 0, box_w, box_h), 3,
                         border_radius=8)
        self.screen.blit(bg, (box_x, box_y))
        # Name tab in corner
        name_font = pygame.font.SysFont("consolas", 18, bold=True)
        name_surf = name_font.render(npc.name, True, (255, 220, 120))
        name_bg = pygame.Surface((name_surf.get_width() + 20, 24), pygame.SRCALPHA)
        name_bg.fill((40, 30, 20, 240))
        pygame.draw.rect(name_bg, (255, 220, 120),
                        (0, 0, name_bg.get_width(), 24), 2, border_radius=4)
        self.screen.blit(name_bg, (box_x + 12, box_y - 12))
        self.screen.blit(name_surf, (box_x + 22, box_y - 8))
        # Dialog text (render all lines stacked)
        text_font = pygame.font.SysFont("consolas", 16)
        for i, line in enumerate(npc.dialog_lines):
            line_surf = text_font.render(line, True, (235, 235, 235))
            self.screen.blit(line_surf, (box_x + 24, box_y + 22 + i * 22))
