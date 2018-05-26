import pygame
import numpy as np


class StandingState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((20,), dtype=int)

    def handleInput(self, Entity, Input):
        if Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]:
            return JumpState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return DashState()


        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity, Input):
        pass

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        self.ButtonsReleased = Input.GetButtons()
        Entity.canDash = True
        Entity.canJump = True

class DashState(object):
    def __init__(self):
        self.DashFrames = 10
        self.velocity = [450,0]

    def handleInput(self, Entity, Input):
        if self.DashFrames <= 0:
            Entity.canDash = False
            if Entity.isOnGround:
                return StandingState()
            else:
                return JumpState()

        self.DashFrames -= 1
        return None

    def update(self, Entity, Input):
        Entity.velocity[0] = self.velocity[0]
        Entity.velocity[1] = self.velocity[1]

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        if Entity.velocity[0] >= 0:
            self.velocity = [450,0]
        else:
            self.velocity = [-450,0]

class JumpState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((20,), dtype=int)
        self.jumps = 2

    def handleInput(self, Entity, Input):
        if Entity.isOnGround:
            return StandingState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]] and Entity.canDash:
            return DashState()

        if self.jumps > 0 and Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]] and not Entity.isOnGround:
            Entity.isOnGround = True
            self.jumps -= 1

        self.ButtonsReleased = Input.GetButtons()
        return None

    def update(self, Entity, Input):
        if Entity.isOnGround:
            Entity.velocity[1] = -350

        if Entity.velocity[1] < 0 and not self.ButtonsReleased[Input.Actions["Jump"]]:
            Entity.velocity[1] *= 0.35

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        self.ButtonsReleased = Input.GetButtons()


