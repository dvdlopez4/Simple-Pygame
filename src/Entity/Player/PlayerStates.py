import pygame
import numpy as np
import random


def is_on_the_ground(Entity):
    if Entity.physics is None:
        return True

    return Entity.physics.isOnGround


def set_ground_status(Entity, status):
    if Entity.physics is None:
        return

    Entity.physics.isOnGround = status


class StandingState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity, Input):

        if Input.Buttons[Input.Actions["Attack"]] and not self.ButtonsReleased[Input.Actions["Attack"]]:
            return AttackState()

        if Input.Buttons[Input.Actions["Right"]] or Input.Buttons[Input.Actions["Left"]]:
            return RunningState()

        if (Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]) or not is_on_the_ground(Entity):
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
        Entity.Animation = Entity.AnimationStates["idle"]
        Entity.canDash = True
        Entity.canJump = True


class RunningState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity, Input):

        if Input.Buttons[Input.Actions["Attack"]] and not self.ButtonsReleased[Input.Actions["Attack"]]:
            return AttackState()

        if (not Input.Buttons[Input.Actions["Left"]] and not Input.Buttons[Input.Actions["Right"]]) and is_on_the_ground(Entity):
            return StandingState()

        if (Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]) or not is_on_the_ground(Entity):
            return JumpState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return DashState()

        if Input.Buttons[Input.Actions["Left"]]:
            Entity.directionFacing = -1

        if Input.Buttons[Input.Actions["Right"]]:
            Entity.directionFacing = 1

        Entity.physics.velocity[0] = (Entity.directionFacing * 150)

        self.ButtonsReleased = Input.GetButtons()
        return None

    def update(self, Entity):
        pass

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        Entity.Animation = Entity.AnimationStates["running"]
        self.ButtonsReleased = Input.GetButtons()


class DashState(object):
    def __init__(self):
        self.DashFrames = 15
        self.velocity = [450, 0]

    def handleInput(self, Entity, Input):
        if Input.Buttons[Input.Actions["Attack"]]:
            return AttackState()

        if Entity.invincibility:
            self.DashFrames = 0

        if self.DashFrames <= 0:
            Entity.canDash = False
            if is_on_the_ground(Entity):
                if Input.Buttons[Input.Actions["Right"]] or Input.Buttons[Input.Actions["Left"]]:
                    return RunningState()

                return StandingState()
            else:
                return JumpState()

        self.DashFrames -= 1
        return None

    def update(self, Entity):
        Entity.physics.velocity[0] = self.velocity[0]
        Entity.physics.velocity[1] = self.velocity[1]

    def exit(self, Entity, Input):
        Entity.rect.h = 45

    def enter(self, Entity, Input):
        Entity.Animation = Entity.AnimationStates["dashing"]
        Entity.rect.centery += 25
        Entity.rect.h = 5
        self.velocity = [(Entity.directionFacing * 450), 0]


class JumpState(object):
    def __init__(self, jumps=1):
        self.ButtonsReleased = np.zeros((20,), dtype=int)
        self.jumps = jumps

    def handleInput(self, Entity, Input):
        if Input.Buttons[Input.Actions["Attack"]] and not self.ButtonsReleased[Input.Actions["Attack"]]:
            return AttackState()

        if Input.Buttons[Input.Actions["Left"]]:
            Entity.directionFacing = -1
            Entity.physics.velocity[0] = -150

        if Input.Buttons[Input.Actions["Right"]]:
            Entity.directionFacing = 1
            Entity.physics.velocity[0] = 150

        if is_on_the_ground(Entity):
            return StandingState()

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]] and Entity.canDash:
            return DashState()

        if self.jumps > 0 and Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]:
            set_ground_status(Entity, True)
            Entity.jumpSound[random.randint(0, 1)].play()
            Entity.Animation = Entity.AnimationStates["jumping"]
            self.jumps -= 1

        self.ButtonsReleased = Input.GetButtons()
        if Entity.physics.velocity[1] < 0 and not self.ButtonsReleased[Input.Actions["Jump"]]:
            Entity.physics.velocity[1] *= 0.35

        return None

    def update(self, Entity):
        if is_on_the_ground(Entity):
            Entity.jumpSound[random.randint(0, 1)].play()
            Entity.physics.velocity[1] = -450

        if Entity.physics.velocity[1] > 0:
            Entity.Animation = Entity.AnimationStates["falling"]

    def exit(self, Entity, Input):
        pass

    def enter(self, Entity, Input):
        Entity.Animation = Entity.AnimationStates["jumping"]
        self.ButtonsReleased = Input.GetButtons()


class AttackState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((20,), dtype=int)

    def handleInput(self, Entity, Input):
        if Entity.frameIndex == len(Entity.AnimationStates) - 1:
            return StandingState()

        return None

    def update(self, Entity):
        Entity.invincibility = 1
        Entity.physics.velocity[1] = 0
        if Entity.frameIndex == len(Entity.AnimationStates) - 3:
            Entity.canHurt = True
            Entity.physics.velocity[0] = (Entity.directionFacing * 50)

    def exit(self, Entity, Input):
        Entity.canHurt = False
        Entity.invincibility = 0

    def enter(self, Entity, Input):
        Entity.Animation = Entity.AnimationStates["attacking"]
        Entity.slashSound.play()
        Entity.frameIndex = 0
