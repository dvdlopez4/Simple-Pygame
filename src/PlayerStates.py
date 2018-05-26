import pygame
import numpy as np


class StandingState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((20,), dtype=int)

    def handleInput(self, Entity, Input):
        if Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]] and Entity.isOnGround:
            return JumpState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return DashState()

        if not Entity.isOnGround:
            return FallState()

        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity):
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
            return FallState()

        self.DashFrames -= 1
        return None

    def update(self, Entity):
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
        pass

    def handleInput(self, Entity, Input):
        return FallState()

    def update(self, Entity):
        Entity.velocity[1] = -350

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        pass

class FallState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((20,), dtype=int)

    def handleInput(self, Entity, Input):

        if Entity.isOnGround:
            return StandingState()

        if Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]] and Entity.canJump:
            Entity.canJump = False
            return JumpState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]] and Entity.canDash:
            return DashState()

        if not Input.Buttons[Input.Actions["Jump"]]:
            if Entity.velocity[1] < 0 and not Entity.isOnGround:
                Entity.velocity[1] *= 0.35

        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity):
        pass

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        self.ButtonsReleased = Input.GetButtons()

