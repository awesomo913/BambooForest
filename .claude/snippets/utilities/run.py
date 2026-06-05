# From: web/game.py:94
# Async main loop -- Pygbag/WASM requirement.

    async def run(self) -> None:
        """Async main loop -- Pygbag/WASM requirement."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()
            await asyncio.sleep(0)
        pygame.quit()
