import pygame

from Level import Level
from Util.constants import ASSET_FILE_PATH, ROOMS
from Entity.Wall import Wall
from Entity.EndBlock import EndBlock
from Entity.Bot import Bot
from Components.graphics import GraphicsComponent, EndGraphics
from Components.physics import PhysicsComponent
from Entity.DumbBot import DumbBot


LEVEL_WIDTH = 6
LEVEL_HEIGHT = 3
SQUARE_DIMENSION = 40


def load_level(world):
    level = Level((LEVEL_HEIGHT, LEVEL_WIDTH))

    world.platforms.clear()

    level_as_text = level.generate_as_text(ROOMS)
    create_level_from_text(level_as_text, world)


def create_level_from_text(lines_of_level, world):
    enemyImage = pygame.image.load(
        f'{ASSET_FILE_PATH}sprites/enemy.png').convert_alpha()

    x = y = 0
    for row in lines_of_level:
        for char in row:
            if char == 'w':
                world.platforms.append(Wall(None, None, GraphicsComponent(
                    world.screen, None), x, y, SQUARE_DIMENSION, SQUARE_DIMENSION))

            if char == 'e':
                world.end = EndBlock(
                    x, y, SQUARE_DIMENSION, SQUARE_DIMENSION)
                world.end.graphics = EndGraphics(world.screen)
                world.addEntity(world.end)

            if char == 's':
                world.start = x, y

            if char == 'b':
                bot = Bot(DumbBot(world), PhysicsComponent(),
                          GraphicsComponent(world.screen, enemyImage))
                bot.x, bot.y = x, y
                world.addEntity(bot)

            x += SQUARE_DIMENSION
        y += SQUARE_DIMENSION
        x = SQUARE_DIMENSION
