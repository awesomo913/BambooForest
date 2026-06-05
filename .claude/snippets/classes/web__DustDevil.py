# From: web/biomes.py:943
# Level 6. Invincible erratic sandstorm, must dodge. Minimum 150px patrol

class DustDevil(pygame.sprite.Sprite):
    """Level 6. Invincible erratic sandstorm, must dodge. Minimum 150px patrol
    to ensure the movement pattern reads clearly even in tight spaces.
    """
    is_stompable: bool = False

    def __init__(self, x: int, y: int, patrol_width: float = 300.0) -> None:
        super().__init__()
        # Enforce minimum width so small instances still move visibly
        self.patrol_width = max(150.0, patrol_width)
        # Build a bigger, more readable sandstorm sprite (44x72)
        W, H = 44, 72
        self._frames = []
        for frame_offset in range(4):
            surf = pygame.Surface((W, H), pygame.SRCALPHA)
            for dy in range(0, H, 3):
                # Wider base, narrower top (tornado shape)
                base_w = 10 + int(14 * (dy / H))
                wobble = int(7 * math.sin(dy * 0.15 + frame_offset))
                w = base_w + wobble
                # Darker sand at core, lighter at edges
                alpha = 140 if abs(wobble) < 4 else 90
                pygame.draw.rect(surf, (*COL_SANDSTONE, alpha),
                                 (W // 2 - w // 2, dy, w, 3))
            # Darker swirl lines
            for i in range(4):
                sx = (frame_offset * 3 + i * 5) % W
                pygame.draw.line(surf, (140, 100, 60, 160),
                                 (sx, 10), (sx + 6, H - 8), 1)
            self._frames.append(surf)
        self.image = self._frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.origin_x = float(x)
        self.pos_x = float(x)
        self.time: float = random.uniform(0, 6.28)
        self.alive_flag = True

    def update(self, dt: float, platforms: pygame.sprite.Group,
               player=None) -> None:
        self.time += dt * 3
        self.pos_x = self.origin_x + math.sin(self.time) * self.patrol_width * 0.5
        self.pos_x += math.sin(self.time * 2.7) * self.patrol_width * 0.3
        self.rect.x = _fl(self.pos_x)
        self.rect.y = _fl(FLOOR_Y - 72 + math.sin(self.time * 1.5) * 10)
        # Cycle through swirl frames for visible animation
        frame_idx = int(self.time * 8) % len(self._frames)
        self.image = self._frames[frame_idx]

    def die(self) -> None:
        pass

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
