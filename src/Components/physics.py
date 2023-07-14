from math import ceil, floor

ONE_MILLISECOND = 1000


def modRound(number):
    if number > 0:
        return ceil(number)
    else:
        return floor(number)


class PhysicsComponent(object):

    def __init__(self):
        self.acceleration = [0, 980]
        self.velocity = [0, 0]
        self.mass = 1
        self.isOnGround = True
        self.world = None

    def update(self, Entity, world):
        time = world.clock.get_time() / ONE_MILLISECOND
        self.world = world

        self.isOnGround = False
        if self.velocity[0] != 0:
            self.move_single_axis(Entity, self.velocity[0] * time, 0)
        if self.velocity[1] != 0:
            self.move_single_axis(Entity, 0, self.velocity[1] * time)

        self.velocity[1] += self.acceleration[1] * time * self.mass
        self.velocity[0] *= 0.20

        if abs(self.velocity[0]) < 0.00125:
            self.velocity[0] = 0

    def move_single_axis(self, Entity, dx, dy):
        dx = modRound(dx)
        dy = modRound(dy)
        Entity.centerx += dx
        Entity.centery += dy

        for platform in self.world.platforms:
            if not Entity.colliderect(platform):
                continue

            if dx > 0:
                Entity.right = platform.left
            if dx < 0:
                Entity.left = platform.right
            if dy < 0:
                Entity.top = platform.bottom
                self.velocity[1] -= self.velocity[1]
            if dy > 0:
                self.isOnGround = True
                self.velocity[1] -= self.velocity[1]
                Entity.bottom = platform.top

            break
