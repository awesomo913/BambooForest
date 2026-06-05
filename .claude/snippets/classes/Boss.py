# From: sprites.py:1710
# Mutant panda boss with clear state-machine telegraph.

class Boss(pygame.sprite.Sprite):
    """Mutant panda boss with clear state-machine telegraph.

    States:
      idle (1.5s)       -- faces player, calm
      telegraph (0.8s)  -- FLASHES RED, warning charge incoming
      charging (varies) -- dashes toward player's last position
      stunned (1.5s)    -- BLUE TINT, vulnerable window, player can stomp
      defeated          -- dies after BOSS_HP stomps during stun

    Win condition: Stomp the boss BOSS_HP times during its stunned state.
    Each hit shows damage flash + HP bar decrement above the boss.
    """
    is_stompable: bool = True

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

    def update(self, dt: float, player: Player,  # type: ignore[override]
               platforms: pygame.sprite.Group) -> None:
        if not self.alive_flag:
            return
        self.flash_timer = max(0.0, self.flash_timer - dt)

        # Always track the player
        dx_player = player.rect.centerx - self.rect.centerx
        abs_dist = abs(dx_player)
        self.facing_right = dx_player > 0

        AGGRO_RANGE = 600.0
        ATTACK_RANGE = 140.0
        CHASE_SPEED = BOSS_CHARGE_SPEED * 0.75  # faster chase -- feels threatening
        LUNGE_SPEED = BOSS_CHARGE_SPEED * 1.6   # FAST attack lunge

        if self.state == "idle":
            self.state_timer -= dt
            if self.state_timer <= 0:
                if abs_dist < AGGRO_RANGE:
                    self.state = "chasing"
                else:
                    self.state_timer = BOSS_IDLE_SEC
            self.stunned = False
        elif self.state == "chasing":
            if abs_dist > ATTACK_RANGE:
                self.rect.x += _fl(CHASE_SPEED * dt * (1 if dx_player > 0 else -1))
            else:
                # Telegraph (longer + VERY obvious)
                self.state = "telegraph"
                self.state_timer = 0.9
                self.telegraph_timer = 0.9
        elif self.state == "telegraph":
            self.state_timer -= dt
            self.telegraph_timer = self.state_timer
            if self.state_timer <= 0:
                self.state = "attacking"
                # Lock the attack direction at lunge start so the boss
                # commits -- player can dodge past him if timed right
                self._lunge_dir = 1 if dx_player > 0 else -1
                self.state_timer = 0.45
        elif self.state == "attacking":
            # Commit to the locked direction -- no mid-lunge tracking
            self.rect.x += _fl(LUNGE_SPEED * dt * self._lunge_dir)
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "stunned"
                self.stunned = True
                self.state_timer = BOSS_STUN_SEC
        elif self.state == "stunned":
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = BOSS_IDLE_SEC * 0.5
                self.stunned = False

        # Gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY
        self.rect.y += _fl(self.velocity_y * dt)
        for hit in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
                self.velocity_y = 0

        # Visuals: base flip by facing
        img = self._base_image if self.facing_right else pygame.transform.flip(
            self._base_image, True, False)
        # Telegraph: strong red flash 4 times/sec
        if self.state == "telegraph":
            if int(self.telegraph_timer * 8) % 2 == 0:
                img = img.copy()
                img.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_ADD)
        # Damage flash (white burst after being hit)
        elif self.flash_timer > 0:
            if int(self.flash_timer * 20) % 2:
                img = img.copy()
                img.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_ADD)
        # Stun tint (strong pulsing BLUE overlay -- the vulnerable window)
        # Sword + stomp + ice all deal 1 HP while this is visible.
        if self.stunned:
            img = img.copy()
            # Pulsing intensity synced to game clock for visibility
            t = pygame.time.get_ticks() / 120.0
            pulse = int(140 + 60 * math.sin(t))
            img.fill((60, 140, 255, pulse), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = img

    def take_hit(self) -> bool:
        self.hp -= 1
        self.flash_timer = 0.35
        if self.hp <= 0:
            self.alive_flag = False
            self.kill()
            return True
        return False

    def alive(self) -> bool:  # type: ignore[override]
        return self.alive_flag
