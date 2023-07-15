import numpy as np

from Entity.entity import Entity
from . import Utils


class StandingState(object):
    def __init__(self):
        self.isJumpPressed = False
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity: Entity, Input):

        if Input.Buttons[Input.Actions["Attack"]] and not self.ButtonsReleased[Input.Actions["Attack"]]:
            return Utils.get_state("Attack")

        if Input.Buttons[Input.Actions["Right"]] or Input.Buttons[Input.Actions["Left"]]:
            return Utils.get_state("Running")

        if (Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]) or not Entity.physics.isOnGround:
            return Utils.get_state("Jump")

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return Utils.get_state("Dash")

        self.ButtonsReleased = Input.GetButtons()

        return None

    def update(self, Entity: Entity):
        pass

    def exit(self, Entity: Entity, Input):
        pass

    def enter(self, Entity: Entity, Input):
        self.ButtonsReleased = Input.GetButtons()
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("idle")

        if Entity.physics.isOnGround:
            Entity.jumps = Entity.maxJumps

        Entity.canDash = True
