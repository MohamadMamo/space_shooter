# bullet.py

from entity import Entity
from settings import BULLET_SPEED


class Bullet(Entity):
    """A player projectile travelling straight up."""

    def __init__(self, x, y, assets, speed=BULLET_SPEED):
        super().__init__(assets["bullet"], x, y)
        self.speed = speed

    def move(self, dt):
        self.move_by(0, -self.speed * dt)
