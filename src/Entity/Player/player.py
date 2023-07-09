from Entity.entity import Entity
from Util.constants import ASSET_FILE_PATH
from pygame import mixer, image, transform


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

        self.SpriteSheet = image.load(
            f"{ASSET_FILE_PATH}/sprites/adventurer-Sheet.png").convert_alpha()

        # Animation Components?
        self.AnimationStates = {}
        self.frameIndex = 0
        self.initializeAnimations()
        self.Animation = self.AnimationStates["idle"]

    def initializeAnimations(self):
        runningFrames = [
            (67, 45, 20, 28),
            (116, 46, 20, 27),
            (166, 48, 20, 25),
            (217, 45, 23, 28),
            (266, 46, 20, 27),
            (316, 48, 20, 25)
        ]

        idleFrames = [
            (14, 7, 19, 29),
            (14, 7, 19, 29),
            (66, 6, 17, 30),
            (66, 6, 17, 30),
            (115, 6, 19, 30),
            (115, 6, 19, 30),
            (163, 7, 20, 29),
            (163, 7, 20, 29)
        ]

        jumpingFrames = [(117, 81, 19, 27)]
        fallingFrames = [(118, 112, 17, 31)]
        dashingFrames = [(155, 132, 34, 15)]
        attackingFrames = [
            (13, 268, 20, 27),
            (13, 268, 20, 27),
            (60, 266, 38, 29),
            (102, 274, 32, 21),
            (152, 273, 31, 22)
        ]

        self.setAnimation("idle", idleFrames)
        self.setAnimation("running", runningFrames)
        self.setAnimation("jumping", jumpingFrames)
        self.setAnimation("falling", fallingFrames)
        self.setAnimation("dashing", dashingFrames)
        self.setAnimation("attacking", attackingFrames)

    def setAnimation(self, key, frames):
        self.AnimationStates[key] = []
        for frame in frames:
            self.AnimationStates[key].append(transform.scale2x(
                self.SpriteSheet.subsurface(frame)).copy())

    def renew(self, world):
        return

    def set_center(self, center):
        self.center = center
