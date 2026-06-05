# From: backgrounds.py:559

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Stormy gray-blue gradient
        self._sky_gradient(surf, (70, 90, 110), (120, 140, 160))
        random.seed(242)
        # Distant rain / mist streaks
        for _ in range(50):
            sx = random.randint(0, self.w)
            sy = random.randint(0, 200)
            pygame.draw.line(surf, (180, 200, 220, 100),
                            (sx, sy), (sx - 2, sy + 8), 1)
        # Coastal rocks (dark silhouettes)
        for i in range(5):
            cx = int(i * self.w / 4) + random.randint(-40, 40)
            r_w = random.randint(60, 110)
            r_h = random.randint(40, 90)
            base_y = SCREEN_HEIGHT - 30
            col = (50, 70, 85)
            self._wrap_polygon(surf, col, [
                (cx - r_w, base_y),
                (cx - r_w // 2, base_y - r_h),
                (cx, base_y - r_h + 10),
                (cx + r_w // 2, base_y - r_h),
                (cx + r_w, base_y),
            ])
        # Lighthouse (centered ish)
        lh_x = self.w // 2 + 80
        lh_base_y = SCREEN_HEIGHT - 80
        # Tower (red/white bands)
        pygame.draw.rect(surf, (220, 220, 210),
                        (lh_x - 10, lh_base_y - 80, 20, 80))
        pygame.draw.rect(surf, (180, 50, 50),
                        (lh_x - 10, lh_base_y - 65, 20, 10))
        pygame.draw.rect(surf, (180, 50, 50),
                        (lh_x - 10, lh_base_y - 35, 20, 10))
        # Lantern room
        pygame.draw.rect(surf, (50, 50, 60),
                        (lh_x - 8, lh_base_y - 95, 16, 15))
        # Light beam
        pygame.draw.circle(surf, (255, 230, 120), (lh_x, lh_base_y - 88), 5)
        # Crashing wave foam near the bottom
        for _ in range(40):
            sx = random.randint(0, self.w)
            sy = SCREEN_HEIGHT - random.randint(5, 25)
            pygame.draw.circle(surf, (220, 230, 240), (sx, sy), 2)
        random.seed()
        return surf
