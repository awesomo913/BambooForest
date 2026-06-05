# From: backgrounds.py:300
# Misty gray sky, hexagonal column silhouettes, sea spray.

class BasaltBackground(_BaseBackground):
    """Misty gray sky, hexagonal column silhouettes, sea spray."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (140, 150, 160), (200, 210, 220))
        random.seed(42)
        # Fog clouds
        for _ in range(6):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(40, 200)
            for _ in range(8):
                pygame.draw.circle(surf, (180, 190, 200),
                                   (cx + random.randint(-40, 40),
                                    cy + random.randint(-10, 10)),
                                   random.randint(25, 45))
        random.seed(311)
        # Distant hex column cliffs (silhouette)
        for i in range(10):
            x = int(i * self.w / 7) + random.randint(-30, 30)
            col_h = random.randint(140, 250)
            col_w = random.randint(30, 50)
            shade = random.randint(-10, 10)
            c = (70 + shade, 80 + shade, 95 + shade)
            for dx in (-self.w, 0, self.w):
                pygame.draw.rect(surf, c,
                                 (x - col_w // 2 + dx, SCREEN_HEIGHT - col_h,
                                  col_w, col_h))
            # Hex pattern lines on top
            for ty in range(SCREEN_HEIGHT - col_h, SCREEN_HEIGHT, 24):
                pygame.draw.line(surf, (50, 60, 75),
                                 (x - col_w // 2, ty),
                                 (x + col_w // 2, ty), 1)
        # Front cliffs (darker)
        for i in range(6):
            x = int(i * self.w / 4) + random.randint(-40, 40)
            col_h = random.randint(80, 140)
            col_w = random.randint(60, 100)
            c = (45, 50, 60)
            for dx in (-self.w, 0, self.w):
                pygame.draw.rect(surf, c,
                                 (x - col_w // 2 + dx, SCREEN_HEIGHT - col_h,
                                  col_w, col_h))
        # Sea spray at very bottom
        for y in range(SCREEN_HEIGHT - 10, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 10)) / 10
            gc = (int(70 + 30 * t), int(80 + 30 * t), int(95 + 20 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf
