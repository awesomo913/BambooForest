# From: backgrounds.py:507

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Deep purple / midnight gradient
        self._sky_gradient(surf, (30, 15, 50), (60, 30, 80))
        random.seed(142)
        # Giant background mushrooms (silhouettes with soft glow)
        for i in range(6):
            cx = int(i * self.w / 5) + random.randint(-30, 30)
            stalk_h = random.randint(140, 220)
            cap_r = random.randint(60, 100)
            base_y = SCREEN_HEIGHT - 10
            # Stalk (pale)
            stalk_col = (120, 110, 140)
            pygame.draw.rect(surf, stalk_col,
                            (cx - 8, base_y - stalk_h, 16, stalk_h))
            # Cap (glowing magenta)
            cap_col = (120, 50, 130)
            self._wrap_polygon(surf, cap_col, [
                (cx - cap_r, base_y - stalk_h),
                (cx, base_y - stalk_h - cap_r // 2),
                (cx + cap_r, base_y - stalk_h),
            ])
            # Bright highlight on top of cap
            hl_col = (200, 100, 220)
            pygame.draw.ellipse(surf, hl_col,
                              (cx - cap_r // 2, base_y - stalk_h - cap_r // 3,
                               cap_r, cap_r // 4))
            # Yellow spots
            for _ in range(3):
                sx = cx + random.randint(-cap_r // 2, cap_r // 2)
                sy = base_y - stalk_h - random.randint(5, cap_r // 3)
                pygame.draw.circle(surf, (255, 240, 150), (sx, sy), 5)
        # Drifting spores (small glowing dots)
        random.seed(271)
        for _ in range(120):
            sx = random.randint(0, self.w)
            sy = random.randint(0, SCREEN_HEIGHT - 40)
            col = random.choice([(220, 130, 220), (130, 230, 180),
                                 (220, 230, 130)])
            r = random.choice([1, 1, 2])
            pygame.draw.circle(surf, col, (sx, sy), r)
        random.seed()
        return surf
