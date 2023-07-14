import random
from Entity.entity import Entity
from AssetManager import SoundManager


class DumbBot(object):
    def __init__(self, world):
        self.direction = 1
        self.players = world.players

    def update(self, Entity: Entity):
        Entity.physics.velocity[0] = 100 * self.direction
        if not Entity.physics.isOnGround:
            return

        Entity.physics.velocity[1] = -250
        if len(self.players) and abs(Entity.centerx - self.players[0].centerx) <= 300 and abs(Entity.centery - self.players[0].centery) <= 75:
            SoundManager.play_sound(f'ENEMY_SOUND_{random.randint(0, 3)}')
            difference = Entity.x - self.players[0].x
            if difference == 0:
                difference = 1
            self.direction = -difference / abs(difference)
        else:
            self.direction *= 0
            Entity.physics.velocity[1] = 0
