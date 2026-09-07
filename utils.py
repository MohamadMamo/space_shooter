# utils.py

import pygame
import os
from settings import *

def load_assets():
    assets = {
        "spaceship": pygame.image.load(SPACESHIP_IMAGE),
        "bullet": pygame.image.load(BULLET_IMAGE),
        "enemy": pygame.image.load(ENEMY_IMAGE),
        "enemy_fast": pygame.image.load(ENEMY_FAST_IMAGE),
        "boss": pygame.image.load(BOSS_IMAGE),
        "explosion": [pygame.image.load(frame) for frame in EXPLOSION_FRAMES],
        "powerup": pygame.image.load(POWERUP_IMAGE),
        "background": pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE), (WIDTH, HEIGHT)),
    }
    return assets

class _NullSound:
    """No-op stand-in for pygame.mixer.Sound, used when there is no audio
    device available. Lets call sites keep calling sounds["..."].play()
    unconditionally instead of crashing with a KeyError mid-game."""

    def play(self, *args, **kwargs):
        pass


def load_sounds():
    try:
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play(-1)  # Loop the background music
        sounds = {
            "shoot": pygame.mixer.Sound(SHOOT_SOUND),
            "explosion": pygame.mixer.Sound(EXPLOSION_SOUND),
            "powerup": pygame.mixer.Sound(POWERUP_SOUND),
        }
    except pygame.error:
        # No audio device available (e.g. a headless environment) -- fall
        # back to silent no-op sounds so the game still runs instead of
        # crashing the first time something calls sounds["..."].play().
        sounds = {
            "shoot": _NullSound(),
            "explosion": _NullSound(),
            "powerup": _NullSound(),
        }
    return sounds

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return int(f.read())
        except (ValueError, OSError):
            return 0
    return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            f.write(str(score))
    except OSError:
        pass
