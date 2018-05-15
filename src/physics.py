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
                    Entity.velocity[1] -= Entity.jump
                if dy > 0:
                    Entity.state = 0
                    Entity.velocity[1] = 0
                    Entity.rect.bottom = e.rect.top
                break

class Movement(object):
    def __init__(self, velocity, start, dest):
        self.start = start
        self.dest = dest
        self.velocity = velocity
        self.right = True


    def update(self, Entity, time):
        time /= 1000
        
        if self.right:
            
            Entity.velocity[1] = floor(self.velocity[1] * time)
            Entity.velocity[0] = floor(self.velocity[0] * time)
            Entity.rect.centerx += Entity.velocity[0]
            Entity.rect.centery += Entity.velocity[1]
            distance = sqrt((Entity.rect.centerx - self.dest[0]) ** 2 + (Entity.rect.centery - self.dest[1]) ** 2)
            if distance <= 25:
                self.right = False
        else:
            Entity.velocity[1] = ceil(-self.velocity[1] * time)
            Entity.velocity[0] = ceil(-self.velocity[0] * time)
            Entity.rect.centerx += Entity.velocity[0]
            Entity.rect.centery += Entity.velocity[1]
            distance = sqrt((Entity.rect.centerx - self.start[0]) ** 2 + (Entity.rect.centery - self.start[1]) ** 2)
            if distance <= 25:
                self.right = True

class CircularMovement(object):
    def __init__(self, radius, x, y, speed):
        self.radius = radius
        self.degree = 0
        self.speed = speed
        self.x = x
        self.y = y

    def update(self, Entity, time):

        previous = [0,0]
        previous[0] = Entity.rect.centerx
        previous[1] = Entity.rect.centery
        x = self.radius * sqrt(1 / ((tan(radians(self.degree)) ** 2) + 1))
        y = sqrt(self.radius ** 2 - x ** 2)
        
        if self.degree >= 90:
            x *= -1
        if self.degree >= 180:
            y *= -1
        if self.degree >= 270:
            x *= -1   

        if self.degree <= 360:
            self.degree += self.speed
        else:
            self.degree = 0

        x = modRound(x)
        y = modRound(y)
        Entity.rect.centerx = x + self.x
        Entity.rect.centery = y + self.y
        Entity.velocity[0] = Entity.rect.centerx - previous[0]
        Entity.velocity[1] = previous[1] - Entity.rect.centery

        Entity.velocity[0] = modRound(Entity.velocity[0])
        Entity.velocity[1] = modRound(Entity.velocity[1])

class ProjectilePhysics(object):
    def __init__(self, world):
        self.world = world
        self.flipx = False
        self.flipy = False

    def update(self, Entity, time):
        Entity.age -= 1

        Entity.rect.centerx += Entity.velocity[0]
        Entity.rect.centery += Entity.velocity[1]

        for e in self.world.entities:
            if e != Entity and e.collide and Entity.rect.colliderect(e.rect):
                self.world.entities.remove(Entity)
                break

        if Entity.age < 0:
            self.world.entities.remove(Entity)