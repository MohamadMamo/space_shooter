# enemy.py

import pygame
from settings import *

class Enemy:
    def __init__(self, x, y, speed, assets):
        self.image = assets["enemy"]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, win):
        win.blit(self.image, self.rect)

class Boss:
    def __init__(self, x, y, assets):
        self.image = assets["boss"]
        self.rect = self.image.get_rect(center=(x, y))
        self.health = BOSS_HEALTH
        self.direction = 1

    def move(self):
        self.rect.x += self.direction * 3
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

    def draw(self, win):
        win.blit(self.image, self.rect)
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        pygame.draw.rect(win, RED, (self.rect.x, self.rect.bottom + 10, self.rect.width, 10))
        pygame.draw.rect(win, YELLOW, (self.rect.x, self.rect.bottom + 10, self.rect.width * (self.health / BOSS_HEALTH), 10))
