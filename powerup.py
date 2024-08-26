# powerup.py

import pygame
from settings import *

class PowerUp:
    def __init__(self, x, y, assets):
        self.image = assets["powerup"]
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.y += ENEMY_SPEED

    def draw(self, win):
        win.blit(self.image, self.rect)
