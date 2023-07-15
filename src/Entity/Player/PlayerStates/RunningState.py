import numpy as np

from Entity.entity import Entity
from . import PlayerStateManager


class RunningState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity: Entity):
        if "PlayStateManager" not in Entity.components:
            return

        play_state_manager: PlayerStateManager = Entity.components["PlayStateManager"]
        Input = Entity.input

        if Input.Buttons[play_state_manager.Actions["SPECIAL_2"]] and not self.ButtonsReleased[play_state_manager.Actions["SPECIAL_2"]]:
            return play_state_manager.get_state("Attack")

        if (not Input.Buttons[play_state_manager.Actions["RIGHT"]] and not Input.Buttons[play_state_manager.Actions["LEFT"]]) and Entity.physics.isOnGround:
            return play_state_manager.get_state("Standing")

        if (Input.Buttons[play_state_manager.Actions["JUMP"]] and not self.ButtonsReleased[play_state_manager.Actions["JUMP"]]) or not Entity.physics.isOnGround:
            return play_state_manager.get_state("Jump")

        if Input.Buttons[play_state_manager.Actions["SPECIAL_1"]] and not self.ButtonsReleased[play_state_manager.Actions["SPECIAL_1"]]:
            return play_state_manager.get_state("Dash")

        if Input.Buttons[play_state_manager.Actions["LEFT"]]:
            Entity.components["Animation"].directionFacing = -1

        if Input.Buttons[play_state_manager.Actions["RIGHT"]]:
            Entity.components["Animation"].directionFacing = 1

        Entity.physics.velocity[0] = (
            Entity.components["Animation"].directionFacing * Entity.speed)

        self.ButtonsReleased = Input.GetButtons()
        return None

    def update(self, Entity: Entity):
        pass

    def exit(self, Entity: Entity):
        pass

    def enter(self, Entity: Entity):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("running")

        self.ButtonsReleased = Entity.input.GetButtons()
