import pygame
from Entity.Player.PlayerStates.Utils import get_state


class KeyBoardInput(object):

    def __init__(self):
        self.state_ = get_state("Standing")
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

        current_state = self.state_.handleInput(Entity, self)
        if current_state is not None:
            self.state_.exit(Entity, self)
            self.state_ = current_state
            self.state_.enter(Entity, self)

        self.state_.update(Entity)
