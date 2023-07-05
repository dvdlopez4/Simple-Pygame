from pygame import Rect


class ColliderComponent(object):

    def __init__(self, width, height):
        self.collision_rect = Rect(0, 0, width, height)
        self.collisions = []
        self.static = True

    def update(self, world):
        if self.static:
            return

        self.collisions = []
        for platform in world.platforms:
            if "collider" not in platform.components:
                continue

            colliding_component = platform.components["collider"]
            if colliding_component is None:
                continue
            if not self.collision_rect.colliderect(colliding_component.collision_rect):
                continue

            self.collisions.append(colliding_component.collision_rect)
