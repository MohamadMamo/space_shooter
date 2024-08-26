# explosion.py

import pygame
from settings import *

class Explosion:
    def __init__(self, x, y, assets):
        self.frames = assets["explosion"]
        self.rect = self.frames[0].get_rect(center=(x, y))
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # milliseconds per frame

    def draw(self, win):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                return True  # Explosion is done
        win.blit(self.frames[self.current_frame], self.rect)
        return False
