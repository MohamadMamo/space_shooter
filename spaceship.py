# spaceship.py

import pygame
from settings import *

class Spaceship:
    def __init__(self, x, y, assets):
        self.image = assets["spaceship"]
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.powered_up = False
        self.power_up_end_time = 0
        self.weapon_level = 1

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, win):
        win.blit(self.image, self.rect)

    def draw_health_bar(self, win):
        pygame.draw.rect(win, RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(win, GREEN, (self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5))

    def power_up(self):
        self.powered_up = True
        self.power_up_end_time = pygame.time.get_ticks() + POWERUP_DURATION

    def check_power_up(self):
        if self.powered_up and pygame.time.get_ticks() > self.power_up_end_time:
            self.powered_up = False

    def upgrade_weapon(self):
        if self.weapon_level < 3:
            self.weapon_level += 1
