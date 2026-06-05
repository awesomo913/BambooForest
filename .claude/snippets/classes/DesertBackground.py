# From: backgrounds.py:356
# Warm orange sky, sand dunes, distant mesas, heat haze.

class DesertBackground(_BaseBackground):
    """Warm orange sky, sand dunes, distant mesas, heat haze."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        self._sky_gradient(surf, (255, 180, 100), (255, 230, 160))
        random.seed(42)
        # Sun
        pygame.draw.circle(surf, (255, 220, 120), (self.w // 2, 90), 50)
        pygame.draw.circle(surf, (255, 240, 160), (self.w // 2, 90), 35)
        random.seed(411)
        # Distant mesas (dark red-orange)
        for i in range(7):
            x = int(i * self.w / 5) + random.randint(-50, 50)
            mesa_h = random.randint(120, 180)
            mesa_w = random.randint(200, 350)
            top_y = SCREEN_HEIGHT - mesa_h
            c = (150 + random.randint(-15, 15),
                 85 + random.randint(-10, 10),
                 50 + random.randint(-10, 10))
            # Flat-top mesa
            for dx in (-self.w, 0, self.w):
                pygame.draw.polygon(surf, c, [
                    (x - mesa_w // 2 + dx, SCREEN_HEIGHT),
                    (x - mesa_w // 3 + dx, top_y),
                    (x + mesa_w // 3 + dx, top_y),
                    (x + mesa_w // 2 + dx, SCREEN_HEIGHT)])
            # Top stripe
            pygame.draw.line(surf, (180, 100, 60),
                             (x - mesa_w // 3, top_y),
                             (x + mesa_w // 3, top_y), 2)
        # Foreground dunes
        for i in range(5):
            x = int(i * self.w / 3) + random.randint(-60, 60)
            dune_h = random.randint(60, 120)
            dune_w = random.randint(300, 500)
            top_y = SCREEN_HEIGHT - dune_h
            c = (194 + random.randint(-10, 10), 160 + random.randint(-10, 10),
                 100 + random.randint(-10, 10))
            # Smooth rolling dune
            pts = [(x - dune_w // 2, SCREEN_HEIGHT)]
            for px_off in range(-dune_w // 2, dune_w // 2, 20):
                py = top_y + int(20 * math.sin(px_off * 0.02))
                pts.append((x + px_off, py))
            pts.append((x + dune_w // 2, SCREEN_HEIGHT))
            self._wrap_polygon(surf, c, pts)
        # Sand strip
        for y in range(SCREEN_HEIGHT - 12, SCREEN_HEIGHT):
            t = (y - (SCREEN_HEIGHT - 12)) / 12
            gc = (int(200 + 20 * t), int(170 + 15 * t), int(110 + 10 * t))
            pygame.draw.line(surf, gc, (0, y), (self.w, y))
        random.seed()
        return surf
