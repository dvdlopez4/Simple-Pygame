from Entity.entity import Entity


class Wall(Entity):
    def __init__(self, _input, _physics, _graphics, x, y, w, h):
        super(Wall, self).__init__(_input, _physics, _graphics)
        self.x, self.y, self.w, self.h = x, y, w, h
