# game_state.py

import random

from bullet import Bullet
from enemy import Boss, Enemy, enemy_speed_for
from explosion import Explosion
from powerup import PowerUp
from settings import (
    BOSS_LEVEL_INTERVAL, ENEMIES_PER_LEVEL, FAST_ENEMY_LEVEL_INTERVAL, HEIGHT,
    MAX_ENEMIES_PER_WAVE, WIDTH,
)
from spaceship import Spaceship


class GameState:
    """All mutable game state, with one place that resets it.

    The previous code duplicated a ten-line reset block at two collision sites
    and rebound the entity lists while an outer loop was still iterating the
    old ones, which raised ValueError on the next remove(). Keeping the lists
    on an object and clearing them in place removes both problems: nothing is
    ever rebound, so no live iteration can be invalidated.
    """

    def __init__(self, assets, high_score=0):
        self.assets = assets
        self.high_score = high_score
        self.bullets = []
        self.enemies = []
        self.power_ups = []
        self.explosions = []
        self.boss = None
        self.spaceship = None
        self.score = 0
        self.level = 1
        self.combo = 1
        self.game_over = False
        self.reset()

    def reset(self):
        """Return to a fresh run. Clears in place; never rebinds a list."""
        self.spaceship = Spaceship(WIDTH // 2, HEIGHT - 50, self.assets)
        self.bullets.clear()
        self.enemies.clear()
        self.power_ups.clear()
        self.explosions.clear()
        self.boss = None
        self.score = 0
        self.level = 1
        self.combo = 1
        self.game_over = False
        self.spawn_wave()

    # -- spawning ---------------------------------------------------------

    def spawn_wave(self):
        """Populate the next wave, capped so late levels stay playable."""
        count = min(self.level * ENEMIES_PER_LEVEL, MAX_ENEMIES_PER_WAVE)
        speed = enemy_speed_for(self.level)
        for _ in range(count):
            self.enemies.append(
                Enemy(
                    random.randint(20, WIDTH - 20),
                    random.randint(-1500, -100),
                    speed,
                    self.assets,
                )
            )
        if self.level % FAST_ENEMY_LEVEL_INTERVAL == 0:
            self.enemies.append(
                Enemy(
                    random.randint(20, WIDTH - 20),
                    random.randint(-1500, -100),
                    enemy_speed_for(self.level, fast=True),
                    self.assets,
                )
            )

    def spawn_boss(self):
        self.boss = Boss(WIDTH // 2, 100, self.assets)

    def advance_level(self):
        self.level += 1
        if self.level % BOSS_LEVEL_INTERVAL == 0:
            self.spawn_boss()
        else:
            self.spawn_wave()

    def spawn_power_up(self):
        power_up = PowerUp(random.randint(20, WIDTH - 20), 0, self.assets)
        # Start fully on-screen; spawning centred at y=0 put half the sprite
        # above the viewport.
        power_up.set_topleft(power_up.rect.x, 0)
        self.power_ups.append(power_up)

    def add_explosion(self, x, y):
        self.explosions.append(Explosion(x, y, self.assets))

    def fire(self, now):
        """Fire if the cooldown has elapsed. Returns True if shots were fired."""
        ship = self.spaceship
        if not ship.can_shoot(now):
            return False
        for x, y in ship.bullet_origins():
            self.bullets.append(Bullet(x, y, self.assets))
        ship.register_shot(now)
        return True

    # -- score ------------------------------------------------------------

    def record_high_score(self):
        """Promote the run's score if it is a record. Returns True if it was."""
        if self.score > self.high_score:
            self.high_score = self.score
            return True
        return False
