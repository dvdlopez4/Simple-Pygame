from pygame import Rect
from math import *


def modRound(number):
    if number > 0:
        return ceil(number)
    else:
        return floor(number)


class PhysicsComponent(object):

    def __init__(self, world):
        self.world = world
        self.acceleration = [0, 980]

    def update(self, Entity, time):
        time /= 1000

        Entity.isOnGround = False
        if Entity.velocity[0] != 0:
            self.move_single_axis(Entity, Entity.velocity[0] * time, 0)
        if Entity.velocity[1] != 0:
            self.move_single_axis(Entity, 0, Entity.velocity[1] * time)

        Entity.velocity[0] += Entity.acceleration[0] * time * Entity.mass
        Entity.velocity[1] += Entity.acceleration[1] * time * Entity.mass
        if Entity.velocity[1] > 0:
            Entity.velocity[1] += self.acceleration[1] * time * Entity.mass
        Entity.velocity[0] *= 0.20

        if abs(Entity.velocity[0]) < 0.00125:
            Entity.velocity[0] = 0

    def move_single_axis(self, Entity, dx, dy):
        dx = modRound(dx)
        dy = modRound(dy)

        Entity.rect.centerx += dx
        Entity.rect.centery += dy
        for platform in self.world.platforms:
            if platform == Entity or not Entity.rect.colliderect(platform.rect):
                continue

            if dx > 0:
                Entity.rect.right = platform.rect.left
            if dx < 0:
                Entity.rect.left = platform.rect.right
            if dy < 0:
                Entity.rect.top = platform.rect.bottom
                Entity.velocity[1] -= Entity.velocity[1]
            if dy > 0:
                Entity.isOnGround = True
                Entity.velocity[1] -= Entity.velocity[1]
                Entity.rect.bottom = platform.rect.top
            break
