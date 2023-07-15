
from Entity.entity import Entity
from . import Utils


class DashState(object):
    def __init__(self):
        self.DashFrames = 15
        self.velocity = [450, 0]
        self.previous_player_dimensions = None

    def handleInput(self, Entity: Entity, Input):
        if Input.Buttons[Input.Actions["Attack"]]:
            return Utils.get_state("Attack")

        if Entity.invincibility:
            self.DashFrames = 0

        if self.DashFrames <= 0:
            Entity.canDash = False
            if Entity.physics.isOnGround:
                if Input.Buttons[Input.Actions["Right"]] or Input.Buttons[Input.Actions["Left"]]:
                    return Utils.get_state("Running")

                return Utils.get_state("Standing")
            else:
                return Utils.get_state("Jump")

        self.DashFrames -= 1
        return None

    def update(self, Entity: Entity):
        Entity.physics.velocity[0] = self.velocity[0]
        Entity.physics.velocity[1] = self.velocity[1]

    def exit(self, Entity: Entity, Input):
        Entity.w, Entity.h = self.previous_player_dimensions

    def enter(self, Entity: Entity, Input):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("dashing")

        current_animation_rect = Entity.components["Animation"].get_current_animation_rect(
        )

        self.previous_player_dimensions = (Entity.w, Entity.h)
        Entity.h = current_animation_rect.h
        Entity.w = current_animation_rect.w // 3
        Entity.y += current_animation_rect.h // 2
        self.velocity[0] *= Entity.components["Animation"].directionFacing
