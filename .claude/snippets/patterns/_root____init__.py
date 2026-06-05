# From: backgrounds.py:936

    def __init__(self, biome: str = "forest") -> None:
        cls = _BIOME_MAP.get(biome, ForestBackground)
        self.bg = cls()
