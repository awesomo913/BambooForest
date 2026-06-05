# From: engine.py:104

class ParticleSystem:
    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def update(self, dt: float) -> None:
        alive: list[Particle] = []
        for p in self.particles:
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.gravity:
                p.vy += 400 * dt
            p.life -= dt
            if p.life > 0:
                alive.append(p)
        self.particles = alive

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        for p in self.particles:
            sx, sy = camera.apply_pos(p.x, p.y)
            if sx < -20 or sx > SCREEN_WIDTH + 20 or sy < -20 or sy > SCREEN_HEIGHT + 20:
                continue
            alpha = max(0, min(255, int(255 * (p.life / p.max_life))))
            r, g, b = p.color
            color = (min(255, r), min(255, g), min(255, b))
            sz = max(1, int(p.size * (p.life / p.max_life)))
            if p.shape == "circle":
                if alpha > 200:
                    pygame.draw.circle(screen, color, (int(sx), int(sy)), sz)
                else:
                    s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*color, alpha), (sz, sz), sz)
                    screen.blit(s, (int(sx) - sz, int(sy) - sz))
            elif p.shape == "leaf":
                s = pygame.Surface((sz + 2, sz + 2), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (*color, alpha), (0, 0, sz + 2, max(1, sz // 2)))
                screen.blit(s, (int(sx), int(sy)))
            elif p.shape == "rect":
                if alpha > 200:
                    pygame.draw.rect(screen, color, (int(sx), int(sy), sz, sz))
                else:
                    s = pygame.Surface((sz, sz), pygame.SRCALPHA)
                    s.fill((*color, alpha))
                    screen.blit(s, (int(sx), int(sy)))

    def emit_sparkle(self, x: float, y: float, count: int = 8) -> None:
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(60, 180)
            self.particles.append(Particle(
                x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                SPARKLE_LIFE + random.uniform(-0.1, 0.1),
                (255, 215 + random.randint(-20, 20), random.randint(0, 80)),
                random.uniform(2, 5), "circle",
            ))

    def emit_dust(self, x: float, y: float, count: int = 5) -> None:
        for _ in range(count):
            self.particles.append(Particle(
                x + random.uniform(-10, 10), y,
                random.uniform(-40, 40), random.uniform(-80, -20),
                DUST_LIFE + random.uniform(0, 0.1),
                (COL_PLAT_DIRT[0] + random.randint(-15, 15),
                 COL_PLAT_DIRT[1] + random.randint(-10, 10),
                 COL_PLAT_DIRT[2] + random.randint(-5, 5)),
                random.uniform(2, 4), "circle", gravity=True,
            ))

    def emit_damage(self, x: float, y: float, count: int = 6) -> None:
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            self.particles.append(Particle(
                x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                0.3, (255, random.randint(30, 80), random.randint(0, 30)),
                random.uniform(2, 5), "circle", gravity=True,
            ))

    def emit_death(self, x: float, y: float, count: int = 15) -> None:
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            self.particles.append(Particle(
                x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                random.uniform(0.3, 0.7),
                (255, random.randint(50, 150), random.randint(0, 50)),
                random.uniform(3, 7), "circle", gravity=True,
            ))

    def emit_ambient_leaves(self, visible_rect: pygame.Rect) -> None:
        leaf_count = sum(1 for p in self.particles if p.shape == "leaf")
        while leaf_count < LEAF_COUNT:
            x = visible_rect.x + random.uniform(0, visible_rect.width)
            y = visible_rect.y + random.uniform(-40, visible_rect.height * 0.4)
            greens = [(60, 140, 40), (40, 120, 30), (80, 160, 50), (50, 130, 20),
                      (70, 150, 35), (90, 170, 55)]
            self.particles.append(Particle(
                x, y,
                random.uniform(-20, 20), random.uniform(15, 45),
                random.uniform(4, 8),
                random.choice(greens),
                random.uniform(3, 6), "leaf",
            ))
            leaf_count += 1
