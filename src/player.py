from entity import *

class Player(Entity):
    """docstring for Player"""
    def __init__(self, _input, _physics, _graphics):
        super(Player, self).__init__(_input, _physics, _graphics)
        self.rect.center = 0, 0
        self.rect.w = self.rect.h = 20
        self.mass = 1
        self.ID = -1
        self.health = 150
        self.state = None
        self.canDash = True
