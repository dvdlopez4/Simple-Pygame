import os
import pygame
import json
from Components.physics import *
from Entity.DumbBot import *
from Entity.Player.player import *
from Components.graphics import *
from math import *
from Entity.Wall import *
from Entity.EndBlock import *
from Entity.Bot import *
from Components.KeyBoardInput import *
from Components.GamePadInput import *
from pygame.locals import *
from Camera import *
from Entity.Particle import *
import random
from Util.constants import ASSET_FILE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT


class Level(object):
    def __init__(self, shape):
        self.Layout = np.zeros(shape, dtype=int).tolist()

    def getDirection(self, room, size):
        if room == 0:
            direction = 1
        elif room == size:
            direction = -1
        else:
            direction = pow(-1, random.randint(0, 1))

        return direction

    def createPath(self):
        (ChooseStartState, AdjacentRoomState, NextFloorState) = (1, 2, 3)
        size = len(self.Layout[0]) - 1
        if not size:
            return 0
        height = len(self.Layout) - 1
        room = 0
        state = ChooseStartState
        floor = 0
        direction = 0
        done = False
        floorChance = 0.6
        while not done:
            roomType = "hall"
            if state == ChooseStartState:
                room = random.randint(0, size)
                direction = self.getDirection(room, size)
                state = AdjacentRoomState
                roomType = "start"
            elif state == AdjacentRoomState:
                room += direction
                if direction != 0 and ((room == 0 or room == size) or random.random() < floorChance):
                    state = NextFloorState
                    roomType = "drop"
                    if floor == height:
                        done = True
                        roomType = "end"
            elif state == NextFloorState:
                floor += 1
                direction = self.getDirection(room, size)
                state = AdjacentRoomState

            self.Layout[floor][int(room)] = roomType

    def generateLines(self, rooms):
        mapLines = []
        for floor in self.Layout:
            lines = np.zeros(len(rooms[0][0])).tolist()
            lines = list(map(lambda x: "w", lines))

            for room in floor:
                select = random.randint(0, len(rooms[room]) - 1)
                for index, line in enumerate(lines):
                    lines[index] += (rooms[room])[select][index]

            for line in lines:
                mapLines.append(line + "w")

        return mapLines


class World(object):
    def __init__(self):
        self.entities = []
        self.platforms = []
        self.players = []
        self.particles = []
        self.lag = 0
        self.MS_PER_UPDATE = 16

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.myfont = pygame.font.SysFont("monospace", 34, bold=True)
        self.score = 0
        pygame.display.set_caption("Simple Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(
            x) for x in range(pygame.joystick.get_count())]
        for stick in self.joysticks:
            stick.init()

        self.loadAssets()
        player = Player(KeyBoardInput(), PhysicsComponent(
            self), PlayerGraphics(self.screen))
        self.addEntity(player)
        for player in self.players:
            player.rect.center = self.start
        self.camera = Camera(760, 800)

    def createLevel(self, x, y):

        square = 40
        rawImage = pygame.image.load(
            f'{ASSET_FILE_PATH}background/platform.png').convert()
        enemyImage = pygame.image.load(
            f'{ASSET_FILE_PATH}sprites/enemy.png').convert_alpha()
        currentX = 0
        currentY = 0
        wallCount = 0
        for row in self.CurrentLevel:
            for char in row:
                if char == 'w':
                    self.platforms.append(Wall(None, None, GraphicsComponent(
                        self.screen, None), x, y, square, square))
                if char == 'e':
                    self.end = EndBlock(x, y, square, square)
                    self.end.graphics = EndGraphics(self.screen)
                    self.addEntity(self.end)
                if char == 's':
                    self.start = x, y
                if char == 'b':
                    bot = Bot(DumbBot(self), PhysicsComponent(self),
                              GraphicsComponent(self.screen, enemyImage))
                    bot.rect.center = x, y
                    self.addEntity(bot)
                x += square
            y += square
            x = square

    def loadLevel(self):

        lvl = Level((3, 3))
        lvl.createPath()

        rooms = {
            "hall": [
                ["       w",
                 "   www w",
                 "       w",
                 "  www  w",
                 " wwww   ",
                 " wwww   ",
                 " w      ",
                 "wwwwwwww"],
                ["        ",
                 "   w w  ",
                 "    w   ",
                 "    w   ",
                 "        ",
                 "    ww  ",
                 " w wwwww",
                 "wwwwwwww"],
                ["    w   ",
                 "   www  ",
                 "        ",
                 "www     ",
                 "     w  ",
                 "    ww  ",
                 " www w  ",
                 "wwwwwwww"],
                ["       w",
                 "  w     ",
                 "  w     ",
                 "www    w",
                 "w       ",
                 "w       ",
                 "w       ",
                 "wwwwwwww"],
                ["      ww",
                 "w     ww",
                 "        ",
                 "        ",
                 "        ",
                 "wwwww   ",
                 "    w   ",
                 "wwwwwwww"],
                ["ww      ",
                 "  w     ",
                 "        ",
                 "w ww    ",
                 "     w  ",
                 "     w  ",
                 "     w  ",
                 "wwwwwwww"],
                ["   w    ",
                 "        ",
                 "   wwwww",
                 "ww      ",
                 "  www   ",
                 "    w   ",
                 " w    w ",
                 "wwwwwwww"],
            ],
            "drop": [
                ["        ",
                 "        ",
                 "        ",
                 "        ",
                 "     b  ",
                 "        ",
                 "        ",
                 "        "],
                ["        ",
                 "        ",
                 "        ",
                 "    w   ",
                 "        ",
                 "  w    w",
                 "        ",
                 "   www  "],
                ["     b  ",
                 "   w w   ",
                 "    w   ",
                 "    w   ",
                 "   w w  ",
                 "  w   w ",
                 "        ",
                 "        "]
            ],
            0: [
                ["wwwwwwww", "wwwww   ", "wwwww   ", "wwwww   ",
                    "wwwww   ", "wwwww   ", "wwwww   ", "wwwwwwww"],
                ["    wwww", "w   w   ", "  www   ", "        ",
                    "        ", "        ", "        ", "wwwwwwww"],
                ["wwwwwwww", "wwwwwwww", "wwwwwwww", "wwwwwwww",
                    "wwwwwwww", "wwwwwwww", "wwwwwwww", "wwwwwwww"],
            ],
            "start": [["        ", "        ", "        ", "        ", "        ", " ^      ", "(e)     ", "wwwwwwww"]],
            "end": [["        ", "        ", "        ", "        ", "        ", " ^      ", "(s)     ", "wwwwwwww"]]
        }
        level = lvl.generateLines(rooms)

        self.CurrentLevel = level
        self.entities.clear()
        self.platforms.clear()
        self.platforms.append(
            Wall(None, None, GraphicsComponent(self.screen, None), 0, 0, 1320, 40))

        self.createLevel(0, 0)

    def loadAssets(self):
        f = open(f'{ASSET_FILE_PATH}/data/data.json', "r")
        self.data = json.load(f)
        f.close()

        self.loadLevel()
        self.explosion = pygame.image.load(
            f'{ASSET_FILE_PATH}/sprites/spritesheet.png').convert_alpha()
        rawImage = pygame.image.load(
            f'{ASSET_FILE_PATH}/background/game_background_4.png').convert()
        self.image = pygame.transform.scale(
            rawImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        total = 0
        running = True
        paused = False
        clock = pygame.time.Clock()
        while running:
            time = clock.get_time()
            pygame.display.set_caption("{:.2f}".format(clock.get_fps()))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                    paused = not paused
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    if GameOver:
                        self.loadLevel()
                        player = Player(KeyBoardInput(), PhysicsComponent(
                            self), PlayerGraphics(self.screen))
                        player.rect.center = self.start
                        self.addEntity(player)
                        GameOver = False
                        self.score = 0

            if len(self.players) and self.end.check(self.players[0]):
                self.loadLevel()
                self.score += 100
                for player in self.players:
                    player.rect.center = self.start
                    self.entities.append(player)

            if not paused:
                if pygame.mixer.get_busy():
                    pygame.mixer.unpause()
                for particle in self.particles:
                    if particle.isDone:
                        self.particles.remove(particle)
                self.input()
                self.physics(time)
                self.camera.update(self.players)
                self.render()
            else:
                pygame.mixer.pause()

            for player in self.players:
                if player.rect.y > 1320 or player.health <= 0:
                    self.players.remove(player)

            if not len(self.players):
                label = self.myfont.render("Game Over", 1, (255, 255, 255))
                self.screen.blit(
                    label, (SCREEN_WIDTH // 2 - label.get_rect().right, SCREEN_HEIGHT // 2 - label.get_rect().h))
                GameOver = True
            scoreboard = self.myfont.render(
                "{:.0f}".format(self.score), 1, (255, 255, 255))
            self.screen.blit(scoreboard, (1000, 40))

            pygame.display.update()
            clock.tick(60)

    def input(self):
        for e in self.entities:
            e.handleInput()
            if e.health <= 0:
                explosion = Particle(None, None, ExplosionGraphics(
                    self.screen, self.explosion))
                explosion.rect = e.rect
                explosion.centerx = e.rect.centerx - 100
                self.entities.remove(e)
                self.particles.append(explosion)
        for player in self.players:
            player.renew(self)

    def physics(self, time):
        self.lag += time
        while self.lag >= self.MS_PER_UPDATE:
            for e in self.entities:
                e.update(time)
            self.lag -= self.MS_PER_UPDATE

    def render(self):
        self.screen.blit(self.image, (0, 0))
        for e in self.entities:
            e.render(self.camera)
        for platform in self.platforms:
            platform.render(self.camera)
        for particles in self.particles:
            particles.render(self.camera)

        if len(self.players):
            for hitpoint in range(self.players[0].maxHealth):
                if hitpoint + 1 <= self.players[0].health:
                    pygame.draw.rect(
                        self.screen, (255, 0, 0), (20 + hitpoint * 23, int(SCREEN_HEIGHT * 0.025), 20, 20))
                pygame.draw.rect(self.screen, (255, 255, 255), (20 +
                                 hitpoint * 23, int(SCREEN_HEIGHT * 0.025), 20, 20), 2)

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)
