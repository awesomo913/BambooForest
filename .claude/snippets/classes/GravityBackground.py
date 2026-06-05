# From: backgrounds.py:612
# Arcane void with floating structures and pulsing veins.

class GravityBackground(_BaseBackground):
    """Arcane void with floating structures and pulsing veins."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Deep void purple-black
        self._sky_gradient(surf, (15, 5, 25), (40, 20, 60))
        random.seed(342)
        # Distant stars / energy dots
        for _ in range(100):
            sx = random.randint(0, self.w)
            sy = random.randint(0, SCREEN_HEIGHT - 30)
            col = random.choice([(200, 180, 255), (255, 220, 255),
                                 (180, 220, 255)])
            surf.set_at((sx, sy), col)
        # Floating crystal structures (geometric silhouettes)
        for i in range(5):
            cx = int(i * self.w / 4) + random.randint(-40, 40)
            cy = random.randint(100, 350)
            c_sz = random.randint(30, 60)
            col = (80, 50, 130)
            self._wrap_polygon(surf, col, [
                (cx, cy - c_sz),
                (cx + c_sz // 2, cy),
                (cx, cy + c_sz),
                (cx - c_sz // 2, cy),
            ])
            # Highlight facet
            hl_col = (140, 100, 200)
            self._wrap_polygon(surf, hl_col, [
                (cx, cy - c_sz),
                (cx + c_sz // 3, cy - c_sz // 3),
                (cx, cy),
                (cx - c_sz // 3, cy - c_sz // 3),
            ])
        # Mechanical gears (silhouettes)
        for i in range(3):
            cx = int(i * self.w / 2.5) + random.randint(-30, 30)
            cy = random.randint(80, SCREEN_HEIGHT - 100)
            r = random.randint(25, 45)
            col = (60, 40, 90)
            pygame.draw.circle(surf, col, (cx, cy), r)
            pygame.draw.circle(surf, (40, 25, 60), (cx, cy), r // 2)
            # Teeth
            for ang in range(0, 360, 30):
                t = math.radians(ang)
                x1 = cx + int(math.cos(t) * r)
                y1 = cy + int(math.sin(t) * r)
                x2 = cx + int(math.cos(t) * (r + 6))
                y2 = cy + int(math.sin(t) * (r + 6))
                pygame.draw.line(surf, col, (x1, y1), (x2, y2), 4)
        # Energy veins (glowing lines)
        for _ in range(8):
            vx = random.randint(0, self.w)
            vy_start = random.randint(0, SCREEN_HEIGHT // 2)
            vlen = random.randint(80, 180)
            pygame.draw.line(surf, (180, 120, 255),
                            (vx, vy_start), (vx + 20, vy_start + vlen), 2)
        random.seed()
        return surf
