# powerup.py

from entity import Entity
from settings import POWERUP_SPEED


class PowerUp(Entity):
    """A collectable that grants rapid fire for a short time."""

    def __init__(self, x, y, assets, speed=POWERUP_SPEED):
        super().__init__(assets["powerup"], x, y)
        self.speed = speed

    def move(self, dt):
        self.move_by(0, self.speed * dt)
