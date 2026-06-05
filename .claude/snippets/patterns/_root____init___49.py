# From: module_auto.py:44

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("panda.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 6
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.is_on_ground = False
        self.health = 100
        self.score = 0
        self.invincible_timer = 0
