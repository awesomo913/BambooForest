# From: biomes.py:387
# Platform with biome-specific tile art.

class BiomePlatform(pygame.sprite.Sprite):
    """Platform with biome-specific tile art."""

    def __init__(self, x: int, y: int, w: int, h: int = 20,
                 biome: str = "forest") -> None:
        super().__init__()
        gen = _TILE_GENERATORS.get(biome)
        if gen:
            self.image = gen(w, h)
        else:
            from sprites import generate_platform_tile
            self.image = generate_platform_tile(w, h)
        self.rect = self.image.get_rect(topleft=(x, y))
