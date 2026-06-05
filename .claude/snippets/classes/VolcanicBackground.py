# From: backgrounds.py:231
# Red-orange sky, dark volcanic peaks, lava glow, ash particles.

class VolcanicBackground(_BaseBackground):
    """Red-orange sky, dark volcanic peaks, lava glow, ash particles."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (120, 40, 30), (220, 100, 40))
        random.seed(42)
        # Ash clouds (dark red-gray)
        for _ in range(6):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(30, 160)
            for _ in range(7):
                pygame.draw.circle(surf, (100, 50, 40),
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-8, 8) + 3),
                                   random.randint(20, 35))
            for _ in range(5):
                pygame.draw.circle(surf, (60, 30, 25),
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-8, 6)),
                                   random.randint(20, 32))
        random.seed(211)
        # Dark volcanic mountains (almost black)
        for i in range(8):
            x = int(i * self.w / 6) + random.randint(-50, 50)
            peak_h = random.randint(220, 320)
            base_w = random.randint(280, 450)
            top_y = SCREEN_HEIGHT - peak_h
            self._wrap_polygon(surf, (40, 25, 30),
                               [(x - base_w // 2, SCREEN_HEIGHT),
                                (x, top_y),
                                (x + base_w // 2, SCREEN_HEIGHT)])
            # Lava crack
            crack_c = (220, 80, 30)
            pygame.draw.line(surf, crack_c,
                             (x - base_w // 8, SCREEN_HEIGHT - 30),
                             (x, top_y + 40), 2)
            pygame.draw.line(surf, (255, 140, 50),
                             (x - base_w // 8, SCREEN_HEIGHT - 30),
                             (x, top_y + 40), 1)
            # Smoke wisp from peak
            for sy_off in range(0, 40, 5):
                pygame.draw.circle(surf, (80, 50, 45),
                                   (x + random.randint(-5, 5),
                                    top_y - sy_off),
                                   3)
        # Front smaller peaks
        for i in range(6):
            x = int(i * self.w / 5) + random.randint(-40, 40)
            peak_h = random.randint(110, 180)
            base_w = random.randint(220, 360)
            top_y = SCREEN_HEIGHT - peak_h
            self._wrap_polygon(surf, (30, 20, 25),
                               [(x - base_w // 2, SCREEN_HEIGHT),
                                (x, top_y),
                                (x + base_w // 2, SCREEN_HEIGHT)])
        # Lava glow at base
        for y in range(SCREEN_HEIGHT - 20, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 20)) / 20
            gc = (int(180 + 60 * t), int(60 + 40 * t), int(20 + 10 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf
