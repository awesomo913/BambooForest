# From: sprites.py:1014
# Stab hitbox: fast out, hold, quick retract.

    def get_attack_rect(self) -> pygame.Rect:
        """Stab hitbox: fast out, hold, quick retract."""
        if not self.is_attacking:
            return pygame.Rect(0, 0, 0, 0)
        max_reach = 60
        total = 0.25
        atk_t = 1.0 - (self.attack_timer / total)
        atk_t = max(0.0, min(1.0, atk_t))
        # Reach curve: 0-0.2 grow fast, 0.2-0.7 hold max, 0.7-1.0 retract
        if atk_t < 0.2:
            reach = int(max_reach * (atk_t / 0.2))
        elif atk_t < 0.7:
            reach = max_reach
        else:
            reach = int(max_reach * (1.0 - (atk_t - 0.7) / 0.3))
        reach = max(reach, 20)  # minimum reach while attacking
        hit_h = 30
        hit_y = self.rect.y + 2
        if self.facing_right:
            return pygame.Rect(self.rect.right, hit_y, reach, hit_h)
        return pygame.Rect(self.rect.left - reach, hit_y, reach, hit_h)
