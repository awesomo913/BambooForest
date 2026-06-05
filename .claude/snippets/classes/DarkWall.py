# From: biomes.py:2208
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
        # --- Magical barrier: 4-frame animation with flowing runic energy ---
        self._frames = []
        for phase in range(4):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            # Deep void base with slight violet tint
            surf.fill((12, 4, 28, 235))
            # Layered hex-pattern for barrier "mesh" feel
            for hy in range(-4 + phase * 2, h + 4, 10):
                pygame.draw.line(surf, (60, 30, 100, 180),
                                 (0, hy), (w, hy + 4), 1)
                pygame.draw.line(surf, (60, 30, 100, 180),
                                 (0, hy + 6), (w, hy + 2), 1)
            # Runic bars (thick horizontal energy threads)
            for i, bar_y in enumerate(range(10, h - 10, max(20, h // 4))):
                # Outer purple glow
                pygame.draw.rect(surf, (110, 40, 180),
                                 (3, bar_y - 3, w - 6, 8))
                # Inner bright cyan-purple core
                pygame.draw.rect(surf, (200, 140, 255),
                                 (5, bar_y, w - 10, 2))
                # Animated flowing highlight packet
                packet_x = ((phase * 12) + i * 16) % max(12, w - 12)
                pygame.draw.rect(surf, (255, 230, 255),
                                 (packet_x, bar_y, 8, 2))
            # Central runic sigils (circle + cross)
            for rune_y in [h // 3, 2 * h // 3]:
                cx = w // 2
                # Outer ring (pulses with phase)
                ring_col = (130 + phase * 20, 60 + phase * 10,
                            200 + phase * 10)
                pygame.draw.circle(surf, ring_col, (cx, rune_y),
                                   min(8, w // 3), 2)
                # Inner filled dot
                pygame.draw.circle(surf, (200, 100, 230),
                                   (cx, rune_y), 3)
                pygame.draw.circle(surf, (255, 220, 255),
                                   (cx, rune_y), 1)
                # Cross strokes
                pygame.draw.line(surf, (255, 200, 255),
                                 (cx - 6, rune_y), (cx + 6, rune_y), 1)
                pygame.draw.line(surf, (255, 200, 255),
                                 (cx, rune_y - 6), (cx, rune_y + 6), 1)
            # Glowing edge particles climbing up both sides
            for py_ in range(0, h, 5):
                offset = (phase * 3 + py_ // 5) % 5
                pygame.draw.circle(surf, (200, 120, 255),
                                   (2 + offset, py_), 1)
                pygame.draw.circle(surf, (200, 120, 255),
                                   (w - 3 - offset, py_), 1)
            # Thick bright cap at top and bottom (so it reads as a WALL)
            pygame.draw.rect(surf, (180, 80, 220), (0, 0, w, 3))
            pygame.draw.rect(surf, (255, 180, 255), (0, 0, w, 1))
            pygame.draw.rect(surf, (180, 80, 220), (0, h - 3, w, 3))
            pygame.draw.rect(surf, (255, 180, 255), (0, h - 1, w, 1))
            self._frames.append(surf)
        # Faded frames (shown when nearby crystal is lit -- shows the wall
        # dissolving, still visible as a ghost so the player sees the passage)
        self._faded_frames = []
        for f in self._frames:
            ff = f.copy()
            ff.set_alpha(55)
            self._faded_frames.append(ff)
        self.solid = True
        self.image = self._frames[0]
        self._frame_timer: float = 0.0
        platforms_group.add(self)

    def update(self, dt):
        # Animate across 4 frames at ~6 fps
        self._frame_timer += dt
        frame_idx = int(self._frame_timer * 6) % 4

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
        elif not should_solid and self.solid:
            self.solid = False
            self._platforms.remove(self)
        # Pick frame from active (solid) or faded bank every tick
        if self.solid:
            self.image = self._frames[frame_idx]
        else:
            self.image = self._faded_frames[frame_idx]
