import pygame
from PlayerStates import *


class KeyBoardInput(object):

    def __init__(self):
        self.state_ = StandingState()
        self.Actions = {
            'Right': pygame.K_d, 
            'Left': pygame.K_a,
            'Jump': pygame.K_SPACE,
            'Dash': pygame.K_v
        }
        self.Buttons = None
        self.GetButtons = pygame.key.get_pressed


    def update(self, Entity):
        self.Buttons = self.GetButtons()

        if self.Buttons[self.Actions["Left"]]: Entity.velocity[0] = -150
        if self.Buttons[self.Actions["Right"]]: Entity.velocity[0] = 150

        Entity.state = self.state_.handleInput(Entity, self)
        if Entity.state != None:
            self.state_ = Entity.state
            self.state_.enter(Entity, self)

        self.state_.update(Entity)