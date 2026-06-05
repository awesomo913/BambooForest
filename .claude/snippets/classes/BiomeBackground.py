# From: backgrounds.py:933
# Factory that returns the correct background for each biome.

class BiomeBackground:
    """Factory that returns the correct background for each biome."""

    def __init__(self, biome: str = "forest") -> None:
        cls = _BIOME_MAP.get(biome, ForestBackground)
        self.bg = cls()

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:
        self.bg.draw(screen, camera_x)
