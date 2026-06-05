# From: sprites.py:1149

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.base_image = generate_bamboo_surface()
        # Pre-render a composite with a glow halo around the stalk
        w, h = self.base_image.get_size()
        self._composite = pygame.Surface((w + 12, h + 12), pygame.SRCALPHA)
        self._stalk_offset = (6, 6)
        self.image = self._composite.copy()
        # Blit stalk on top
        self.image.blit(self.base_image, self._stalk_offset)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.base_y = float(self.rect.y)
        self.bob_timer: float = random.uniform(0, 6.28)
        self.glow_timer: float = random.uniform(0, 6.28)
