import pygame
import numpy as np
from Entity.entity import *
from Entity.Player.PlayerStates import *
from Entity.DamageBlock import *


class GamePadInput(object):

    def __init__(self, joystick):
        self.state_ = StandingState()
        self.joystick = joystick

        self.Actions = {
            'Right': 7,
            'Left': 6,
            'Jump': 1,
            'Dash': 5,
            'Attack': 2
        }
        self.Buttons = []

    def GetButtons(self):
        buttons = []
        for button in range(self.joystick.get_numbuttons()):
            buttons.append(self.joystick.get_button(button))
        return buttons

    def update(self, Entity):
        self.Buttons = self.GetButtons()

        if Entity.invincibility:
            Entity.invincibility -= 1
        if Entity.invincibility <= 45:
            if self.joystick.get_axis(0) < -0.25:
                self.Buttons[self.Actions["Left"]] = True

            if self.joystick.get_axis(0) > 0.25:
                self.Buttons[self.Actions["Right"]] = True

            Entity.state = self.state_.handleInput(Entity, self)
            if Entity.state != None:
                self.state_.exit(Entity, self)
                self.state_ = Entity.state
                self.state_.enter(Entity, self)

            self.state_.update(Entity)
