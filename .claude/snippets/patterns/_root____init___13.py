# From: biomes.py:457

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # Dormant: dark rock opening with faint orange glow
        self._img_off = pygame.Surface((44, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(self._img_off, (40, 25, 30), (0, 8, 44, 16))
        pygame.draw.ellipse(self._img_off, (80, 45, 35), (4, 10, 36, 12))
        pygame.draw.ellipse(self._img_off, (180, 80, 40), (8, 12, 28, 8))
        pygame.draw.ellipse(self._img_off, (60, 35, 30), (2, 18, 40, 6))  # rock lip
        # Erupting: tall steam+lava column
        self._img_on = pygame.Surface((44, 200), pygame.SRCALPHA)
        # Base glow
        pygame.draw.ellipse(self._img_on, (40, 25, 30), (0, 184, 44, 16))
        pygame.draw.ellipse(self._img_on, (255, 100, 30), (4, 186, 36, 12))
        # Rising jet (narrowing toward top)
        for y in range(0, 185):
            t = y / 185.0
            w = int(8 + 24 * t)  # wider at bottom
            xc = 22
            alpha = int(200 - 150 * (1 - t))
            if y < 40:
                c = (255, 240, 180, min(255, alpha))
            elif y < 100:
                c = (255, 180, 80, min(255, alpha))
            else:
                c = (255, 120, 50, min(255, alpha))
            pygame.draw.rect(self._img_on, c, (xc - w // 2, y, w, 1))
        # Steam puffs at top
        for _ in range(8):
            px = random.randint(8, 36)
            py = random.randint(0, 40)
            pygame.draw.circle(self._img_on, (240, 230, 220, 180), (px, py),
                               random.randint(4, 8))
        self.image = self._img_off
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self._off_rect = self.image.get_rect(bottomleft=(x, y))
        self._on_rect = self._img_on.get_rect(bottomleft=(x, y))
        self.erupt_timer: float = random.uniform(0, GEYSER_INTERVAL)
        self.erupt_remaining: float = 0.0
