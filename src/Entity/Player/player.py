from Entity.entity import Entity
from Components.PlayerAnimationComponent import PlayerAnimationComponent
from Util.constants import ASSET_FILE_PATH
from pygame import mixer


class Player(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Player, self).__init__(_input, _physics, _graphics)
        self.ID = -1
        self.center = 0, 0
        self.w = 20
        self.h = 45

        # Player Components?
        self.state = None
        self.health = self.maxHealth = 3
        self.canDash = True
        self.canJump = True
        self.invincibility = 0
        self.directionFacing = 1

        # Sound Effects
        self.jumpSound = [
            mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump2_01.wav"),
            mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump_01.wav")
        ]
        self.slashSound = mixer.Sound(
            f"{ASSET_FILE_PATH}/sound/Sword_01.wav")

        self.components["Animation"] = PlayerAnimationComponent()
