import numpy as np

from AssetManager import SoundManager
from Entity.entity import Entity
from .Utils import get_state


class AttackState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((20,), dtype=int)

    def handleInput(self, Entity: Entity, Input):
        if Entity.components["Animation"].is_on_last_frame():
            return get_state("Standing")

        return None

    def update(self, Entity):
        Entity.physics.velocity[1] = 0

    def exit(self, Entity: Entity, Input):
        pass

    def enter(self, Entity: Entity, Input):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("attacking")
            Entity.components["Animation"].frameIndex = 0

        SoundManager.play_sound("PLAYER_SWORD_ATTACK_SOUND")
