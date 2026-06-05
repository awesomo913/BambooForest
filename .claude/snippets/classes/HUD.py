# From: ui.py:105

class HUD:
    def __init__(self) -> None:
        self.displayed_hp: float = 100.0
        self.floating_texts: list[FloatingText] = []
        self.combo_display_timer: float = 0.0
        self.combo_scale: float = 1.0
        self.total_bamboos: int = 0
        self.collected_bamboos: int = 0
        self.lives: int = 3

    def set_bamboo_count(self, total: int) -> None:
        self.total_bamboos = total
        self.collected_bamboos = 0

    def on_bamboo_collected(self) -> None:
        self.collected_bamboos += 1

    def update(self, dt: float, player: Player) -> None:
        diff = player.health - self.displayed_hp
        self.displayed_hp += diff * min(1.0, 6 * dt)
        if self.combo_display_timer > 0:
            self.combo_display_timer -= dt
        self.combo_scale = max(1.0, self.combo_scale - 2 * dt)
        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]

    def draw(self, screen: pygame.Surface, player: Player,
             level_num: int, camera: Camera) -> None:
        # HUD backing (tall if mana bar visible)
        hud_h = 100 if player.has_ice_magic else 85
        hud_surf = pygame.Surface((260, hud_h), pygame.SRCALPHA)
        hud_surf.fill((*COL_HUD_BG, 190))
        pygame.draw.rect(hud_surf, (60, 60, 60, 100),
                        (0, 0, 260, hud_h), 2, border_radius=8)
        screen.blit(hud_surf, (8, 8))

        # HP label + bar
        draw_text(screen, "HP", 18, COL_WHITE, 30, 28)
        pygame.draw.rect(screen, COL_HP_RED, (48, 20, 150, 14), border_radius=4)
        fill_w = max(0, int(self.displayed_hp * 1.5))
        if fill_w > 0:
            pygame.draw.rect(screen, COL_HP_GREEN, (48, 20, fill_w, 14), border_radius=4)
        # HP text
        draw_text(screen, f"{int(self.displayed_hp)}", 14, COL_WHITE, 123, 28)

        # Mana bar (only shown if player has ice magic unlocked)
        if player.has_ice_magic:
            draw_text(screen, "MP", 14, COL_WHITE, 30, 44)
            # Background
            pygame.draw.rect(screen, (40, 40, 70), (48, 40, 150, 10),
                            border_radius=3)
            mana_w = max(0, int(player.mana * 1.5))
            if mana_w > 0:
                # Cyan gradient
                col = (80, 180, 240) if player.mana >= player.mana_max else (60, 140, 200)
                pygame.draw.rect(screen, col, (48, 40, mana_w, 10),
                                border_radius=3)
                # Bright edge highlight
                pygame.draw.rect(screen, (180, 230, 255),
                                (48, 40, mana_w, 2), border_radius=2)
            # "READY" indicator when full
            if player.mana >= player.mana_max:
                t = pygame.time.get_ticks() / 200.0
                pulse = 0.7 + 0.3 * math.sin(t)
                pygame.draw.circle(screen,
                                  (int(255 * pulse), 255, int(255 * pulse)),
                                  (207, 45), 3)

        # Score (shift down if mana bar visible)
        score_y = 65 if player.has_ice_magic else 50
        draw_text(screen, f"SCORE: {player.score}", 20, COL_GOLD, 138, score_y, bold=True)

        # Bamboo counter with checkmark icons
        bx = 22
        by = 80 if player.has_ice_magic else 65
        for i in range(min(self.total_bamboos, 12)):
            checked = i < self.collected_bamboos
            _draw_bamboo_icon(screen, bx + i * 14, by, checked)
        if self.total_bamboos > 12:
            draw_text(screen, f"{self.collected_bamboos}/{self.total_bamboos}",
                      14, COL_BAMBOO, bx + 12 * 14 + 20, by + 8)
        else:
            draw_text(screen, f"{self.collected_bamboos}/{self.total_bamboos}",
                      14, (150, 220, 150), bx + self.total_bamboos * 14 + 15, by + 8)

        # Level indicator
        draw_text_shadow(screen, f"LEVEL {level_num}", 20, COL_WHITE,
                         SCREEN_WIDTH - 60, 25)

        # Lives display (panda head icons)
        lives_x = SCREEN_WIDTH - 100
        lives_y = 45
        draw_text(screen, "LIVES:", 14, (180, 180, 180), lives_x - 5, lives_y)
        for li in range(self.lives):
            lx = lives_x + 28 + li * 20
            pygame.draw.circle(screen, (240, 240, 235), (lx, lives_y), 7)
            pygame.draw.circle(screen, (30, 30, 30), (lx - 2, lives_y - 1), 2)
            pygame.draw.circle(screen, (30, 30, 30), (lx + 2, lives_y - 1), 2)

        # Power-up indicators (below lives) -- show countdown timers
        pwr_y = lives_y + 18
        pwr_x = SCREEN_WIDTH - 100
        if player.glide_time_remaining > 0:
            gt = int(player.glide_time_remaining)
            col = (140, 220, 255) if gt > 3 else (255, 100, 100)
            # Cyan feather icon
            pygame.draw.polygon(screen, col, [
                (pwr_x, pwr_y), (pwr_x + 4, pwr_y - 10),
                (pwr_x + 8, pwr_y)])
            draw_text(screen, f"GLIDE {gt}s", 11, col, pwr_x + 14, pwr_y - 2)
            pwr_x += 75
        if player.dash_time_remaining > 0:
            dt_ = int(player.dash_time_remaining)
            col = (255, 180, 100) if dt_ > 5 else (255, 100, 100)
            draw_text(screen, f"DASH {dt_}s", 11, col, pwr_x, pwr_y - 2)
            pwr_x += 60
        if player.has_bamboo_weapon:
            wt = int(player.weapon_time_remaining)
            col = (255, 230, 120) if wt > 10 else (255, 100, 80)
            draw_text(screen, f"SWORD {wt}s", 11, col, pwr_x, pwr_y - 2)

        # Combo counter
        if player.combo_count > 1:
            sz = int(28 * self.combo_scale)
            draw_text_shadow(screen, f"x{player.combo_count}!", sz, COL_GOLD,
                             SCREEN_WIDTH // 2, 30, bold=True)

        # Persistent controls hint at bottom-right (always visible during play)
        hint_font = get_font(11)
        hint = hint_font.render(
            "ESC pause  |  F11 fullscreen", True, (150, 170, 150))
        screen.blit(hint, (SCREEN_WIDTH - hint.get_width() - 8,
                           SCREEN_HEIGHT - 16))

        # Floating texts
        for ft in self.floating_texts:
            ft.draw(screen, camera)

    def add_floating_text(self, text: str, x: float, y: float,
                          color: tuple = COL_GOLD) -> None:
        self.floating_texts.append(FloatingText(text, x, y, color))
        self.combo_display_timer = 1.0
        self.combo_scale = 1.5
