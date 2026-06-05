# From: sprites.py:1245
# Glowing cyan-white diamond-shaped ice shard.

    @staticmethod
    def _make_shard() -> pygame.Surface:
        """Glowing cyan-white diamond-shaped ice shard."""
        W, H = 36, 20
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        # Outer glow halo (concentric ellipses)
        for r_scale, alpha in [(1.0, 60), (0.8, 120), (0.6, 180)]:
            w2, h2 = int(W * r_scale), int(H * r_scale)
            ox, oy = (W - w2) // 2, (H - h2) // 2
            pygame.draw.ellipse(surf, (140, 220, 255, alpha),
                                (ox, oy, w2, h2))
        # Core ice shard (diamond shape)
        pts = [(2, H // 2), (W // 2, 3), (W - 3, H // 2),
               (W // 2, H - 3)]
        pygame.draw.polygon(surf, (200, 240, 255), pts)
        # Inner highlight
        pts2 = [(6, H // 2), (W // 2, 6), (W - 7, H // 2), (W // 2, H - 6)]
        pygame.draw.polygon(surf, (255, 255, 255), pts2)
        # Tip sparkles
        pygame.draw.circle(surf, (255, 255, 255), (W - 3, H // 2), 2)
        pygame.draw.circle(surf, (255, 255, 255), (2, H // 2), 2)
        return surf
