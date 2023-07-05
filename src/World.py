import os
import pygame
import json

from Components.physics import PhysicsComponent
from Entity.DumbBot import DumbBot
from Entity.Player.player import Player
from Components.graphics import GraphicsComponent, ExplosionGraphics, EndGraphics, PlayerGraphics
from Entity.Wall import Wall
from Entity.EndBlock import EndBlock
from Entity.Bot import Bot
from Components.KeyBoardInput import KeyBoardInput
from Camera import Camera
from Level import Level
from Entity.Particle import Particle
from Util.constants import ASSET_FILE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, ROOMS

PLAY_STATE = 0
START_MENU_STATE = 1
PAUSE_STATE = 2
GAME_OVER_STATE = 3
RESTART_STATE = 4
HEIGHT_THRESHOLD = 1320
POINTS_PER_LEVEL = 100


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
        player = Player(KeyBoardInput(), PhysicsComponent(),
                        PlayerGraphics(self.screen))
        self.addEntity(player)
        for player in self.players:
            # player.rect.center = self.start
            player.x = self.start[0]
            player.y = self.start[1]

        self.camera = Camera(760, 800)
        self.game_state = PLAY_STATE

    def createLevel(self, x, y):

        square = 40
        enemyImage = pygame.image.load(
            f'{ASSET_FILE_PATH}sprites/enemy.png').convert_alpha()
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
                    bot = Bot(DumbBot(self), PhysicsComponent(),
                              GraphicsComponent(self.screen, enemyImage))
                    bot.x, bot.y = x, y
                    self.addEntity(bot)

                x += square
            y += square
            x = square

    def loadLevel(self):

        lvl = Level((3, 3))
        lvl.createPath()

        level = lvl.generateLines(ROOMS)

        self.CurrentLevel = level
        self.entities.clear()
        self.platforms.clear()
        self.platforms.append(
            Wall(None, None, GraphicsComponent(self.screen, None), 0, 0, HEIGHT_THRESHOLD, 40))

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
        running = True
        clock = pygame.time.Clock()
        while running:
            time = clock.get_time()
            pygame.display.set_caption("{:.2f}".format(clock.get_fps()))

            key_events = []
            for e in pygame.event.get():
                key_events.append(e)

            if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_ESCAPE:
                break

            if (self.game_state == PLAY_STATE):
                if pygame.mixer.get_busy():
                    pygame.mixer.unpause()

                self.input()
                self.physics(time)
                self.camera.update(self.players)
                self.render()
                self.logic()

                if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_p:
                    self.game_state = PAUSE_STATE
                elif not len(self.players):
                    self.game_state = GAME_OVER_STATE

            elif self.game_state == PAUSE_STATE:
                if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_p:
                    self.game_state = PLAY_STATE

                pygame.mixer.pause()

            elif self.game_state == GAME_OVER_STATE:
                label = self.myfont.render(
                    "Game Over", 1, (255, 255, 255))
                self.screen.blit(
                    label, (SCREEN_WIDTH // 2 - label.get_rect().right, SCREEN_HEIGHT // 2 - label.get_rect().h))

                if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_RETURN:
                    self.game_state = RESTART_STATE

            elif self.game_state == RESTART_STATE:
                self.loadLevel()
                player = Player(KeyBoardInput(), PhysicsComponent(),
                                PlayerGraphics(self.screen))
                player.rect.center = self.start
                self.addEntity(player)
                self.score = 0
                self.game_state = PLAY_STATE

            scoreboard = self.myfont.render(
                "{:.0f}".format(self.score), 1, (255, 255, 255))
            self.screen.blit(scoreboard, (1000, 40))

            pygame.display.update()
            clock.tick(60)

    def input(self):
        for e in self.entities:
            e.handleInput()
            if e.health > 0:
                continue

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
                e.update_components(self)
            self.lag -= self.MS_PER_UPDATE

    def render(self):
        self.screen.blit(self.image, (0, 0))
        for e in self.entities:
            e.render(self.camera)

        for platform in self.platforms:
            platform.render(self.camera)

        for particles in self.particles:
            if particles.isDone:
                continue

            particles.render(self.camera)

    def logic(self):
        if len(self.players) == 0:
            return

        SURFACE = self.screen
        HEALTH_BORDER_COLOR_WHITE = (255, 255, 255)
        HEALTH_FILL_COLOR_RED = (255, 0, 0)
        BORDER_RADIUS = 2
        HEALTH_LEFT_OFFSET = 23
        HEALTH_TOP_COEFFICIENT = 0.025
        HEALTH_BOX_WIDTH = HEALTH_BOX_HEIGHT = 20

        for hitpoint in range(self.players[0].maxHealth):
            if hitpoint >= self.players[0].health:
                continue

            xPos = (HEALTH_BOX_WIDTH + hitpoint * HEALTH_LEFT_OFFSET)
            yPos = int(SCREEN_HEIGHT * HEALTH_TOP_COEFFICIENT)

            HEALTH_BAR_RECT = (xPos, yPos, HEALTH_BOX_WIDTH, HEALTH_BOX_HEIGHT)

            pygame.draw.rect(SURFACE, HEALTH_FILL_COLOR_RED, HEALTH_BAR_RECT)
            pygame.draw.rect(SURFACE, HEALTH_BORDER_COLOR_WHITE,
                             HEALTH_BAR_RECT, BORDER_RADIUS)

        # Remove players that have fallen through the map
        for player in self.players:
            if player.y < HEIGHT_THRESHOLD and player.health > 0:
                continue

            self.players.remove(player)

        # Player reached the end of the level, go to the next level
        if len(self.players) and self.end.check(self.players[0]):
            self.loadLevel()
            self.score += POINTS_PER_LEVEL
            for player in self.players:
                player.x = self.start[0]
                player.y = self.start[1]
                self.entities.append(player)

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)
