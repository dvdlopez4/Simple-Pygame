import pygame

class Entity(object):
    def __init__(self, _input, _physics, _graphics):
        self.input = _input
        self.physics = _physics
        self.graphics = _graphics
        self.rect = pygame.Rect(0,0,0,0)
        self.velocity = [0,0]
        self.acceleration = [0,980]
        self.mass = 0.25
        self.isOnGround = True

    def handleInput(self):
        if self.input != None: self.input.update(self)

    def update(self, time):
        if self.physics != None: self.physics.update(self, time)

    def render(self, camera):
        if self.graphics != None: self.graphics.update(self, camera)