# settings.py

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
SPACESHIP_IMAGE = "assets/spaceship.png"
BULLET_IMAGE = "assets/bullet.png"
ENEMY_IMAGE = "assets/enemy.png"
ENEMY_FAST_IMAGE = "assets/enemy_fast.png"
BOSS_IMAGE = "assets/boss.png"
EXPLOSION_FRAMES = [f"assets/explosion_{i}.png" for i in range(5)]
POWERUP_IMAGE = "assets/powerup.png"
BACKGROUND_IMAGE = "assets/background.png"

# Sounds
BACKGROUND_MUSIC = "assets/background_music.mp3"
SHOOT_SOUND = "assets/shoot.wav"
EXPLOSION_SOUND = "assets/explosion.wav"
POWERUP_SOUND = "assets/powerup.wav"

# High score file
HIGHSCORE_FILE = "highscore.txt"
