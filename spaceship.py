# spaceship.py

import pygame

from entity import Entity
from settings import (
    GREEN, HEIGHT, HIT_INVULNERABILITY_MS, MAX_WEAPON_LEVEL, PLAYER_MAX_HEALTH,
    POWERUP_DURATION, RAPID_FIRE_COOLDOWN_MS, RED, SHOOT_COOLDOWN_MS,
    SPACESHIP_SPEED, WHITE, WIDTH,
)


class Spaceship(Entity):
    """The player ship: movement, health, weapon tier and power-up state."""

    def __init__(self, x, y, assets, speed=SPACESHIP_SPEED):
        super().__init__(assets["spaceship"], x, y)
        self.speed = speed
        self.health = PLAYER_MAX_HEALTH
        self.powered_up = False
        self.power_up_end_time = 0
        self.weapon_level = 1
        self.last_shot = 0
        self.invulnerable_until = 0

    # -- movement ---------------------------------------------------------

    def move(self, dx, dy, dt):
        self.move_by(dx * self.speed * dt, dy * self.speed * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        # clamp_ip may have moved the rect; keep the float position in step.
        self.sync_from_rect()

    # -- combat -----------------------------------------------------------

    @property
    def shoot_cooldown(self):
        """Rapid fire while a power-up is active. This is what power-ups do."""
        return RAPID_FIRE_COOLDOWN_MS if self.powered_up else SHOOT_COOLDOWN_MS

    def can_shoot(self, now):
        return now - self.last_shot >= self.shoot_cooldown

    def register_shot(self, now):
        self.last_shot = now

    def is_invulnerable(self, now):
        return now < self.invulnerable_until

    def take_damage(self, amount, now):
        """Apply damage unless still in the grace period after the last hit.

        Returns True if the hit landed. Without this, contact damage applies
        every frame and overlapping an enemy for a moment is instant death.
        """
        if self.is_invulnerable(now):
            return False
        self.health = max(0, self.health - amount)
        self.invulnerable_until = now + HIT_INVULNERABILITY_MS
        return True

    # -- power-ups --------------------------------------------------------

    def power_up(self, now):
        self.powered_up = True
        self.power_up_end_time = now + POWERUP_DURATION

    def check_power_up(self, now):
        if self.powered_up and now > self.power_up_end_time:
            self.powered_up = False

    def upgrade_weapon(self):
        if self.weapon_level < MAX_WEAPON_LEVEL:
            self.weapon_level += 1

    def bullet_origins(self):
        """Muzzle positions for the current weapon tier."""
        cx, top = self.rect.centerx, self.rect.top
        if self.weapon_level == 1:
            return [(cx, top)]
        if self.weapon_level == 2:
            return [(cx - 10, top), (cx + 10, top)]
        return [(cx, top), (cx - 20, top), (cx + 20, top)]

    # -- drawing ----------------------------------------------------------

    def draw(self, win, now=0):
        # Blink while invulnerable so the grace period is visible.
        if self.is_invulnerable(now) and (now // 100) % 2 == 0:
            return
        super().draw(win)

    def draw_health_bar(self, win):
        ratio = max(0.0, self.health / PLAYER_MAX_HEALTH)
        pygame.draw.rect(win, RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(
            win, GREEN, (self.rect.x, self.rect.y - 10, int(self.rect.width * ratio), 5)
        )
        if self.powered_up:
            pygame.draw.rect(win, WHITE, (self.rect.x, self.rect.y - 14, self.rect.width, 2))
