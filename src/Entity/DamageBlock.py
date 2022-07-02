import pygame
import time
from Entity.Bot import *

class DamageBlock(object):
    def __init__(self):
        self.rect = pygame.Rect(10,10,10,10)
        self.isVisible = False

    def update(self, world):
        for enemy in world.entities:
            if self.rect.colliderect(enemy.rect) and type(enemy) == Bot:
                enemy.health -= 30
                if enemy.velocity[1] > 0:
                    enemy.velocity[1] *= -1.50
                enemy.velocity[0] *= -2

                continue
