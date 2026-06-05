# From: game.py:263

    def _load_level(self, level_num: int) -> None:
        self.level = build_level_state(level_num)
        self.camera = Camera(self.level.world_width, SCREEN_HEIGHT)
        self.background = BiomeBackground(self.level.biome)
        self.respawn_x = self.level.player_start[0]
        self.respawn_y = self.level.player_start[1]
        self.player = Player(self.respawn_x, self.respawn_y)
        if level_num >= DOUBLE_JUMP_LEVEL:
            self.player.has_double_jump = True
        # Glide + Dash are per-level timed pickups (not permanent).
        # Player must collect them each level to use those abilities.
        # Ice magic persists once unlocked from boss kill
        if self._has_ice_magic_permanent:
            self.player.has_ice_magic = True
            self.player.mana = self.player.mana_max
        if self.level.is_icy:
            self.player.friction_mode = "ice"
        else:
            self.player.friction_mode = "normal"
        self.player.reset_state()  # clear input locks, dash, attack flags
        self.player.score = self._total_score
        self.level.all_sprites.add(self.player)
        self.current_level = level_num
        self.particles = ParticleSystem()
        self.hud = HUD()
        self.hud.set_bamboo_count(len(self.level.bamboos))
        self.hud.lives = self.lives
        self.death_anim = None
        self._was_on_ground = False
        self._jump_pressed = False
        self._outro_active = False
        self._outro_timer = 0.0
        # If player already has weapon from previous level, keep tutorial hidden
        if self.player.has_bamboo_weapon:
            self._weapon_used = True
        self.state = ST_PLAYING
