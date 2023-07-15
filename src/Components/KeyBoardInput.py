import pygame

from Entity.entity import Entity


class KeyBoardInput(object):

    def __init__(self):
        self.Buttons = None
        self.GetButtons = pygame.key.get_pressed

    def update(self, Entity: Entity):
        self.Buttons = self.GetButtons()
        Entity.update_component("PlayStateManager")
