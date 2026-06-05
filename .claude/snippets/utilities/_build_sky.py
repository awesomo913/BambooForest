# From: engine.py:239
# Static sky gradient + clouds -- never scrolls so no tiling needed.

    def _build_sky(self) -> pygame.Surface:
        """Static sky gradient + clouds -- never scrolls so no tiling needed."""
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(120 + 80 * t)
            g = int(185 + 45 * t)
            b = int(235 + 15 * t)
            pygame.draw.line(surf, (min(255, r), min(255, g), min(255, b)),
                             (0, y), (SCREEN_WIDTH, y))
        # Clouds
        random.seed(42)
        for _ in range(5):
            cx = random.randint(80, SCREEN_WIDTH - 80)
            cy = random.randint(40, 140)
            for _ in range(6):
                pygame.draw.circle(surf, (215, 228, 242),
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-4, 8) + 3),
                                   random.randint(18, 30))
            for _ in range(8):
                pygame.draw.circle(surf, COL_WHITE,
                                   (cx + random.randint(-30, 30),
                                    cy + random.randint(-8, 5)),
                                   random.randint(18, 30))
        random.seed()
        return surf
