# From: biomes.py:405

    def __init__(self, x: int, y: int, w: int, h: int,
                 axis: str = "horizontal", distance: float = 150.0,
                 biome: str = "forest") -> None:
        super().__init__()
        gen = _TILE_GENERATORS.get(biome)
        if gen:
            self.image = gen(w, h)
        else:
            from sprites import generate_platform_tile
            self.image = generate_platform_tile(w, h)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.origin_x = float(x)
        self.origin_y = float(y)
        self.axis = axis
        self.distance = distance
        self.direction: float = 1.0
        self.pos_x = float(x)
        self.pos_y = float(y)
