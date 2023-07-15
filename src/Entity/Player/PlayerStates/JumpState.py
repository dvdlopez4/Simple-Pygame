import numpy as np

from AssetManager import SoundManager
from Entity.entity import Entity
from .Utils import get_state


class JumpState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((20,), dtype=int)

    def handleInput(self, Entity: Entity, Input):
        if Input.Buttons[Input.Actions["Attack"]] and not self.ButtonsReleased[Input.Actions["Attack"]]:
            return get_state("Attack")

        if Entity.physics.isOnGround:
            return get_state("Standing")

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]] and Entity.canDash:
            return get_state("Dash")

        if (Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]) and Entity.jumps > 0:
            Entity.components["Animation"].set_animation_state("jumping")
            Entity.physics.velocity[1] = -450
            Entity.jumps -= 1

        if Input.Buttons[Input.Actions["Left"]]:
            Entity.components["Animation"].directionFacing = -1
            Entity.physics.velocity[0] = -150

        if Input.Buttons[Input.Actions["Right"]]:
            Entity.components["Animation"].directionFacing = 1
            Entity.physics.velocity[0] = 150

        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity: Entity):

        if Entity.physics.velocity[1] > 0:
            if "Animation" in Entity.components:
                Entity.components["Animation"].set_animation_state("falling")

    def exit(self, Entity: Entity, Input):
        pass

    def enter(self, Entity: Entity, Input):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("jumping")

        if Entity.physics.isOnGround:
            SoundManager.play_sound("PLAYER_JUMP_SOUND_1")
            Entity.physics.velocity[1] = -450
            Entity.jumps -= 1

        self.ButtonsReleased = Input.GetButtons()
