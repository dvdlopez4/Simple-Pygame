import pygame

class Camera(object):
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        targetx = -target.rect.centerx + 1280 // 2
        targety = -target.rect.centery + 720 // 2
        targetx = min(0, targetx)
        targety = min(0, targety)
        targetx = max(-self.width - 1280,  targetx)
        targety = max(-self.height - 1280, targety)
        self.camera.x += (targetx - self.camera.x) * 0.025
        self.camera.y += (targety - self.camera.y) * 0.025

        # self.camera = pygame.Rect(x,y,self.width, self.height)