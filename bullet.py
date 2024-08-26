# bullet.py

import pygame
from settings import *

class Bullet:
    def __init__(self, x, y, assets):
        self.image = assets["bullet"]
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, win):
        win.blit(self.image, self.rect)
