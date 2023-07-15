from .StandingState import StandingState
from .AttackState import AttackState
from .RunningState import RunningState
from .JumpState import JumpState
from .DashState import DashState


def get_state(state_name: str):
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
