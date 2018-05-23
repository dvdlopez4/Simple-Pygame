import pygame
from entity import *
from PlayerStates import *


class GamePadInput(object):

    def __init__(self):
        self.state_ = StandingState()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joysticks[0].init()

        self.Actions = {
            'Right': 7,
            'Left': 6,
            'Jump': 1,
            'Dash': 5
        }
        self.Buttons = []

    def GetButtons(self):
        buttons = []
        for button in range(self.joysticks[0].get_numbuttons()):
            buttons.append(self.joysticks[0].get_button(button))
        return buttons


    def update(self, Entity):
        self.Buttons = self.GetButtons()

        if self.Buttons[self.Actions["Left"]]: Entity.velocity[0] = -150
        if self.Buttons[self.Actions["Right"]]: Entity.velocity[0] = 150


        if self.joysticks[0].get_axis(0) < -0.25:
            Entity.velocity[0] = -150

        if self.joysticks[0].get_axis(0) > 0.25:
            Entity.velocity[0] = 150

        Entity.state = self.state_.handleInput(Entity, self)
        if Entity.state != None:
            self.state_ = Entity.state
            self.state_.enter(Entity, self)

        self.state_.update(Entity)

