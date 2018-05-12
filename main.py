#! /usr/bin/env python

import os
import pygame
import pdb
from player import *
from physics import *
from inputs import * 
from graphics import *
from math import *
from pygame.locals import *

class World(object):
    def __init__(self):
        self.entities = []
        self.players = []
        self.lag = 0
        self.MS_PER_UPDATE = 16

    def update(self, time):
        
        self.lag += time
        self.input()
        while self.lag >= self.MS_PER_UPDATE:

            for e in self.entities:  
                if e.physics != None:
                    e.update(time)
            self.lag -= self.MS_PER_UPDATE
        
        self.render()   
                

    def input(self):
        for e in self.entities:
            if e.input != None:
                e.handleInput()

    def render(self):
        for e in self.entities:
            if e.graphics != None:
                e.render()

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)
            print("Added a player! ID: " + repr(Entity.ID))

        self.entities.append(Entity)
                    
 
class Wall(Entity):
    def __init__(self, _input, _physics, _graphics, x, y, w, h):
        super(Wall, self).__init__(_input, _physics, _graphics)
        self.rect.x, self.rect.y, self.rect.w, self.rect.h = x,y,w,h
        self.collide = True
        self.moving = False


class Bot(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Bot, self).__init__(_input, _physics, _graphics)
        self.shootRate = 2500
        self.totalTime = 0
        self.rect.center = 450, 0
        self.rect.w, self.rect.h = 5, 5
        self.range = 150
        self.inRange = False
        self.shot = False
        

class CooldownBar(object):
    def __init__(self):
        self.bar = pygame.Rect(100,550,50,0)
        self.maxHeight = 50
        self.outerBar = pygame.Rect(100,500,50,50)
        self.cdTime = 1500
        self.coolDown = False
        self.progress = 0
        self.totTime = 0

    def update(self, time):
        if self.coolDown and self.progress <= 1:
            self.progress += time / self.cdTime
            self.totTime += time
        else:
            self.coolDown = False
            self.totTime = self.cdTime / 1000
            self.progress = 1
            return True
        return False

    def draw(self, screen, myfont):
        color = (255,255,255)
        self.bar.height = self.maxHeight * -self.progress
        pygame.draw.rect(screen, (230,45,120), self.bar)
        if self.progress == 1:
            color = (230, 180, 120)
        pygame.draw.rect(screen, color, self.outerBar, 3)
        label = myfont.render("{}".format(round(self.totTime / 1000)), 1, (255,255,255))
        if self.progress != 1:
            screen.blit(label, ((self.outerBar.centerx - 14), self.outerBar.centery - 20))

class Bar(object):
    def __init__(self, cTime=1, x=300, y=600, W=300):
        self.castTime = cTime * 1000
        self.progress = 0
        self.heal = False
        self.maxWidth = W
        self.height = 20
        self.bar = pygame.Rect(x,y,0,self.height)
        self.outerBar = pygame.Rect(x,y,self.maxWidth,self.height)
        self.totalTime = 0
        self.prevTime = 0
        self.curTime = 0


    def update(self, time):

        if self.heal:
            if self.progress <= 1:
                self.progress += time / self.castTime
                self.totalTime += time
                self.curTime = round(self.totalTime / 1000, 1)
                if self.curTime != self.prevTime:
                    self.prevTime = self.curTime
            else:
                self.heal = False
                return True

        else:
            self.loaded = False
            self.playing = False
            self.progress = 0.01
            self.totalTime = 0
            self.prevTime = time

        return False


    def draw(self, myfont, screen):
        self.bar.width = self.maxWidth * self.progress
        
        label = myfont.render("{}/{}".format(self.curTime, self.castTime / 1000), 1, (255,255,255))
        pygame.draw.rect(screen, (230,45,120), self.bar)
        pygame.draw.rect(screen, (255,255,255), self.outerBar, 3)
        screen.blit(label, ((self.outerBar.x) * 2, self.outerBar.y))

    

def main():
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Set up the display
    pygame.display.set_caption("Get to the red square!")
    screen = pygame.display.set_mode((1280, 720),pygame.NOFRAME)
    myfont = pygame.font.SysFont("monospace", 34, bold=True)
    pygame.joystick.init()

    clock = pygame.time.Clock()
    world = World()

    # Create the player
    
   
    World_Map = [
    "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    "w                                                       ",
    "w                                                       ",
    "w   ww   ww   wwww                         w   wwwwwwwww",
    "w                    w      wwwwwwww                   w",
    "w                                                      w",
    "w                                                      w",
    "w                                                      w",
    "w                                                      w",
    "w                                                      w",
    "w                         wwwwwwwwwww                  w",
    "w                                                      w",
    "w                                                      w",
    "w                                       wwwwwwwwww     w",
    "w              wwww                                    w",
    "w                                                      w",
    "w                                                      w",
    "wwwwwwwwwwwwwwwww          wwwwwwwwwww                 w",
    "           w                                           w",
    "           w                                           w",
    "           w                                       wwwww",
    "           w                                       w   w",
    "           w                                       w   w",
    "           w                                wwwwwwwwwwww",
    "           w                                w          w",
    "           wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
    ]
    x = y = 0
    square = 20
    for row in World_Map:
        for char in row:
            if char == 'w':
                world.addEntity(Wall(None, None, GraphicsComponent(screen),x,y,square,square))
            x += square
        y += square
        x = 0

    
    player = Player(InputComponent2(), PhysicsComponent(world), PlayerGraphics(screen))
    world.addEntity(player)
    
    b1 = Bot(BotInput(world, screen), None, BotGraphics(screen))
    b1.shootRate = 2000
    b1.rect.center = 600, 250
    b1.collide = True
    b2 = Bot(BotInput(world,screen), None, BotGraphics(screen))
    b2.rect.center = 400, 250
    b2.shootRate = 1000
    b2.collide = True
    world.addEntity(b2)
    world.addEntity(b1)
    
    b2 = Bot(BotInput(world, screen), None, BotGraphics(screen))
    b2.rect.center = 900, 450
    b2.shootRate = 790
    world.addEntity(b2)
    player2 = Player(InputComponent(), PhysicsComponent(world), GraphicsComponent(screen))
    player2.collide = True
    player2.rect.center = 100, 100
    # world.addEntity(player2)

    cd = CooldownBar()
    bar = Bar(9)
    
    # world.addEntity(player2)
    total = 0
    running = True
    while running:
        time = clock.get_time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r and cd.coolDown == False:
                cd.coolDown = True
                cd.progress = 0
        
        for e in world.entities:
            if type(e) == Projectile and e.rect.colliderect(player.rect):
                player.health -= 15
                player.velocity[0] = 150
                player.velocity[1] = -75

                if player.health <= 0:
                    player.rect.center = 100, 300
                    player.health = 150
                world.entities.remove(e)
                break
                

        # Draw the scene
        screen.fill((0, 0, 0))
        world.update(time)
        cd.update(time)
        if (cd.coolDown == True):
            if total <= 3000:
                total += time
                world.MS_PER_UPDATE = 32
                cd.progress = 0
                cd.totTime = 0
            else:
                world.MS_PER_UPDATE = 16
        else:
            world.MS_PER_UPDATE = 16
            total = 0
        label = myfont.render("{}".format(player.health), 1, (255,255,255))
        bar.draw(myfont, screen)
        cd.draw(screen, myfont)
        screen.blit(label, (100,600))
        pygame.display.update()

        clock.tick(60)

if __name__ == '__main__':
    main()

