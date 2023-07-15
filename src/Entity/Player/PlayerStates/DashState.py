from Entity.entity import Entity
from . import PlayerStateManager


class DashState(object):
    def __init__(self):
        self.DashFrames = 15
        self.velocity = [750, 0]
        self.previous_player_dimensions = None

    def handleInput(self, Entity: Entity):
        if "PlayStateManager" not in Entity.components:
            return

        play_state_manager: PlayerStateManager = Entity.components["PlayStateManager"]
        Input = Entity.input

        if Input.Buttons[play_state_manager.Actions["SPECIAL_2"]]:
            return play_state_manager.get_state("Attack")

        if self.DashFrames <= 0:
            Entity.canDash = False
            if Entity.physics.isOnGround:
                if Input.Buttons[play_state_manager.Actions["RIGHT"]] or Input.Buttons[play_state_manager.Actions["LEFT"]]:
                    return play_state_manager.get_state("Running")

                return play_state_manager.get_state("Standing")
            else:
                return play_state_manager.get_state("Jump")

        self.DashFrames -= 1
        return None

    def update(self, Entity: Entity):
        Entity.physics.velocity[1] = 0
        Entity.physics.velocity[0] += self.velocity[0]

    def exit(self, Entity: Entity):
        Entity.w, Entity.h = self.previous_player_dimensions

    def enter(self, Entity: Entity):
        if "Animation" in Entity.components:
            Entity.components["Animation"].set_animation_state("dashing")

        current_animation_rect = Entity.components["Animation"].get_current_animation_rect(
        )

        self.previous_player_dimensions = (Entity.w, Entity.h)
        Entity.h = current_animation_rect.h
        Entity.w = current_animation_rect.w // 3
        Entity.y += current_animation_rect.h // 2
        self.velocity[0] *= Entity.components["Animation"].directionFacing
