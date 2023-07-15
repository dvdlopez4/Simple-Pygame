import pygame

from .StandingState import StandingState
from .AttackState import AttackState
from .RunningState import RunningState
from .JumpState import JumpState
from .DashState import DashState
from Entity.entity import Entity


class PlayerStateManager(object):
    def __init__(self):
        super(PlayerStateManager, self).__init__()
        self.state = StandingState()
        self.Actions = {
            'RIGHT': pygame.K_d,
            'LEFT': pygame.K_a,
            'JUMP': pygame.K_SPACE,
            'SPECIAL_1': pygame.K_v,
            'SPECIAL_2': pygame.K_f
        }

    def get_state(self, state_name: str):
        if (state_name == ""):
            return None

        if (state_name == "Standing"):
            return StandingState()
        if (state_name == "Attack"):
            return AttackState()
        if (state_name == "Dash"):
            return DashState()
        if (state_name == "Running"):
            return RunningState()
        if (state_name == "Jump"):
            return JumpState()

    def update(self, Entity: Entity):
        if Entity.input is None:
            return

        next_state = self.state.handleInput(Entity)
        if next_state is not None:
            self.state.exit(Entity)
            self.state = next_state
            self.state.enter(Entity)

        self.state.update(Entity)
