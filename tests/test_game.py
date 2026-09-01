"""Headless regression tests.

Each test pins a bug that was actually present, so a future refactor that
reintroduces one fails here rather than in front of a player.
"""

import os
import sys

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

import main as main_module  # noqa: E402
import settings  # noqa: E402
import utils  # noqa: E402
from game_state import GameState  # noqa: E402
from spaceship import Spaceship  # noqa: E402


@pytest.fixture(scope="module")
def game_env():
    win, assets, sounds, fonts = main_module.init_game(headless=True)
    yield win, assets, sounds, fonts
    pygame.quit()


@pytest.fixture
def state(game_env):
    _, assets, _, _ = game_env
    return GameState(assets)


class SilentSounds(dict):
    def __missing__(self, key):
        return utils.NullSound()


# -- assets ---------------------------------------------------------------

def test_placeholder_art_used_when_file_missing(game_env):
    """The repo ships no binary assets; the game must still have sprites."""
    _, assets, _, _ = game_env
    for key in ("spaceship", "bullet", "enemy", "enemy_fast", "boss", "powerup", "background"):
        assert isinstance(assets[key], pygame.Surface)
    assert len(assets["explosion"]) == len(settings.EXPLOSION_FRAMES)


def test_load_image_falls_back_for_missing_path(game_env):
    surface = utils.load_image(
        settings.ASSETS_DIR / "definitely-not-here.png", (20, 20), utils.draw_enemy
    )
    assert isinstance(surface, pygame.Surface)
    assert surface.get_size() == (20, 20)


def test_load_image_prefers_a_real_file(game_env, tmp_path):
    """A real asset must win over the placeholder."""
    real = tmp_path / "real.png"
    source = pygame.Surface((10, 10), pygame.SRCALPHA)
    source.fill((1, 2, 3, 255))
    pygame.image.save(source, str(real))

    loaded = utils.load_image(real, (10, 10), utils.draw_enemy)
    assert loaded.get_at((5, 5))[:3] == (1, 2, 3)


# -- the restart crash ----------------------------------------------------

def test_reset_clears_in_place_without_rebinding(state):
    """reset() must mutate the existing lists, never rebind them.

    The original bug: the restart block assigned `enemies = []` while
    `for enemy in enemies[:]` was still running, so the next remove() raised
    ValueError. Keeping identity stable is what makes that impossible.
    """
    enemies, bullets = state.enemies, state.bullets
    state.bullets.append(object())
    state.reset()
    assert state.enemies is enemies
    assert state.bullets is bullets
    assert state.bullets == []


def test_restart_during_enemy_collision_does_not_crash(game_env):
    """Drive a real game-over-then-restart through update(). Used to ValueError."""
    _, assets, _, _ = game_env
    state = GameState(assets)
    sounds = SilentSounds()

    # Park several enemies on top of the ship so the collision branch runs
    # with more of the iterated snapshot still pending.
    for enemy in state.enemies[:6]:
        enemy.set_center(*state.spaceship.rect.center)
    state.spaceship.health = settings.ENEMY_CONTACT_DAMAGE

    main_module.update(state, sounds, dt=1 / 60, now=1000)
    assert state.game_over

    state.reset()
    assert not state.game_over
    assert state.spaceship.health == settings.PLAYER_MAX_HEALTH
    # The next frame must run cleanly against the fresh lists.
    main_module.update(state, sounds, dt=1 / 60, now=2000)


def test_reset_restores_every_field(state):
    state.score, state.level, state.combo = 999, 7, 5
    state.boss = object()
    state.power_ups.append(object())
    state.explosions.append(object())
    state.reset()
    assert (state.score, state.level, state.combo) == (0, 1, 1)
    assert state.boss is None
    assert state.power_ups == [] and state.explosions == []


# -- fire rate ------------------------------------------------------------

def test_shooting_respects_cooldown(state):
    """Firing used to be uncapped: up to 3 bullets every frame."""
    assert state.fire(now=10_000) is True
    fired_once = len(state.bullets)
    assert state.fire(now=10_000) is False
    assert len(state.bullets) == fired_once

    assert state.fire(now=10_000 + settings.SHOOT_COOLDOWN_MS) is True
    assert len(state.bullets) > fired_once


def test_power_up_shortens_the_cooldown(game_env):
    """powered_up was previously set but never read by anything."""
    _, assets, _, _ = game_env
    ship = Spaceship(100, 100, assets)
    assert ship.shoot_cooldown == settings.SHOOT_COOLDOWN_MS
    ship.power_up(now=0)
    assert ship.shoot_cooldown == settings.RAPID_FIRE_COOLDOWN_MS
    ship.check_power_up(now=settings.POWERUP_DURATION + 1)
    assert ship.shoot_cooldown == settings.SHOOT_COOLDOWN_MS


# -- damage ---------------------------------------------------------------

def test_contact_damage_has_an_invulnerability_window(game_env):
    """Boss contact used to apply 20 damage every frame — instant death."""
    _, assets, _, _ = game_env
    ship = Spaceship(100, 100, assets)
    assert ship.take_damage(settings.BOSS_CONTACT_DAMAGE, now=0) is True
    assert ship.take_damage(settings.BOSS_CONTACT_DAMAGE, now=10) is False
    assert ship.health == settings.PLAYER_MAX_HEALTH - settings.BOSS_CONTACT_DAMAGE
    assert ship.take_damage(
        settings.BOSS_CONTACT_DAMAGE, now=settings.HIT_INVULNERABILITY_MS + 1
    ) is True


def test_health_never_goes_negative(game_env):
    _, assets, _, _ = game_env
    ship = Spaceship(100, 100, assets)
    ship.take_damage(10_000, now=0)
    assert ship.health == 0


# -- movement -------------------------------------------------------------

def test_movement_is_frame_rate_independent(game_env):
    """One 0.5s step must travel as far as fifty 0.01s steps."""
    _, assets, _, _ = game_env
    coarse = Spaceship(400, 300, assets)
    fine = Spaceship(400, 300, assets)

    coarse.move(1, 0, 0.5)
    for _ in range(50):
        fine.move(1, 0, 0.01)

    assert abs(coarse.rect.x - fine.rect.x) <= 1


def test_ship_stays_on_screen(game_env):
    _, assets, _, _ = game_env
    ship = Spaceship(400, 300, assets)
    for _ in range(200):
        ship.move(-1, -1, 0.05)
    assert ship.rect.left >= 0 and ship.rect.top >= 0


# -- explosions -----------------------------------------------------------

def test_explosion_finishes_without_being_drawn(state):
    """Explosions used to advance only inside draw(), so they leaked."""
    state.add_explosion(100, 100)
    explosion = state.explosions[0]
    total_ms = settings.EXPLOSION_FRAME_MS * len(explosion.frames)
    assert explosion.update(dt=(total_ms + 10) / 1000.0) is True


# -- high score -----------------------------------------------------------

def test_highscore_survives_a_corrupt_file(tmp_path, monkeypatch):
    """int(f.read()) on a corrupt file used to crash the game at startup."""
    path = tmp_path / "highscore.txt"
    path.write_text("not a number")
    monkeypatch.setattr(utils, "HIGHSCORE_FILE", path)
    assert utils.load_highscore() == 0


def test_highscore_missing_file_is_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "HIGHSCORE_FILE", tmp_path / "nope.txt")
    assert utils.load_highscore() == 0


def test_highscore_round_trip(tmp_path, monkeypatch):
    path = tmp_path / "highscore.txt"
    monkeypatch.setattr(utils, "HIGHSCORE_FILE", path)
    assert utils.save_highscore(4321) is True
    assert utils.load_highscore() == 4321


# -- waves ----------------------------------------------------------------

def test_wave_size_is_capped(state):
    """level * 5 was uncapped: level 20 spawned 100 enemies at once."""
    state.level = 50
    state.enemies.clear()
    state.spawn_wave()
    assert len(state.enemies) <= settings.MAX_ENEMIES_PER_WAVE + 1


def test_fast_enemies_use_their_own_sprite(state):
    """assets['enemy_fast'] was loaded but never used."""
    state.level = settings.FAST_ENEMY_LEVEL_INTERVAL
    state.enemies.clear()
    state.spawn_wave()
    assert any(enemy.fast for enemy in state.enemies)


def test_power_up_spawns_fully_on_screen(state):
    state.spawn_power_up()
    assert state.power_ups[-1].rect.top >= 0


# -- loop -----------------------------------------------------------------

def test_game_loop_runs_and_quits_cleanly():
    """A full loop must start, run, and tear pygame down."""
    result = main_module.main(headless=True, max_frames=120)
    assert result.level >= 1
    assert pygame.get_init() is False
