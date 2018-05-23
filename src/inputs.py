
import pygame
import time
from math import *
from physics import *
from graphics import *
from entity import *


class InputComponent(object):

    def __init__(self):
        self.isPressed = False
        self.held = False
        self.boost = False
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joysticks[0].init()

    def update(self, Entity):
        key = pygame.key.get_pressed()
        button = self.joysticks[0].get_button(1)
        self.boost = False
        if not button:
            self.isPressed = False
            if Entity.velocity[1] < 0 and Entity.state == 1:
                Entity.velocity[1] *= 0.35

        if button and not self.isPressed:
            self.isPressed = True
            if Entity.state == 0:
                Entity.velocity[1] = Entity.jump
                Entity.state = 1
            elif Entity.state == 1:
                Entity.state = 2
                Entity.velocity[1] = -325
            else:
                pass


        if self.joysticks[0].get_axis(2) <= -0.85 and self.joysticks[0].get_axis(2) >= -1.0:
            self.boost = True

        if self.joysticks[0].get_axis(0) < -0.25:
            Entity.velocity[0] = -150
            if self.boost and Entity.velocity[0] > -280:
                Entity.velocity[0] *= 1.4

        if self.joysticks[0].get_axis(0) > 0.25:
            Entity.velocity[0] = 185
            if self.boost and Entity.velocity[0] < 280:
                Entity.velocity[0] *= 1.4


class StandingState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.releasedKeys = pygame.key.get_pressed()

    def handleInput(self, Entity, key):
        if key[pygame.K_SPACE] and not self.releasedKeys[pygame.K_SPACE] and Entity.isOnGround:
            return JumpState()

        if key[pygame.K_v] and not self.releasedKeys[pygame.K_v]:
            return DashState()

        if not Entity.isOnGround:
            return FallState()

        self.releasedKeys = pygame.key.get_pressed()

        return None

    def update(self, Entity):
        pass

    def enter(self, Entity, key):
        Entity.canDash = True

class DashState(object):
    def __init__(self, limit = -1):
        self.DashFrames = 10
        self.velocity = [350,0]
        self.limit = limit

    def handleInput(self, Entity, key):
        if self.DashFrames <= 0:
            Entity.canDash = False
            return FallState()

        self.DashFrames -= 1
        return None

    def update(self, Entity):
        Entity.velocity[0] = self.velocity[0]
        Entity.velocity[1] = self.velocity[1]

    def enter(self, Entity, key):
        if Entity.velocity[0] >= 0:
            self.velocity = [350,0]
        else:
            self.velocity = [-350,0]

class JumpState(object):
    def __init__(self):
        pass

    def handleInput(self, Entity, key):
        return FallState()

    def update(self, Entity):
        Entity.velocity[1] = -350

    def enter(self, Entity, key):
        pass

class FallState(object):
    def __init__(self):
        self.releasedKeys = pygame.key.get_pressed()

    def handleInput(self, Entity, key):
        if Entity.isOnGround:
            return StandingState()

        if key[pygame.K_v] and not self.releasedKeys[pygame.K_v] and Entity.canDash:
            return DashState()

        if not key[pygame.K_SPACE]:
            if Entity.velocity[1] < 0 and not Entity.isOnGround:
                Entity.velocity[1] *= 0.35

        self.releasedKeys = pygame.key.get_pressed()

        return None


    def update(self, Entity):
        pass

    def enter(self, Entity, key):
        pass


class InputComponent2(object):

    def __init__(self):
        self.state = 0
        self.state_ = StandingState()
        self.keyHeld = None
        self.keyReleased = None

    def update(self, Entity):
        key = pygame.key.get_pressed()

        if key[pygame.K_a]: Entity.velocity[0] = -150
        if key[pygame.K_d]: Entity.velocity[0] = 150

        Entity.state = self.state_.handleInput(Entity, key)
        if Entity.state != None:
            self.state_ = Entity.state
            self.state_.enter(Entity, key)

        self.state_.update(Entity)




class DumbBot(object):
    def __init__(self, world):
        self.direction = 1
        self.players = world.players
        self.state = 0

    def update(self, Entity):

        Entity.velocity[0] = 100 * self.direction
        if Entity.state == 0:
            Entity.velocity[1] = -250
            Entity.state = 1
            self.direction = 1
            if Entity.rect.x > self.players[0].rect.x:
                self.direction = -1

        for player in self.players:
            if Entity.rect.colliderect(player.rect):
                player.health = 0
                time.sleep(0.25)
