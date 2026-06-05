# From: sprites.py:1725

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._base_image = generate_mutant_boss(*BOSS_SIZE)
        self.image = self._base_image
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.max_hp: int = BOSS_HP
        self.hp: int = BOSS_HP
        self.state: str = "idle"
        self.state_timer: float = BOSS_IDLE_SEC
        self.charge_target_x: float = 0.0
        self.stunned: bool = False
        self.facing_right: bool = False
        self.velocity_y: float = 0.0
        self.alive_flag: bool = True
        self.flash_timer: float = 0.0
        self.telegraph_timer: float = 0.0
        self._lunge_dir: int = 1
