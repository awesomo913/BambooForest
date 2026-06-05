# From: backgrounds.py:798
# Industrial iron workshop. Ember glow, chains, hanging gears.

class ForgeBackground(_BaseBackground):
    """Industrial iron workshop. Ember glow, chains, hanging gears."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Dark iron gradient with ember underlight
        self._sky_gradient(surf, (60, 35, 30), (120, 70, 45))
        random.seed(1515)
        # Distant chimney smokestacks
        for i in range(4):
            cx = int(i * self.w / 3) + random.randint(-40, 40)
            c_h = random.randint(150, 230)
            c_w = random.randint(40, 60)
            base_y = SCREEN_HEIGHT - 60
            self._wrap_polygon(surf, (40, 30, 30), [
                (cx - c_w, base_y),
                (cx - c_w // 2, base_y - c_h),
                (cx + c_w // 2, base_y - c_h),
                (cx + c_w, base_y),
            ])
            # Smoke puffs
            for _ in range(2):
                sx = cx + random.randint(-15, 15)
                sy = base_y - c_h - random.randint(10, 50)
                pygame.draw.circle(surf, (80, 60, 60), (sx, sy),
                                   random.randint(10, 20))
        # Suspended chains
        random.seed(1616)
        for _ in range(14):
            chx = random.randint(20, self.w - 20)
            chl = random.randint(30, 80)
            pygame.draw.line(surf, (40, 40, 50), (chx, 0), (chx, chl), 2)
            # Tiny chain links
            for ly in range(0, chl, 6):
                pygame.draw.circle(surf, (80, 80, 90), (chx, ly), 2, 1)
        # Hanging gears
        for i in range(5):
            gx = int(i * self.w / 4) + random.randint(-30, 30)
            gy = random.randint(60, 200)
            r = random.randint(20, 35)
            pygame.draw.circle(surf, (50, 40, 40), (gx, gy), r)
            pygame.draw.circle(surf, (30, 25, 25), (gx, gy), r // 2)
            for ang in range(0, 360, 30):
                t = math.radians(ang)
                x1 = gx + int(math.cos(t) * r)
                y1 = gy + int(math.sin(t) * r)
                x2 = gx + int(math.cos(t) * (r + 5))
                y2 = gy + int(math.sin(t) * (r + 5))
                pygame.draw.line(surf, (50, 40, 40), (x1, y1), (x2, y2), 3)
        # Ember particles floating
        for _ in range(80):
            ex = random.randint(0, self.w)
            ey = random.randint(100, SCREEN_HEIGHT - 80)
            col = random.choice([(255, 140, 60), (220, 100, 40), (255, 200, 80)])
            pygame.draw.circle(surf, col, (ex, ey), 1)
        random.seed()
        return surf
