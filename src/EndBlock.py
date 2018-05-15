from entity import *
import pygame

class EndBlock(Entity):
    """docstring for EndBlock"""
    def __init__(self, x, y, w, h):
        super(EndBlock, self).__init__(None, None, None)
        self.rect = pygame.Rect(x, y, w, h)

    def check(self, player):
        if player.rect.colliderect(self.rect):
            return True
        
        return False