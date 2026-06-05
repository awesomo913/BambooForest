# From: backgrounds.py:742
# Dark red-purple lair. Throbbing corruption, boss epicenter.

class MutantLairBackground(_BaseBackground):
    """Dark red-purple lair. Throbbing corruption, boss epicenter."""

    def _build(self) -> pygame.Surface:
        surf = pygame.Surface((self.w, SCREEN_HEIGHT))
        # Blood-purple sky gradient
        self._sky_gradient(surf, (60, 20, 45), (120, 40, 70))
        random.seed(1111)
        # Throbbing corruption clouds
        for _ in range(8):
            cx = random.randint(50, self.w - 50)
            cy = random.randint(30, 180)
            cr = random.randint(40, 80)
            col = (110, 40, 100)
            for r, a in [(cr, 40), (cr - 10, 60), (cr - 20, 90)]:
                cloud = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(cloud, (*col, a), (r, r), r)
                surf.blit(cloud, (cx - r, cy - r))
        # Twisted black spires (from ground, dead trees/corruption)
        for i in range(8):
            tx = int(i * self.w / 6) + random.randint(-40, 40)
            spire_h = random.randint(130, 220)
            base_y = SCREEN_HEIGHT - 60
            col = (20, 10, 25)
            self._wrap_polygon(surf, col, [
                (tx - 20, base_y),
                (tx - 8, base_y - spire_h + 40),
                (tx, base_y - spire_h),
                (tx + 8, base_y - spire_h + 40),
                (tx + 20, base_y),
            ])
            # Crimson vein glow on spire
            for _ in range(3):
                vy = base_y - random.randint(30, spire_h - 20)
                pygame.draw.line(surf, (180, 50, 70),
                               (tx - 3, vy), (tx + 3, vy), 2)
        # Pulsing ember particles
        random.seed(2222)
        for _ in range(80):
            ex = random.randint(0, self.w)
            ey = random.randint(100, SCREEN_HEIGHT - 60)
            col = random.choice([(220, 80, 50), (255, 120, 80), (180, 40, 60)])
            pygame.draw.circle(surf, col, (ex, ey), 1)
        # Bones/skulls in the distance (tiny silhouettes)
        for _ in range(5):
            bx = random.randint(30, self.w - 30)
            by = SCREEN_HEIGHT - random.randint(50, 70)
            pygame.draw.circle(surf, (30, 15, 20), (bx, by), 4)
        random.seed()
        return surf
