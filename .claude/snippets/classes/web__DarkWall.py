# From: web/biomes.py:2187
# Wall that only disappears when a crystal within range is lit.

class DarkWall(pygame.sprite.Sprite):
    """Wall that only disappears when a crystal within range is lit."""

    def __init__(self, x, y, w, h, crystals_group, platforms_group,
                 reveal_range=350.0):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self._crystals = crystals_group
        self._platforms = platforms_group
        self._reveal_range = reveal_range
        # Deranged / eldritch dark wall visual
        solid = pygame.Surface((w, h), pygame.SRCALPHA)
        # Deep pulsing void base
        solid.fill((15, 5, 30))
        # Warped cracks and veins
        for _ in range(max(2, w // 8)):
            vx = random.randint(4, max(5, w - 4))
            vy = random.randint(4, max(5, h - 4))
            vlen = random.randint(10, min(40, h - 4))
            col = random.choice([(200, 60, 255), (255, 40, 120), (120, 0, 200)])
            pygame.draw.line(solid, col,
                            (vx, vy),
                            (vx + random.randint(-8, 8), vy + vlen), 2)
        # Eye-like shapes peering through
        for _ in range(max(1, w // 18)):
            ex = random.randint(6, max(7, w - 6))
            ey = random.randint(8, max(9, h - 8))
            # Outer eye glow
            pygame.draw.ellipse(solid, (180, 40, 200),
                               (ex - 5, ey - 3, 10, 6))
            # Pupil
            pygame.draw.circle(solid, (255, 0, 80), (ex, ey), 2)
            pygame.draw.circle(solid, (255, 255, 200), (ex + 1, ey - 1), 1)
        # Jagged edge border (deranged look)
        for by in range(0, h, 4):
            jag = random.randint(0, 3)
            col = random.choice([(200, 60, 255), (255, 80, 160)])
            pygame.draw.line(solid, col, (jag, by), (jag, by + 3), 2)
            pygame.draw.line(solid, col, (w - jag - 1, by), (w - jag - 1, by + 3), 2)
        # Top/bottom jagged edge
        for bx in range(0, w, 4):
            jag = random.randint(0, 3)
            col = (200, 60, 255)
            pygame.draw.line(solid, col, (bx, jag), (bx + 3, jag), 2)
            pygame.draw.line(solid, col, (bx, h - jag - 1), (bx + 3, h - jag - 1), 2)
        # Scattered corruption dots
        for _ in range(max(3, w * h // 30)):
            sx = random.randint(1, max(2, w - 2))
            sy = random.randint(1, max(2, h - 2))
            solid.set_at((sx, sy), random.choice([
                (255, 60, 200), (200, 0, 255), (255, 100, 255), (100, 0, 180)]))
        self._solid = solid
        # Faded version when crystal reveals
        faded = solid.copy()
        faded.set_alpha(35)
        self._faded = faded
        self.solid = True
        self.image = self._solid
        platforms_group.add(self)

    def update(self, dt):
        nearby_lit = False
        for cr in self._crystals:
            if getattr(cr, 'is_lit', lambda: False)():
                dx = cr.rect.centerx - self.rect.centerx
                dy = cr.rect.centery - self.rect.centery
                if math.hypot(dx, dy) < self._reveal_range:
                    nearby_lit = True
                    break
        should_solid = not nearby_lit
        if should_solid and not self.solid:
            self.solid = True
            self._platforms.add(self)
            self.image = self._solid
        elif not should_solid and self.solid:
            self.solid = False
            self._platforms.remove(self)
            self.image = self._faded
