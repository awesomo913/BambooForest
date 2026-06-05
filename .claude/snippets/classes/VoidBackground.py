# From: backgrounds.py:861
# Ethereal purple void. Floating stone islands, drifting souls.

class VoidBackground(_BaseBackground):
    """Ethereal purple void. Floating stone islands, drifting souls."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Deep purple void gradient
        self._sky_gradient(surf, (25, 10, 50), (75, 35, 110))
        random.seed(1717)
        # Distant nebula swirls
        for _ in range(6):
            cx = random.randint(50, self.w - 50)
            cy = random.randint(30, 200)
            cr = random.randint(50, 100)
            col = random.choice([(140, 80, 180), (100, 60, 160), (180, 100, 220)])
            for r, a in [(cr, 30), (cr - 10, 50), (cr - 20, 80)]:
                cloud = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(cloud, (*col, a), (r, r), r)
                surf.blit(cloud, (cx - r, cy - r))
        # Floating stone islands
        random.seed(1818)
        for i in range(5):
            ix = int(i * self.w / 4) + random.randint(-40, 40)
            iy = random.randint(80, 280)
            iw = random.randint(60, 100)
            self._wrap_polygon(surf, (80, 60, 120), [
                (ix - iw, iy),
                (ix - iw // 2, iy - 15),
                (ix + iw // 2, iy - 12),
                (ix + iw, iy),
                (ix + iw // 3, iy + 18),
                (ix - iw // 3, iy + 15),
            ])
            # Highlight on top
            pygame.draw.line(surf, (140, 100, 180),
                             (ix - iw + 5, iy - 2),
                             (ix + iw - 5, iy - 2), 2)
        # Drifting soul orbs (translucent circles)
        random.seed(1919)
        for _ in range(50):
            ox = random.randint(0, self.w)
            oy = random.randint(0, SCREEN_HEIGHT - 60)
            col = random.choice([(220, 180, 255), (180, 140, 230)])
            pygame.draw.circle(surf, col, (ox, oy), 2)
            pygame.draw.circle(surf, (*col, 100), (ox, oy), 4)
        # Rippling ether streaks
        for _ in range(20):
            sx = random.randint(0, self.w)
            sy = random.randint(200, SCREEN_HEIGHT - 80)
            slen = random.randint(20, 60)
            pygame.draw.line(surf, (180, 140, 230),
                             (sx, sy), (sx + slen, sy - 8), 1)
        random.seed()
        return surf
