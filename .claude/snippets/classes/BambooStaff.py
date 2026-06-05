# From: sprites.py:1411
# Pickup that grants Pain-da a bamboo weapon (swing with E/X/LMB).

class BambooStaff(pygame.sprite.Sprite):
    """Pickup that grants Pain-da a bamboo weapon (swing with E/X/LMB).

    Rendered as a proper bo-staff: diagonal bamboo pole with leaves at the
    tip, rope grip in the middle, golden halo around it.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # Build diagonal bo-staff on a 56x56 canvas
        W, H = 56, 56
        base = pygame.Surface((W, H), pygame.SRCALPHA)
        # Pole endpoints (lower-left to upper-right diagonal)
        p1 = (8, H - 10)
        p2 = (W - 8, 10)
        # Shadow trail behind pole (depth)
        pygame.draw.line(base, (50, 110, 40), (p1[0] + 2, p1[1] + 2),
                         (p2[0] + 2, p2[1] + 2), 6)
        # Main bamboo pole (thick, vibrant)
        pygame.draw.line(base, (130, 195, 80), p1, p2, 6)
        # Highlight stripe
        pygame.draw.line(base, (180, 230, 120),
                         (p1[0] - 1, p1[1] - 1), (p2[0] - 1, p2[1] - 1), 2)
        # Joint segments along the pole
        import math as _m
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = _m.hypot(dx, dy)
        nx, ny = dx / length, dy / length
        perp_x, perp_y = -ny, nx
        for frac in (0.18, 0.42, 0.66, 0.88):
            jx = int(p1[0] + dx * frac)
            jy = int(p1[1] + dy * frac)
            # Dark ring perpendicular to pole
            rx = int(perp_x * 5)
            ry = int(perp_y * 5)
            pygame.draw.line(base, (60, 130, 35),
                             (jx - rx, jy - ry), (jx + rx, jy + ry), 2)
        # Rope grip in middle (dark red wrapping)
        mid_x = (p1[0] + p2[0]) // 2
        mid_y = (p1[1] + p2[1]) // 2
        for i in range(-6, 7, 2):
            gx = mid_x + int(nx * i)
            gy = mid_y + int(ny * i)
            rx = int(perp_x * 4)
            ry = int(perp_y * 4)
            pygame.draw.line(base, (160, 40, 35),
                             (gx - rx, gy - ry), (gx + rx, gy + ry), 1)
        # Leaves at top tip
        leaf_c1 = (85, 170, 55)
        leaf_c2 = (130, 200, 80)
        tip = p2
        pygame.draw.polygon(base, leaf_c1, [
            (tip[0], tip[1] - 2),
            (tip[0] + 14, tip[1] - 8),
            (tip[0] + 4, tip[1] + 2),
        ])
        pygame.draw.polygon(base, leaf_c2, [
            (tip[0] + 1, tip[1] - 3),
            (tip[0] + 10, tip[1] - 6),
            (tip[0] + 4, tip[1])])
        pygame.draw.polygon(base, leaf_c1, [
            (tip[0], tip[1]),
            (tip[0] + 10, tip[1] + 8),
            (tip[0] - 2, tip[1] + 6),
        ])
        # Hollow tip (bamboo cross-section)
        pygame.draw.circle(base, (200, 230, 150), tip, 3)
        pygame.draw.circle(base, (80, 140, 50), tip, 3, 1)
        # Butt cap at bottom
        pygame.draw.circle(base, (60, 130, 35), p1, 4)
        pygame.draw.circle(base, (100, 170, 65), p1, 3)

        self._base = base
        self.image = self._base.copy()
        self.rect = self.image.get_rect(center=(x, y - 26))
        self.base_y = float(self.rect.y)
        self.glow_timer: float = 0.0

    def update(self, dt: float) -> None:  # type: ignore[override]
        self.glow_timer += dt * 3.5
        # Gentle float + subtle rotation wobble
        self.rect.y = _fl(self.base_y + math.sin(self.glow_timer) * 3)
        # Pulsing golden halo behind
        alpha = int(110 + 60 * (math.sin(self.glow_timer * 1.5) + 1) * 0.5)
        W, H = self._base.get_size()
        img = pygame.Surface((W + 14, H + 14), pygame.SRCALPHA)
        # Soft halo (3 concentric rings for glow softness)
        cx, cy = (W + 14) // 2, (H + 14) // 2
        for r, a_f in ((28, 0.3), (22, 0.55), (16, 0.9)):
            halo = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(halo, (255, 230, 120, int(alpha * a_f)),
                              (r, r), r)
            img.blit(halo, (cx - r, cy - r),
                    special_flags=pygame.BLEND_RGBA_ADD)
        img.blit(self._base, (7, 7))
        self.image = img
