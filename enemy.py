# enemy.py

import pygame

from entity import Entity
from settings import (
    BOSS_HEALTH, BOSS_SPEED, ENEMY_FAST_SPEED, ENEMY_SPEED, RED, WIDTH, YELLOW,
)


class Enemy(Entity):
    """A descending enemy. Fast variants use their own sprite."""

    def __init__(self, x, y, speed, assets):
        # Pick the sprite from the speed, so the enemy_fast art is actually used.
        fast = speed >= ENEMY_FAST_SPEED
        super().__init__(assets["enemy_fast"] if fast else assets["enemy"], x, y)
        self.fast = fast
        self.speed = speed

    def move(self, dt):
        self.move_by(0, self.speed * dt)


class Boss(Entity):
    """A level boss that paces horizontally across the top of the screen."""

    def __init__(self, x, y, assets, speed=BOSS_SPEED):
        super().__init__(assets["boss"], x, y)
        self.health = BOSS_HEALTH
        self.direction = 1
        self.speed = speed

    def move(self, dt):
        self.move_by(self.direction * self.speed * dt, 0)
        # Clamp before reversing, so a large dt cannot leave the boss outside
        # the screen flip-flopping against the edge.
        clamped = max(0.0, min(self._x, float(WIDTH - self.rect.width)))
        if clamped != self._x:
            self._x = clamped
            self.rect.x = round(clamped)
            self.direction *= -1

    def draw(self, win):
        super().draw(win)
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        ratio = max(0.0, self.health / BOSS_HEALTH)
        pygame.draw.rect(win, RED, (self.rect.x, self.rect.bottom + 10, self.rect.width, 10))
        pygame.draw.rect(
            win, YELLOW, (self.rect.x, self.rect.bottom + 10, int(self.rect.width * ratio), 10)
        )


def enemy_speed_for(level, fast=False):
    """Enemy speed for a level. Speed creeps up so later waves stay interesting."""
    base = ENEMY_FAST_SPEED if fast else ENEMY_SPEED
    return base * (1.0 + 0.05 * (level - 1))
