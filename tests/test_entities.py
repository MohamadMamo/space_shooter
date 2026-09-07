# tests/test_entities.py
"""
Headless tests for the game's entity classes (spaceship, bullet, enemy,
boss, power-up, explosion). Runs with SDL's dummy video/audio drivers and
plain pygame.Surface stand-ins for the real image assets -- see
tests/conftest.py. Never imports main.py or calls utils.load_assets, since
both currently require the (missing) real asset files.
"""

import pygame

from bullet import Bullet
from enemy import Enemy, Boss
from explosion import Explosion
from powerup import PowerUp
from settings import BULLET_SPEED, ENEMY_SPEED, HEIGHT, WIDTH
from spaceship import Spaceship


# --- Spaceship -----------------------------------------------------------

def test_spaceship_starts_at_full_health_level_one(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT - 50, assets)
    assert ship.health == 100
    assert ship.weapon_level == 1
    assert ship.powered_up is False


def test_spaceship_move_updates_position(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    x0, y0 = ship.rect.x, ship.rect.y
    ship.move(5, -3)
    assert ship.rect.x == x0 + 5
    assert ship.rect.y == y0 - 3


def test_spaceship_clamped_to_left_edge(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    ship.move(-10_000, 0)
    assert ship.rect.left == 0


def test_spaceship_clamped_to_top_edge(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    ship.move(0, -10_000)
    assert ship.rect.top == 0


def test_spaceship_clamped_to_right_and_bottom_edges(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    ship.move(10_000, 10_000)
    assert ship.rect.right == WIDTH
    assert ship.rect.bottom == HEIGHT


def test_weapon_upgrade_caps_at_three(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    for _ in range(10):
        ship.upgrade_weapon()
    assert ship.weapon_level == 3


def test_power_up_sets_expiry_in_the_future(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    before = pygame.time.get_ticks()
    ship.power_up()
    assert ship.powered_up is True
    assert ship.power_up_end_time > before


def test_check_power_up_expires_after_duration(assets):
    ship = Spaceship(WIDTH // 2, HEIGHT // 2, assets)
    ship.power_up()
    assert ship.powered_up is True
    # Force expiry into the past instead of sleeping.
    ship.power_up_end_time = pygame.time.get_ticks() - 1
    ship.check_power_up()
    assert ship.powered_up is False


# --- Bullet ----------------------------------------------------------------

def test_bullet_moves_up_by_bullet_speed(assets):
    bullet = Bullet(100, 100, assets)
    y0 = bullet.rect.y
    bullet.move()
    assert bullet.rect.y == y0 - BULLET_SPEED


# --- Enemy / Boss ------------------------------------------------------------

def test_enemy_moves_down_by_its_own_speed(assets):
    enemy = Enemy(100, 100, 7, assets)
    y0 = enemy.rect.y
    enemy.move()
    assert enemy.rect.y == y0 + 7


def test_boss_starts_at_full_health(assets):
    from settings import BOSS_HEALTH
    boss = Boss(WIDTH // 2, 100, assets)
    assert boss.health == BOSS_HEALTH


def test_boss_reverses_direction_at_screen_edge(assets):
    boss = Boss(WIDTH // 2, 100, assets)
    boss.rect.x = 0
    boss.direction = 1
    assert boss.direction == 1
    # Push the boss's left edge past the boundary so move() must flip it.
    while boss.rect.left >= 0 and boss.rect.right <= WIDTH:
        boss.move()
    assert boss.direction == -1


def test_boss_draws_health_bar_without_error(assets, surface):
    boss = Boss(WIDTH // 2, 100, assets)
    boss.draw(surface)  # should not raise


# --- PowerUp -----------------------------------------------------------------

def test_powerup_falls_down(assets):
    power_up = PowerUp(100, 0, assets)
    y0 = power_up.rect.y
    power_up.move()
    assert power_up.rect.y == y0 + ENEMY_SPEED


# --- Explosion -----------------------------------------------------------------

def test_explosion_reports_not_done_on_first_draw(assets, surface):
    explosion = Explosion(100, 100, assets)
    assert explosion.draw(surface) is False


def test_explosion_reports_done_after_all_frames(assets, surface):
    explosion = Explosion(100, 100, assets)
    total_frames = len(assets["explosion"])
    result = False
    for _ in range(total_frames):
        # Force each draw call past the frame_rate threshold without sleeping.
        explosion.last_update = pygame.time.get_ticks() - (explosion.frame_rate + 1)
        result = explosion.draw(surface)
    assert result is True


# --- Bullet/Enemy collision ------------------------------------------------------

def test_bullet_hits_overlapping_enemy(assets):
    bullet = Bullet(100, 100, assets)
    enemy = Enemy(100, 100, ENEMY_SPEED, assets)
    assert bullet.rect.colliderect(enemy.rect)


def test_bullet_misses_distant_enemy(assets):
    bullet = Bullet(100, 100, assets)
    enemy = Enemy(700, 500, ENEMY_SPEED, assets)
    assert not bullet.rect.colliderect(enemy.rect)
