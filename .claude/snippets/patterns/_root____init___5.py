# From: bamboo_forest.py:23

    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("panda.png", 40, 40, (0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.velocity_y = 0
        self.speed_x = 6
        self.gravity = 0.8
        self.jump_power = -15
        self.is_on_ground = False
        
        self.health = 100
        self.score = 0
        self.invincible_timer = 0 # Prevents instant-death collisions
