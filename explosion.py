# explosion.py

from settings import EXPLOSION_FRAME_MS


class Explosion:
    """A short frame animation.

    update() advances the animation and draw() only draws, so explosions keep
    animating and get reaped even on a frame that skips rendering.
    """

    def __init__(self, x, y, assets, frame_ms=EXPLOSION_FRAME_MS):
        self.frames = assets["explosion"]
        self.rect = self.frames[0].get_rect(center=(x, y))
        self.current_frame = 0
        self.frame_ms = frame_ms
        self._elapsed = 0.0
        self.done = False

    def update(self, dt):
        """Advance by dt seconds. Returns True once the animation is finished."""
        if self.done:
            return True
        self._elapsed += dt * 1000.0
        while self._elapsed >= self.frame_ms:
            self._elapsed -= self.frame_ms
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 1
                self.done = True
                return True
        return False

    def draw(self, win):
        if not self.done:
            win.blit(self.frames[self.current_frame], self.rect)
