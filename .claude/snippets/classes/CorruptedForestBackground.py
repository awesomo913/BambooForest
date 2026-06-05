# From: backgrounds.py:682
# Sickly forest with purple-tinted vegetation -- corruption creeping in.

class CorruptedForestBackground(_BaseBackground):
    """Sickly forest with purple-tinted vegetation -- corruption creeping in."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Overcast purple-green sky
        self._sky_gradient(surf, (130, 100, 140), (170, 160, 170))
        random.seed(202)
        # Sickly distant mountains
        for i in range(4):
            cx = int(i * self.w / 3) + random.randint(-40, 40)
            m_h = random.randint(80, 140)
            m_w = random.randint(150, 220)
            col = (70, 60, 85)
            self._wrap_polygon(surf, col, [
                (cx - m_w, SCREEN_HEIGHT - 100),
                (cx - m_w // 3, SCREEN_HEIGHT - 100 - m_h),
                (cx + m_w // 3, SCREEN_HEIGHT - 100 - m_h + 20),
                (cx + m_w, SCREEN_HEIGHT - 100),
            ])
        # Dying trees (dark twisted silhouettes)
        for i in range(10):
            tx = int(i * self.w / 8) + random.randint(-30, 30)
            trunk_h = random.randint(90, 140)
            base_y = SCREEN_HEIGHT - 60
            # Twisted trunk
            pygame.draw.line(surf, (40, 30, 40),
                           (tx, base_y), (tx + random.randint(-10, 10),
                                          base_y - trunk_h), 4)
            # Dead canopy (dark purple-green)
            pygame.draw.circle(surf, (70, 60, 80),
                             (tx + random.randint(-5, 5),
                              base_y - trunk_h - random.randint(5, 15)),
                             random.randint(20, 35))
        # Purple corruption wisps floating
        random.seed(303)
        for _ in range(40):
            wx = random.randint(0, self.w)
            wy = random.randint(50, SCREEN_HEIGHT - 80)
            col = random.choice([(180, 100, 180), (140, 70, 150),
                                 (200, 120, 200)])
            pygame.draw.circle(surf, col, (wx, wy), 2)
        # Dark twisted bamboo in the foreground
        random.seed(404)
        for i in range(15):
            bx = int(i * self.w / 14) + random.randint(-15, 15)
            by = SCREEN_HEIGHT - random.randint(40, 80)
            bh = random.randint(60, 120)
            col = (50, 60, 40)  # darker bamboo
            pygame.draw.rect(surf, col, (bx, by - bh, 5, bh))
            # Corruption spots on bamboo
            pygame.draw.circle(surf, (150, 60, 140), (bx + 2, by - bh // 2), 2)
        random.seed()
        return surf
