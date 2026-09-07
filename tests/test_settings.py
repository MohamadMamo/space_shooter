# tests/test_settings.py
"""Tests for the static values in settings.py. These check the *shape* of
the config, not whether the asset files it points to actually exist on
disk -- that is deliberately not asserted here (see
test_every_asset_path_is_declared_under_assets_dir)."""

from pathlib import PurePath

import settings


def test_screen_dimensions_positive():
    assert settings.WIDTH > 0
    assert settings.HEIGHT > 0


def test_speeds_are_sane():
    assert settings.BULLET_SPEED > settings.ENEMY_SPEED
    assert settings.ENEMY_FAST_SPEED > settings.ENEMY_SPEED
    assert settings.FPS > 0


def test_five_explosion_frames_declared():
    assert len(settings.EXPLOSION_FRAMES) == 5


def test_every_asset_path_is_declared_under_assets_dir():
    # String-shape check only: each configured asset path must live in an
    # "assets" directory. This deliberately does NOT check that the files
    # exist on disk -- that would fail today, before the placeholder assets
    # are generated.
    asset_paths = [
        settings.SPACESHIP_IMAGE,
        settings.BULLET_IMAGE,
        settings.ENEMY_IMAGE,
        settings.ENEMY_FAST_IMAGE,
        settings.BOSS_IMAGE,
        settings.POWERUP_IMAGE,
        settings.BACKGROUND_IMAGE,
        settings.BACKGROUND_MUSIC,
        settings.SHOOT_SOUND,
        settings.EXPLOSION_SOUND,
        settings.POWERUP_SOUND,
        *settings.EXPLOSION_FRAMES,
    ]
    assert len(asset_paths) > 0
    for path in asset_paths:
        assert "assets" in PurePath(path).parts
