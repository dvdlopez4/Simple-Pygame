import pygame


class Entity(object):
    def __init__(self, _input, _physics, _graphics):
        self.x = self.y = 0
        self.components = {}
        self.input = _input
        self.physics = _physics
        self.graphics = _graphics
        self.rect = pygame.Rect(0, 0, 0, 0)

    def handleInput(self):
        if self.input != None:
            self.input.update(self)

    def update(self, time):
        if self.physics != None:
            self.physics.update(self, time)

    def render(self, camera):
        if self.graphics != None:
            self.graphics.update(self, camera)

    def update_components(self, world):
        for component in self.components:
            self.components[component].update(world)
