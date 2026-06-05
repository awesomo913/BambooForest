# From: biomes.py:1740

    def __init__(self, x: int, y: int, pair_id: int) -> None:
        super().__init__()
        self.pair_id = pair_id
        self.color = _PORTAL_PAIR_COLORS[pair_id % len(_PORTAL_PAIR_COLORS)]
        self.partner: TeleportPortal | None = None
        self.active: bool = True
        self.cooldown: float = 0.0
        self._rot: float = 0.0
        self._w, self._h = 44, 64
        self.rect = pygame.Rect(0, 0, self._w, self._h)
        self.rect.midbottom = (x, y)
        self.image = self._make_surf()
