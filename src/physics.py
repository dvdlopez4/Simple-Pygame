from pygame import Rect
from math import *

def modRound(number):
    if number > 0:  return ceil(number)
    else:   return floor(number)


class PhysicsComponent(object):

    def __init__(self, world):
        self.world = world
        self.acceleration = [0,980]

    def update(self, Entity, time):
        time /= 1000

        if Entity.velocity[0] != 0:
            self.move_single_axis(Entity, Entity.velocity[0] * time, 0)
        if Entity.velocity[1] != 0:
            self.move_single_axis(Entity, 0, Entity.velocity[1] * time)

        Entity.velocity[0] += self.acceleration[0] * time
        Entity.velocity[1] += self.acceleration[1] * time
        if Entity.velocity[1] > 0: Entity.velocity[1] += self.acceleration[1] * time

        Entity.velocity[0] = 0
  
    def move_single_axis(self, Entity, dx, dy):
        dx = modRound(dx)
        dy = modRound(dy)


        Entity.rect.centerx += dx
        Entity.rect.centery += dy
        for e in self.world.entities:
            if e.collide and e != Entity and Entity.rect.colliderect(e.rect):
                if dx > 0:
                    Entity.rect.right = e.rect.left
                if dx < 0:
                    Entity.rect.left = e.rect.right
                if dy < 0:
                    Entity.rect.top = e.rect.bottom
                    Entity.velocity[1] -= Entity.velocity[1]
                if dy > 0:
                    Entity.state = 0
                    Entity.velocity[1] -= Entity.velocity[1]
                    Entity.rect.bottom = e.rect.top
                break
