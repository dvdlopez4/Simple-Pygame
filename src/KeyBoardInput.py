import pygame
from PlayerStates import *


class KeyBoardInput(object):

    def __init__(self):
        self.state_ = StandingState()
        self.Actions = {
            'Right': pygame.K_d, 
            'Left': pygame.K_a,
            'Jump': pygame.K_SPACE,
            'Dash': pygame.K_v,
            'Attack': pygame.K_f
        }
        self.Buttons = None
        self.GetButtons = pygame.key.get_pressed


    def update(self, Entity):
        self.Buttons = self.GetButtons()
        if Entity.invincibility:
            Entity.invincibility -= 1
        if Entity.invincibility <= 45:

            Entity.state = self.state_.handleInput(Entity, self)
            if Entity.state != None:
                self.state_.exit(Entity, self)
                self.state_ = Entity.state
                self.state_.enter(Entity, self)

            self.state_.update(Entity)