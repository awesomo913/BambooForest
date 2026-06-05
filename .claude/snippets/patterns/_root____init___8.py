# From: bamboo_forest.py:86

    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("heal.png", 25, 25, (255, 105, 180)) # Pink fallback
        self.rect = self.image.get_rect(bottomleft=(x, y))
