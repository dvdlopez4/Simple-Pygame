import pygame
from Util.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PlayState(object):
    def __init__(self):
        pass

    def update(self, world, key_events):
        world.input()
        world.physics()
        world.camera.update(world.players)
        world.render()
        world.logic()

        if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_p:
            return PauseState()

        if len(list(filter(lambda p: p.is_active, world.players))) == 0:
            return GameOverState()

        return None


class PauseState(object):
    def __init__(self):
        pass

    def update(self, world, key_events):
        if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_p:
            return PlayState()

        pygame.mixer.pause()

        return None


class GameOverState(object):
    def __init__(self):
        pass

    def update(self, world, key_events):
        label = world.myfont.render(
            "Game Over", 1, (255, 255, 255))
        world.screen.blit(
            label, (SCREEN_WIDTH // 2 - label.get_rect().right, SCREEN_HEIGHT // 2 - label.get_rect().h))

        if len(key_events) > 0 and key_events[0].type == pygame.KEYDOWN and key_events[0].key == pygame.K_RETURN:
            return RestartState()

        return None


class RestartState(object):
    def __init__(self):
        pass

    def update(self, world, key_events):
        world.loadLevel()
        for player in world.players:
            player.set_center(world.start)
            player.is_active = True

        world.score = 0

        return PlayState()
