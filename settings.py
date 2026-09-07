# settings.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Game settings
FPS = 60
SPACESHIP_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2
ENEMY_FAST_SPEED = 4
POWERUP_DURATION = 5000  # Power-up lasts 5 seconds
BOSS_HEALTH = 100

# Asset paths
SPACESHIP_IMAGE = os.path.join(BASE_DIR, "assets", "spaceship.png")
BULLET_IMAGE = os.path.join(BASE_DIR, "assets", "bullet.png")
ENEMY_IMAGE = os.path.join(BASE_DIR, "assets", "enemy.png")
ENEMY_FAST_IMAGE = os.path.join(BASE_DIR, "assets", "enemy_fast.png")
BOSS_IMAGE = os.path.join(BASE_DIR, "assets", "boss.png")
EXPLOSION_FRAMES = [
    os.path.join(BASE_DIR, "assets", f"explosion_{i}.png") for i in range(5)
]
POWERUP_IMAGE = os.path.join(BASE_DIR, "assets", "powerup.png")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "assets", "background.png")

# Sounds
BACKGROUND_MUSIC = os.path.join(BASE_DIR, "assets", "background_music.wav")
SHOOT_SOUND = os.path.join(BASE_DIR, "assets", "shoot.wav")
EXPLOSION_SOUND = os.path.join(BASE_DIR, "assets", "explosion.wav")
POWERUP_SOUND = os.path.join(BASE_DIR, "assets", "powerup.wav")

# High score file
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")
