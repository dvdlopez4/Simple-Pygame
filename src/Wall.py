from entity import *

class Wall(Entity):
    def __init__(self, _input, _physics, _graphics, x, y, w, h):
        super(Wall, self).__init__(_input, _physics, _graphics)
        self.rect.x, self.rect.y, self.rect.w, self.rect.h = x,y,w,h
        self.collide = True
        self.moving = False