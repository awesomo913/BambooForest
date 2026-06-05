# From: biomes.py:1582

    def __init__(self, x: int, y: int, w: int, h: int,
                 group_id: str, platforms_group: pygame.sprite.Group) -> None:
        super().__init__()
        self.group_id = group_id  # "A" or "B"
        self._platforms_group = platforms_group
        self.rect = pygame.Rect(x, y, w, h)
        self._solid_img = self._make_surf(w, h, lit=True)
        self._intangible_img = self._make_surf(w, h, lit=False)
        self.solid: bool = (group_id == "A")  # A starts solid, B starts intangible
        self.image = self._solid_img if self.solid else self._intangible_img
        if self.solid:
            platforms_group.add(self)
        self._flicker: float = 0.0
