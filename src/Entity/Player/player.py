from Entity.entity import Entity
from Components.PlayerAnimationComponent import PlayerAnimationComponent
from Entity.Player.PlayerStates.PlayerStateManager import PlayerStateManager


class Player(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Player, self).__init__(_input, _physics, _graphics)
        self.ID = -1
        self.center = 0, 0
        self.w = 20
        self.h = 45

        # Ability Component?
        self.canDash = True
        self.jumps = self.maxJumps = 2
        self.speed = 350
        self.jump_force = -450

        # Health Related Component?
        self.health = self.maxHealth = 3
        self.invincibility = 0

        self.components["Animation"] = PlayerAnimationComponent()
        self.components["PlayStateManager"] = PlayerStateManager()
