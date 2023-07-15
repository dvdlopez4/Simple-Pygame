import numpy as np

from Entity.entity import Entity
from . import Utils


class RunningState(object):
    def __init__(self):
        self.ButtonsReleased = np.zeros((200,), dtype=int)

    def handleInput(self, Entity: Entity, Input):

        if Input.Buttons[Input.Actions["Attack"]] and not self.ButtonsReleased[Input.Actions["Attack"]]:
            return Utils.get_state("Attack")

        if (not Input.Buttons[Input.Actions["Left"]] and not Input.Buttons[Input.Actions["Right"]]) and Entity.physics.isOnGround:
            return Utils.get_state("Standing")

        if (Input.Buttons[Input.Actions["Jump"]] and not self.ButtonsReleased[Input.Actions["Jump"]]) or not Entity.physics.isOnGround:
            return Utils.get_state("Jump")

        if Input.Buttons[Input.Actions["Dash"]] and not self.ButtonsReleased[Input.Actions["Dash"]]:
            return Utils.get_state("Dash")

        if Input.Buttons[Input.Actions["Left"]]:
            Entity.components["Animation"].directionFacing = -1

        if Input.Buttons[Input.Actions["Right"]]:
            Entity.components["Animation"].directionFacing = 1

        Entity.physics.velocity[0] = (
            Entity.components["Animation"].directionFacing * 150)

        self.ButtonsReleased = Input.GetButtons()
        return None

    def update(self, Entity: Entity):
        pass

    def exit(self, Entity: Entity, Input):
        pass

    def enter(self, Entity: Entity, Input):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("running")
        self.ButtonsReleased = Input.GetButtons()
