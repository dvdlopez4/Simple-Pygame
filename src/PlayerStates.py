import pygame
import numpy as np


class StandingState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity, Input):
        if Input.Buttons[Input.Actions["Right"]] or Input.Buttons[Input.Actions["Left"]]:
            return RunningState()

        if Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]] or not Entity.isOnGround:
            return JumpState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return DashState()


        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity):
        pass

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        self.ButtonsReleased = Input.GetButtons()
        Entity.Animation = Entity.idle
        Entity.canDash = True
        Entity.canJump = True

class RunningState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity, Input):

        if (not Input.Buttons[Input.Actions["Left"]] and not Input.Buttons[Input.Actions["Right"]]) and Entity.isOnGround:
            return StandingState()

        if (Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]) or not Entity.isOnGround:
            return JumpState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return DashState()

        if Input.Buttons[Input.Actions["Left"]]: Entity.velocity[0] = -150
        if Input.Buttons[Input.Actions["Right"]]: Entity.velocity[0] = 150
        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity):
        pass

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        Entity.Animation = Entity.running
        self.ButtonsReleased = Input.GetButtons()

class DashState(object):
    def __init__(self):
        self.DashFrames = 10
        self.velocity = [450,0]

    def handleInput(self, Entity, Input):

        if Entity.invincibility:
            self.DashFrames = 0
        if self.DashFrames <= 0:
            Entity.canDash = False
            if Entity.isOnGround:
                return StandingState()
            else:
                return JumpState()
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
    def __init__(self, jumps=1):
        self.ButtonsReleased = np.zeros((20,), dtype=int)
        self.jumps = jumps

    def handleInput(self, Entity, Input):
        if Input.Buttons[Input.Actions["Left"]]: Entity.velocity[0] = -150
        if Input.Buttons[Input.Actions["Right"]]: Entity.velocity[0] = 150
        if Entity.isOnGround:
            return StandingState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]] and Entity.canDash:
            return DashState()

        if self.jumps > 0 and Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]:
            Entity.isOnGround = True
            self.jumps -= 1

        self.ButtonsReleased = Input.GetButtons()
        if Entity.velocity[1] < 0 and not self.ButtonsReleased[Input.Actions["Jump"]]:
            Entity.velocity[1] *= 0.35
        return None

    def update(self, Entity):
        if Entity.isOnGround:
            Entity.velocity[1] = -350



    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        Entity.Animation = Entity.jumping
        self.ButtonsReleased = Input.GetButtons()


