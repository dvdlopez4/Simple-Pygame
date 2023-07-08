import pygame
from Entity.entity import Entity


class GraphicsComponent(object):
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image

    def update(self, Entity: Entity, camera):
        if self.image is not None:
            newImage = pygame.transform.scale(
                self.image, (Entity.w, Entity.h))
            self.screen.blit(newImage, camera.apply(Entity))
        else:
            pygame.draw.rect(self.screen, (200, 200, 240),
                             camera.apply(Entity), 0)
            if "collider" not in Entity.components:
                return

            pygame.draw.rect(self.screen, (0, 255, 0), camera.apply(
                Entity.components["collider"].collision_rect), 1)


class PlayerGraphics(object):
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 150, 255)
        self.count = 5

    def update(self, Entity, camera):
        position = camera.apply(Entity)
        if Entity.frameIndex > len(Entity.Animation) - 1:
            Entity.frameIndex = 0

        rect = Entity.Animation[Entity.frameIndex].get_rect()
        rect.center = position.center
        rect.bottom = position.bottom

        if Entity.directionFacing < 0:
            self.screen.blit(pygame.transform.flip(
                Entity.Animation[Entity.frameIndex], True, False), rect)
        else:
            self.screen.blit(Entity.Animation[Entity.frameIndex], rect)

        pygame.draw.rect(self.screen, (255, 0, 0), camera.apply(Entity), 1)

        if self.count <= 0:
            self.count = 5
            Entity.frameIndex += 1

        self.count -= 1


class ExplosionGraphics(object):
    def __init__(self, screen, image):
        self.screen = screen
        self.frame = 0
        self.explosionFrames = []
        frames = [
            (0, 0, 100, 100),
            (100, 0, 100, 100),
            (200, 0, 100, 100),
            (300, 0, 100, 100),
            (400, 0, 100, 100),
            (500, 0, 100, 100),
            (600, 0, 100, 100),
            (700, 0, 100, 100),
            (800, 0, 100, 100),
            (900, 0, 100, 100),
            (0, 100, 100, 100),
            (100, 100, 100, 100),
            (200, 100, 100, 100),
            (300, 100, 100, 100),
            (400, 100, 100, 100),
            (500, 100, 100, 100),
            (600, 100, 100, 100),
            (700, 100, 100, 100),
            (800, 100, 100, 100),
            (900, 100, 100, 100),
            (0, 200, 100, 100),
            (100, 200, 100, 100),
            (200, 200, 100, 100),
            (300, 200, 100, 100),
            (400, 200, 100, 100),
            (500, 200, 100, 100),
            (600, 200, 100, 100),
            (700, 200, 100, 100),
            (800, 200, 100, 100),
            (900, 200, 100, 100),
            (0, 300, 100, 100),
            (100, 300, 100, 100),
            (200, 300, 100, 100),
            (300, 300, 100, 100),
            (400, 300, 100, 100),
            (500, 300, 100, 100),
            (600, 300, 100, 100),
            (700, 300, 100, 100),
            (800, 300, 100, 100),
            (900, 300, 100, 100),
            (0, 400, 100, 100),
            (100, 400, 100, 100),
            (200, 400, 100, 100),
            (300, 400, 100, 100),
            (400, 400, 100, 100),
            (500, 400, 100, 100),
            (600, 400, 100, 100),
            (700, 400, 100, 100),
            (800, 400, 100, 100),
            (900, 400, 100, 100),
            (0, 500, 100, 100),
            (100, 500, 100, 100),
            (200, 500, 100, 100),
            (300, 500, 100, 100),
            (400, 500, 100, 100),
            (500, 500, 100, 100),
            (600, 500, 100, 100),
            (700, 500, 100, 100),
            (800, 500, 100, 100),
            (900, 500, 100, 100),
            (0, 600, 100, 100),
            (100, 600, 100, 100),
            (200, 600, 100, 100),
            (300, 600, 100, 100),
            (400, 600, 100, 100)
        ]
        for frame in frames:
            self.explosionFrames.append(image.subsurface(frame).copy())

    def update(self, Entity, camera):
        if self.frame != len(self.explosionFrames) - 1:
            self.screen.blit(
                self.explosionFrames[self.frame], camera.apply(Entity))
            self.frame += 1
        else:
            Entity.isDone = True


class EndGraphics(object):
    def __init__(self, screen):
        self.screen = screen

    def update(self, Entity, camera):
        pygame.draw.rect(self.screen, (255, 255, 0), camera.apply(Entity), 1)


class BotGraphics(object):
    def __init__(self, screen):
        self.screen = screen
        self.area = True
        self.red = 155

    def update(self, Entity, camera):
        pygame.draw.rect(self.screen, (200, 155, 155), camera.apply(Entity), 0)
