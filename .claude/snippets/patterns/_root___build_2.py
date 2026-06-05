# From: backgrounds.py:418

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Deep dark gradient
        self._sky_gradient(surf, (10, 12, 20), (25, 20, 35))
        random.seed(42)
        # Stalactites from ceiling
        for i in range(15):
            x = int(i * self.w / 12) + random.randint(-20, 20)
            s_h = random.randint(40, 100)
            s_w = random.randint(15, 30)
            c = (40, 35, 50)
            self._wrap_polygon(surf, c, [
                (x - s_w // 2, 0), (x + s_w // 2, 0), (x, s_h)])
        # Bioluminescent specks (tiny cyan dots)
        random.seed(77)
        for _ in range(80):
            sx = random.randint(0, self.w)
            sy = random.randint(50, SCREEN_HEIGHT - 50)
            glow_c = random.choice([(100, 220, 255), (200, 255, 180), (255, 200, 120)])
            pygame.draw.circle(surf, glow_c, (sx, sy), 1)
        # Distant stalagmites from floor
        random.seed(511)
        for i in range(12):
            x = int(i * self.w / 9) + random.randint(-30, 30)
            s_h = random.randint(60, 130)
            s_w = random.randint(25, 45)
            c = (30, 28, 40)
            self._wrap_polygon(surf, c, [
                (x - s_w // 2, SCREEN_HEIGHT),
                (x, SCREEN_HEIGHT - s_h),
                (x + s_w // 2, SCREEN_HEIGHT)])
        random.seed()
        return surf
