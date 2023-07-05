from math import *


def modRound(number):
    if number > 0:
        return ceil(number)
    else:
        return floor(number)


class PhysicsComponent(object):

    def __init__(self):
        self.acceleration = [0, 980]
        self.velocity = [0, 0]
        self.mass = 0.25
        self.isOnGround = True

    def update(self, Entity, time):
        time /= 1000

        self.isOnGround = False
        if self.velocity[0] != 0:
            self.move_single_axis(Entity, self.velocity[0] * time, 0)

        if self.velocity[1] != 0:
            self.move_single_axis(Entity, 0, self.velocity[1] * time)

        self.velocity[0] += self.acceleration[0] * time * self.mass
        self.velocity[1] += self.acceleration[1] * time * self.mass
        if self.velocity[1] > 0:
            self.velocity[1] += self.acceleration[1] * time * self.mass

        self.velocity[0] *= 0.20

        if abs(self.velocity[0]) < 0.00125:
            self.velocity[0] = 0

    def move_single_axis(self, Entity, dx, dy):
        dx = modRound(dx)
        dy = modRound(dy)
        Entity.x += dx
        Entity.y += dy

        if "collider" not in Entity.components:
            return

        collider_component = Entity.components["collider"]
        if collider_component is None:
            return

        collider_component.collision_rect.centerx += dx
        collider_component.collision_rect.centery += dy

        for colliding_rect in collider_component.collisions:
            if dx > 0:
                collider_component.collision_rect.right = colliding_rect.left
            if dx < 0:
                collider_component.collision_rect.left = colliding_rect.right
            if dy < 0:
                collider_component.collision_rect.top = colliding_rect.bottom
                self.velocity[1] -= self.velocity[1]
            if dy > 0:
                self.isOnGround = True
                self.velocity[1] -= self.velocity[1]
                collider_component.collision_rect.bottom = colliding_rect.top
            break

        Entity.x = collider_component.collision_rect.x
        Entity.y = collider_component.collision_rect.y
