import pygame


class GraphicsComponent(object):
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image

    def update(self, Entity, camera):
        if self.image != None:
            newImage = pygame.transform.scale(self.image, (Entity.rect.w, Entity.rect.h))
            self.screen.blit(newImage, camera.apply(Entity))
        else:
            pygame.draw.rect(self.screen, (200, 200, 240), camera.apply(Entity), 0)

class PlayerGraphics(object):
    def __init__(self, screen):
        self.screen = screen
        self.color = (255,150,255)
        self.frameIndex = 0
        self.count = 10

    def update(self, Entity, camera):
        if Entity.invincibility:
            self.color = (255,50,50)
        else:
            self.color = (255,150,255)
        position = camera.apply(Entity)
        if self.frameIndex > len(Entity.Animation) - 1:
            self.frameIndex = 0
        rect = Entity.Animation[self.frameIndex].get_rect()
        rect.center = position.center
        rect.bottom = position.bottom
        self.screen.blit(Entity.Animation[self.frameIndex], rect)
        # pygame.draw.rect(self.screen, self.color, position, 2)
        if self.count <= 0:
            self.count = 7
            self.frameIndex += 1
        self.count -= 1



class EndGraphics(object):
    def __init__(self, screen):
        self.screen = screen

    def update(self, Entity, camera):
        pygame.draw.rect(self.screen, (255,255,0), camera.apply(Entity), 1)

class BotGraphics(object):
    def __init__(self, screen):
        self.screen = screen
        self.area = True
        self.red = 155

    def update(self, Entity, camera):
        pygame.draw.rect(self.screen, (200, 155, 155), camera.apply(Entity), 0)