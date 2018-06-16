from entity import *

class Bot(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Bot, self).__init__(_input, _physics, _graphics)
        self.shootRate = 2500
        self.totalTime = 0
        self.rect.w, self.rect.h = 45,45
        self.range = 150
        self.inRange = False
        self.shot = False
        self.state = 0
        self.mass = 0.50
        self.health = 100
