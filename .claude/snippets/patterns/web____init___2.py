# From: web/biomes.py:949

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
