import os
import pygame
from player import *
from physics import *
from inputs import *
from graphics import *
from math import *
from Wall import *
from entity import *
from pygame.locals import *

class World(object):
    def __init__(self):
        self.entities = []
        self.players = []
        self.lag = 0
        self.MS_PER_UPDATE = 16

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        pygame.display.set_caption("Simple Game")
        self.screen = pygame.display.set_mode((1280, 720),pygame.NOFRAME)
        myfont = pygame.font.SysFont("monospace", 34, bold=True)
        pygame.joystick.init()
        self.loadAssets()



    def loadAssets(self):

        f = open("world.data", "r")
        World_Map = f.readlines()
        f.close()
        x = y = 0
        square = 20
        rawImage = pygame.image.load('platform.png')
        for row in World_Map:
            for char in row:
                if char == 'w':
                    self.addEntity(Wall(None, None, GraphicsComponent(self.screen, rawImage),x,y,square,square))
                x += square
            y += square
            x = 0

        player = Player(InputComponent2(), PhysicsComponent(self), PlayerGraphics(self.screen))
        self.addEntity(player)

        rawImage = pygame.image.load('forest.jpg')
        self.image = pygame.transform.scale(rawImage, (1280, 720))

    def run(self):
        total = 0
        running = True
        clock = pygame.time.Clock()
        while running:
            time = clock.get_time()
            self.screen.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False

            self.input()
            self.physics(time)
            self.render()
            pygame.display.update()
            clock.tick(60)


    def input(self):
        for e in self.entities:
            e.handleInput()
    def physics(self, time):
        self.lag += time
        while self.lag >= self.MS_PER_UPDATE:
            for e in self.entities:
                e.update(time)
            self.lag -= self.MS_PER_UPDATE
    def render(self):
        self.screen.blit(self.image, (0,0))
        for e in self.entities:
            e.render()

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)