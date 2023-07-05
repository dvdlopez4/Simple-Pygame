import pygame


class Camera(object):
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        rect = pygame.Rect(entity.x, entity.y, 20, 45)
        return rect.move(self.camera.topleft)

    def update(self, targets):
        if len(targets):
            targetx = 0
            targety = 0
            for target in targets:
                targetx += -target.x + 1280 // 2
                targety += -target.y + 720 // 2
            targetx //= len(targets)
            targety //= len(targets)
            targetx = min(0, targetx)
            targety = min(0, targety)
            targetx = max(-self.width + 641,  targetx)
            targety = max(-self.height + 85, targety)
            self.camera.x += (targetx - self.camera.x) * 0.025
            self.camera.y += (targety - self.camera.y) * 0.125

        # self.camera = pygame.Rect(x,y,self.width, self.height)
