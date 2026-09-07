# tests/conftest.py
"""
Shared pytest fixtures for the headless test suite.

These tests run without a display and without the game's real image/sound
assets: SDL is forced onto its "dummy" video and audio drivers before pygame
is ever imported, and entity classes are exercised with plain pygame
Surfaces standing in for the (currently missing) PNG/WAV files declared in
settings.py.
"""

import os

# Must happen before the first `import pygame` anywhere in the test run.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def assets():
    """A dict of bare pygame.Surface stubs keyed exactly as the entity
    classes expect, standing in for the real (missing) image assets."""
    return {
        "spaceship": pygame.Surface((40, 40)),
        "bullet": pygame.Surface((5, 10)),
        "enemy": pygame.Surface((30, 30)),
        "enemy_fast": pygame.Surface((30, 30)),
        "boss": pygame.Surface((100, 60)),
        "explosion": [pygame.Surface((40, 40)) for _ in range(5)],
        "powerup": pygame.Surface((20, 20)),
        "background": pygame.Surface((800, 600)),
    }


@pytest.fixture
def surface():
    """An off-screen drawing target — no display.set_mode() required."""
    return pygame.Surface((800, 600))
