# From: ui.py:705
# Pause screen with compact enemy encyclopedia (read while waiting).

class PauseOverlay:
    """Pause screen with compact enemy encyclopedia (read while waiting)."""

    def draw(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        draw_text_shadow(screen, "PAUSED", 42, COL_WHITE,
                         SCREEN_WIDTH // 2, 36, bold=True)
        draw_text(screen, "ESC to Resume  |  Q to Quit", 16, (180, 180, 180),
                  SCREEN_WIDTH // 2, 62)

        # Mini enemy encyclopedia -- compact grid of all characters
        sprites = _get_sprite_cache()
        col_w = 180
        row_h = 90
        cols = 5
        start_x = (SCREEN_WIDTH - cols * col_w) // 2
        start_y = 90
        font_name = get_font(12, bold=True)
        font_desc = get_font(10)
        for i, char in enumerate(_CHARACTERS):
            col = i % cols
            row = i // cols
            x = start_x + col * col_w
            y = start_y + row * row_h
            # Compact card
            card = pygame.Surface((col_w - 8, row_h - 8), pygame.SRCALPHA)
            card.fill((15, 25, 15, 230))
            pygame.draw.rect(card, (*char["color"], 160),
                             (0, 0, col_w - 8, row_h - 8), 1, border_radius=4)
            screen.blit(card, (x, y))
            # Small sprite
            sprite = sprites.get(char["key"])
            if sprite:
                sm = pygame.transform.scale(sprite, (40, 40))
                screen.blit(sm, (x + 8, y + 10))
            # Name + desc
            name = font_name.render(char["name"], True, char["color"])
            screen.blit(name, (x + 56, y + 8))
            role = font_desc.render(char["role"], True, (160, 200, 160))
            screen.blit(role, (x + 56, y + 22))
            # Word-wrap description
            desc = char["desc"]
            max_chars = 22
            if len(desc) > max_chars:
                # Split on word
                words = desc.split()
                line1, line2 = "", ""
                for w in words:
                    if len(line1) + len(w) + 1 <= max_chars:
                        line1 = line1 + " " + w if line1 else w
                    else:
                        line2 = line2 + " " + w if line2 else w
                d1 = font_desc.render(line1, True, (200, 200, 200))
                d2 = font_desc.render(line2, True, (200, 200, 200))
                screen.blit(d1, (x + 56, y + 40))
                screen.blit(d2, (x + 56, y + 54))
            else:
                d = font_desc.render(desc, True, (200, 200, 200))
                screen.blit(d, (x + 56, y + 46))
