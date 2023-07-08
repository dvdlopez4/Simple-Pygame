import os
import pygame
import json

from Components.physics import PhysicsComponent
from Entity.DumbBot import DumbBot
from Entity.Player.player import Player
from Components.graphics import GraphicsComponent, EndGraphics, PlayerGraphics
from Entity.Wall import Wall
from Entity.EndBlock import EndBlock
from Entity.Bot import Bot
from Components.KeyBoardInput import KeyBoardInput
from Camera import Camera
from Level import Level
from Util.constants import ASSET_FILE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, ROOMS

PLAY_STATE = 0
START_MENU_STATE = 1
PAUSE_STATE = 2
GAME_OVER_STATE = 3
RESTART_STATE = 4

HEIGHT_THRESHOLD = 1320
POINTS_PER_LEVEL = 100
MS_PER_UPDATE = 16

LEVEL_WIDTH = 3
LEVEL_HEIGHT = 3


class World(object):
    def __init__(self):
        self.entities = []
        self.platforms = []
        self.players = []

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.initialize_screen()
        self.get_controllers()

        self.loadAssets()
        player = Player(KeyBoardInput(), PhysicsComponent(),
                        PlayerGraphics(self.screen))
        self.addEntity(player)
        for player in self.players:
            player.set_center(self.start)

        self.game_state = PLAY_STATE
        self.clock = pygame.time.Clock()

    def get_controllers(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(
            x) for x in range(pygame.joystick.get_count())]

        for stick in self.joysticks:
            stick.init()

    def initialize_screen(self):
        self.myfont = pygame.font.SysFont("monospace", 34, bold=True)
        self.score = 0
        pygame.display.set_caption("Simple Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = Camera(760, 800)

    def createLevel(self, x, y):
        SQUARE_DIMENSION = 40
        enemyImage = pygame.image.load(
            f'{ASSET_FILE_PATH}sprites/enemy.png').convert_alpha()
        for row in self.CurrentLevel:
            for char in row:
                if char == 'w':
                    self.platforms.append(Wall(None, None, GraphicsComponent(
                        self.screen, None), x, y, SQUARE_DIMENSION, SQUARE_DIMENSION))

                if char == 'e':
                    self.end = EndBlock(
                        x, y, SQUARE_DIMENSION, SQUARE_DIMENSION)
                    self.end.graphics = EndGraphics(self.screen)
                    self.addEntity(self.end)

                if char == 's':
                    self.start = x, y

                if char == 'b':
                    bot = Bot(DumbBot(self), PhysicsComponent(),
                              GraphicsComponent(self.screen, enemyImage))
                    bot.x, bot.y = x, y
                    self.addEntity(bot)

                x += SQUARE_DIMENSION
            y += SQUARE_DIMENSION
            x = SQUARE_DIMENSION

    def loadLevel(self):

        lvl = Level((LEVEL_WIDTH, LEVEL_HEIGHT))
        lvl.createPath()

        level = lvl.generateLines(ROOMS)

        self.CurrentLevel = level
        self.entities.clear()
        self.platforms.clear()

        self.createLevel(0, 0)

    def loadAssets(self):

        f = open(f'{ASSET_FILE_PATH}/data/data.json', "r")
        self.data = json.load(f)
        f.close()

        self.loadLevel()
        rawImage = pygame.image.load(
            f'{ASSET_FILE_PATH}/background/game_background_4.png').convert()
        self.image = pygame.transform.scale(
            rawImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

        for player in self.players:
            player.set_center(self.start)

    def run(self):
        running = True
        while running:
            pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

            key_events = []
            for e in pygame.event.get():
                key_events.append(e)

            if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_ESCAPE:
                break

            if (self.game_state == PLAY_STATE):
                self.input()
                self.physics()
                self.camera.update(self.players)
                self.render()
                self.logic()

                if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_p:
                    self.game_state = PAUSE_STATE
                elif len(list(filter(lambda p: p.is_active, self.players))) == 0:
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
                for player in self.players:
                    player.set_center(self.start)
                    player.is_active = True

                self.score = 0
                self.game_state = PLAY_STATE

            scoreboard = self.myfont.render(
                "{:.0f}".format(self.score), 1, (255, 255, 255))
            self.screen.blit(scoreboard, (1000, 40))

            pygame.display.update()
            self.clock.tick(60)

    def input(self):
        for e in self.entities:
            if not e.is_active:
                continue

            e.handleInput()

    def physics(self):
        for e in self.entities:
            if not e.is_active:
                continue

            e.update(self)

    def render(self):
        self.screen.blit(self.image, (0, 0))
        for e in self.entities:
            if not e.is_active:
                continue
            e.render(self.camera)

        for platform in self.platforms:
            platform.render(self.camera)

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

            player.is_active = False

        # Player reached the end of the level, go to the next level
        if len(self.players) and self.end.check(self.players[0]):
            self.loadLevel()
            self.score += POINTS_PER_LEVEL

            for player in self.players:
                player.set_center(self.start)
                player.is_active = True

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)
