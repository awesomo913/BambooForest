# From: biomes.py:939
# Level 6. Invincible erratic sandstorm, must dodge. Minimum 150px patrol

class DustDevil(pygame.sprite.Sprite):
    """Level 6. Invincible erratic sandstorm, must dodge. Minimum 150px patrol
    to ensure the movement pattern reads clearly even in tight spaces.
    """
    is_stompable: bool = False

    def __init__(self, x: int, y: int, patrol_width: float = 300.0) -> None:
        super().__init__()
        # Minimum patrol width so movement reads clearly even in tight spaces
        self.patrol_width = max(150.0, patrol_width)
        # Build a BIG tornado -- wide at top, narrow at ground (real dust-devil shape)
        W, H = 64, 110
        self._frames = []
        for frame_offset in range(6):
            surf = pygame.Surface((W, H), pygame.SRCALPHA)
            # Column slabs: width starts wide at top and tapers to narrow point
            for dy in range(0, H, 3):
                frac = dy / H  # 0 at top, 1 at bottom
                # Wide top (50% of W), narrow bottom (15%)
                base_w = int(W * (0.5 - 0.35 * frac))
                # Swirl wobble -- shifts with frame for rotation illusion
                wobble = int(9 * math.sin(dy * 0.18 + frame_offset * 0.9))
                w = max(4, base_w + abs(wobble))
                off_x = wobble // 2
                # Alpha gradient: more opaque in middle of the column
                alpha = 180 - int(abs(wobble) * 6)
                alpha = max(70, min(200, alpha))
                # Darker sand core, lighter at edges
                col_core = (150, 110, 65, alpha)
                col_edge = (200, 170, 120, max(40, alpha - 60))
                rect_x = (W - w) // 2 + off_x
                pygame.draw.rect(surf, col_core, (rect_x, dy, w, 3))
                # Bright edge highlights to catch the eye
                pygame.draw.rect(surf, col_edge, (rect_x, dy, 2, 3))
                pygame.draw.rect(surf, col_edge, (rect_x + w - 2, dy, 2, 3))
            # Rotating debris streaks (darker, diagonal)
            for i in range(6):
                sx_top = (frame_offset * 4 + i * 11) % W
                sx_bot = (sx_top + W // 2) % W  # crossover diagonal
                pygame.draw.line(surf, (90, 60, 30, 180),
                                 (sx_top, 4), (sx_bot, H - 6), 2)
            # Flying sand particles scattered around
            for _ in range(15):
                px = random.randint(0, W - 1)
                py_ = random.randint(0, H - 1)
                pygame.draw.circle(surf, (220, 190, 130, 200), (px, py_), 1)
            # Cap at top: wide dark "cloud" cap so it reads as a SANDSTORM
            cap_w = int(W * 0.55)
            cap_x = (W - cap_w) // 2
            pygame.draw.ellipse(surf, (120, 90, 55, 200),
                                (cap_x, 0, cap_w, 14))
            pygame.draw.ellipse(surf, (160, 130, 90, 150),
                                (cap_x + 4, 2, cap_w - 8, 10))
            self._frames.append(surf)
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.pos_x = float(x)
        self.time: float = random.uniform(0, 6.28)
        self.alive_flag = True
        self._W, self._H = W, H

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        self.time += dt * 3
        self.pos_x = self.origin_x + math.sin(self.time) * self.patrol_width * 0.5
        self.pos_x += math.sin(self.time * 2.7) * self.patrol_width * 0.3
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(FLOOR_Y - self._H + math.sin(self.time * 1.5) * 8)
        # Fast swirl frame cycle (~16fps) for strong rotation feel
        frame_idx = int(self.time * 10) % len(self._frames)
        self.image = self._frames[frame_idx]

    def die(self) -> None:
        pass

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
