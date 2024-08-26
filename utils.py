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

def load_sounds():
    sounds = {
        "background_music": pygame.mixer.music.load(BACKGROUND_MUSIC),
        "shoot": pygame.mixer.Sound(SHOOT_SOUND),
        "explosion": pygame.mixer.Sound(EXPLOSION_SOUND),
        "powerup": pygame.mixer.Sound(POWERUP_SOUND),
    }
    pygame.mixer.music.play(-1)  # Loop the background music
    return sounds

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))
