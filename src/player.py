from entity import *

class Player(Entity):
    """docstring for Player"""
    def __init__(self, _input, _physics, _graphics):
        super(Player, self).__init__(_input, _physics, _graphics)
        self.acceleration = [0,980]
        self.state = 0
        self.rect.center = 100, 200
        self.rect.w = self.rect.h = 20
        self.jump = -250
        self.collide = False
        self.ID = -1
        self.health = 150
        self.mass = 1
