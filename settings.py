# settings.py

from pathlib import Path

# Paths are anchored to this file, not the current working directory, so the
# game and its high score behave the same whatever directory you launch from.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (60, 130, 255)
CYAN = (0, 220, 220)
ORANGE = (255, 150, 40)
PURPLE = (170, 80, 230)
DARK = (10, 12, 28)

FPS = 60

# Movement is expressed in pixels per second and scaled by the frame's delta
# time, so the game plays identically whatever frame rate the machine sustains.
SPACESHIP_SPEED = 300.0
BULLET_SPEED = 420.0
ENEMY_SPEED = 120.0
ENEMY_FAST_SPEED = 240.0
POWERUP_SPEED = 150.0

# Gameplay tunables
POWERUP_DURATION = 5000       # ms a collected power-up stays active
POWERUP_SPAWN_INTERVAL = 5.0  # average seconds between power-up spawns
BOSS_HEALTH = 100
BOSS_SPEED = 180.0
BOSS_SCORE = 500
BOSS_LEVEL_INTERVAL = 5       # a boss appears every N levels
FAST_ENEMY_LEVEL_INTERVAL = 3

PLAYER_MAX_HEALTH = 100
ENEMY_CONTACT_DAMAGE = 10
BOSS_CONTACT_DAMAGE = 20
BOSS_BULLET_DAMAGE = 5
HIT_INVULNERABILITY_MS = 800   # grace period after taking a hit

ENEMY_SCORE = 10
COMBO_UPGRADE_STEP = 5         # kills per weapon upgrade
MAX_WEAPON_LEVEL = 3
ENEMIES_PER_LEVEL = 5
MAX_ENEMIES_PER_WAVE = 40      # cap so late levels stay playable

SHOOT_COOLDOWN_MS = 220
RAPID_FIRE_COOLDOWN_MS = 90    # while a power-up is active

EXPLOSION_FRAME_MS = 50

# Asset paths. Missing files fall back to art drawn at runtime (see utils.py),
# so the game is playable with an empty assets/ directory.
SPACESHIP_IMAGE = ASSETS_DIR / "spaceship.png"
BULLET_IMAGE = ASSETS_DIR / "bullet.png"
ENEMY_IMAGE = ASSETS_DIR / "enemy.png"
ENEMY_FAST_IMAGE = ASSETS_DIR / "enemy_fast.png"
BOSS_IMAGE = ASSETS_DIR / "boss.png"
EXPLOSION_FRAMES = [ASSETS_DIR / f"explosion_{i}.png" for i in range(5)]
POWERUP_IMAGE = ASSETS_DIR / "powerup.png"
BACKGROUND_IMAGE = ASSETS_DIR / "background.png"

# Sizes used for both real assets and the generated placeholders.
SPACESHIP_SIZE = (48, 48)
BULLET_SIZE = (6, 16)
ENEMY_SIZE = (40, 40)
BOSS_SIZE = (140, 90)
POWERUP_SIZE = (26, 26)
EXPLOSION_SIZE = (64, 64)

# Sounds
BACKGROUND_MUSIC = ASSETS_DIR / "background_music.mp3"
SHOOT_SOUND = ASSETS_DIR / "shoot.wav"
EXPLOSION_SOUND = ASSETS_DIR / "explosion.wav"
POWERUP_SOUND = ASSETS_DIR / "powerup.wav"

# High score file
HIGHSCORE_FILE = BASE_DIR / "highscore.txt"
