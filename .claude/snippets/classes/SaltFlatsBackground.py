# From: backgrounds.py:457
# Pale sky, snowy Andes silhouettes, mirror-flat salt surface.

class SaltFlatsBackground(_BaseBackground):
    """Pale sky, snowy Andes silhouettes, mirror-flat salt surface."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (180, 220, 250), (220, 240, 255))
        random.seed(42)
        # Wispy high clouds
        for _ in range(4):
            cx = random.randint(80, self.w - 80)
            cy = random.randint(30, 100)
            for _ in range(5):
                pygame.draw.ellipse(surf, (240, 245, 255),
                                    (cx + random.randint(-40, 40),
                                     cy + random.randint(-5, 5),
                                     60, 10))
        # Distant snowy Andes
        random.seed(611)
        for i in range(9):
            x = int(i * self.w / 6) + random.randint(-50, 50)
            peak_h = random.randint(150, 240)
            base_w = random.randint(200, 350)
            top_y = SCREEN_HEIGHT - peak_h - 20
            # Base (purple-gray)
            c = (120, 130, 150)
            self._wrap_polygon(surf, c, [
                (x - base_w // 2, SCREEN_HEIGHT - 20),
                (x, top_y),
                (x + base_w // 2, SCREEN_HEIGHT - 20)])
            # Snow cap (large, takes upper half)
            sw = base_w // 2
            self._wrap_polygon(surf, (245, 248, 255), [
                (x - sw // 2, top_y + 40), (x, top_y),
                (x + sw // 2, top_y + 40)])
        # Reflective salt surface (horizon band)
        for y in range(SCREEN_HEIGHT - 20, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 20)) / 20
            gc = (int(220 + 10 * t), int(230 + 10 * t), int(245 + 10 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf
