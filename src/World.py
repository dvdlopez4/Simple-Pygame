import os
import pygame
from typing import List

from Util.constants import ASSET_FILE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT
from Components.physics import PhysicsComponent
from Entity.Player.player import Player
from Components.graphics import PlayerGraphics
from Components.KeyBoardInput import KeyBoardInput
from Camera import Camera
from GameStates import PlayState
from LevelUtils import load_level


HEIGHT_THRESHOLD = 1320
POINTS_PER_LEVEL = 100
MS_PER_UPDATE = 16

LEVEL_WIDTH = 6
LEVEL_HEIGHT = 3


class World(object):
    def __init__(self):
        self.entities = []
        self.platforms = []
        self.players: List[Player] = []

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.initialize_screen()
        self.get_controllers()

        self.loadAssets()
        player = Player(KeyBoardInput(), PhysicsComponent(),
                        PlayerGraphics(self.screen))
        self.addEntity(player)
        for player in self.players:
            player.center = self.start

        self.game_state = PlayState()
        self.clock = pygame.time.Clock()

    def get_controllers(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(
            x) for x in range(pygame.joystick.get_count())]

        for stick in self.joysticks:
            stick.init()

    def initialize_screen(self):
        self.myfont = pygame.font.SysFont("monospace", 34, bold=True)
        pygame.display.set_caption("Simple Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = Camera(SCREEN_WIDTH * 1.5, HEIGHT_THRESHOLD)

    def loadAssets(self):
        self.score = 0
        rawImage = pygame.image.load(
            f'{ASSET_FILE_PATH}/background/game_background_4.png').convert()
        self.image = pygame.transform.scale(
            rawImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

        load_level(self)
        for player in self.players:
            player.center = self.start

    def run(self):
        while True:
            pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

            key_events = []
            for e in pygame.event.get():
                key_events.append(e)

            if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_ESCAPE:
                break

            current_game_state = self.game_state.update(self, key_events)
            if current_game_state is not None:
                self.game_state = current_game_state

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

        self.ui()

    def logic(self):
        if len(self.players) == 0:
            return

        for player in self.players:
            # Remove players that have fallen through the map
            if player.y >= HEIGHT_THRESHOLD:
                player.is_active = False

            if player.health <= 0:
                player.is_active = False

            # Ignore players that are inactive for any other reason
            if not player.is_active:
                continue

            # Player reached the end of the level, go to the next level
            if not self.end.check(player):
                continue

            # At least one player reached the end of the level
            load_level(self)
            self.score += POINTS_PER_LEVEL
            if "PlayStateManager" in player.components:
                player.components["PlayStateManager"].set_state(
                    player, "Standing")
            player.center = self.start
            player.is_active = True
            break

    def ui(self):
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

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)
