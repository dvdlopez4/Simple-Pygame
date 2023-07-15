import pygame


class Entity(pygame.Rect):
    def __init__(self, _input, _physics, _graphics):
        self.x = self.y = 0
        self.is_active = True

        self.components = {}
        self.input = _input
        self.physics = _physics
        self.graphics = _graphics

    def handleInput(self):
        if self.input is not None:
            self.input.update(self)

    def update(self, world):
        if self.physics is not None:
            self.physics.update(self, world)

    def render(self, camera):
        if self.graphics is not None:
            self.graphics.update(self, camera)

    def update_components(self, world):
        for component in self.components:
            self.components[component].update(world)

    def update_component(self, component_name: str):
        if component_name not in self.components:
            return

        self.components[component_name].update(self)
