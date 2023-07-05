from Entity.entity import Entity
from Components.collider import ColliderComponent


class Wall(Entity):
    def __init__(self, _input, _physics, _graphics, x, y, w, h):
        super(Wall, self).__init__(_input, _physics, _graphics)
        self.x, self.y = x, y
        self.rect.x, self.rect.y, self.rect.w, self.rect.h = x, y, w, h
        self.components["collider"] = ColliderComponent(40, 40)
        self.components["collider"].collision_rect.topleft = x, y
