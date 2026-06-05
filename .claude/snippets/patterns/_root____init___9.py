# From: bamboo_forest.py:92

    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("mutant.png", 45, 45, (255, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.velocity_y = 0
        self.gravity = 0.8
        self.speed_x = 3 # Sped up the enemy
