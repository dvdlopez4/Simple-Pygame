import numpy as np

from AssetManager import SoundManager
from Entity.entity import Entity
from . import PlayerStateManager


class JumpState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((20,), dtype=int)
        self.drag_coefficient = 0.67

    def handleInput(self, Entity: Entity):
        if "PlayStateManager" not in Entity.components:
            return

        play_state_manager: PlayerStateManager = Entity.components["PlayStateManager"]
        Input = Entity.input

        if Entity.physics.isOnGround:
            return play_state_manager.get_state("Standing")

        if Input.Buttons[play_state_manager.Actions["SPECIAL_1"]] and not self.ButtonsReleased[play_state_manager.Actions["SPECIAL_1"]] and Entity.canDash:
            return play_state_manager.get_state("Dash")

        if Input.Buttons[play_state_manager.Actions["SPECIAL_2"]] and not self.ButtonsReleased[play_state_manager.Actions["SPECIAL_2"]]:
            return play_state_manager.get_state("Attack")

        if (Input.Buttons[play_state_manager.Actions["JUMP"]] and not self.ButtonsReleased[play_state_manager.Actions["JUMP"]]) and Entity.jumps >= 1:
            SoundManager.play_sound("PLAYER_JUMP_SOUND_1")
            Entity.components["Animation"].set_animation_state("jumping")
            Entity.physics.velocity[1] = Entity.jump_force * \
                self.drag_coefficient
            Entity.jumps -= 1

        if Input.Buttons[play_state_manager.Actions["LEFT"]]:
            Entity.components["Animation"].directionFacing = -1
            Entity.physics.velocity[0] = -1 * \
                (Entity.speed * self.drag_coefficient)

        if Input.Buttons[play_state_manager.Actions["RIGHT"]]:
            Entity.components["Animation"].directionFacing = 1
            Entity.physics.velocity[0] = Entity.speed * self.drag_coefficient

        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity: Entity):

        if Entity.physics.velocity[1] > 0:
            if "Animation" in Entity.components:
                Entity.components["Animation"].set_animation_state("falling")

    def exit(self, Entity: Entity):
        pass

    def enter(self, Entity: Entity):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("jumping")

        if Entity.physics.isOnGround:
            SoundManager.play_sound("PLAYER_JUMP_SOUND_1")
            Entity.physics.velocity[1] = Entity.jump_force

        Entity.jumps -= 1

        self.ButtonsReleased = Entity.input.GetButtons()
