
import pygame
import time
from math import *
from physics import *
from graphics import *
from entity import *



class DumbBot(object):
    def __init__(self, world):
        self.direction = 1
        self.players = world.players
        self.state = 0

    def update(self, Entity):

        Entity.velocity[0] = 100 * self.direction
        if Entity.isOnGround:
            Entity.velocity[1] = -250
            self.direction = 1
            if Entity.rect.x > self.players[0].rect.x:
                self.direction = -1

        for player in self.players:
            if Entity.rect.colliderect(player.rect):
                player.health -= 10
                time.sleep(0.25)
                break
