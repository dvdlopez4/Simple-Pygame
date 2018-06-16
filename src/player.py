from entity import *
from DamageBlock import *

class Player(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Player, self).__init__(_input, _physics, _graphics)
        self.rect.center = 0, 0
        self.rect.w = 20
        self.rect.h = 35
        self.mass = 1
        self.ID = -1
        self.health = 8
        self.maxHealth = 8
        self.state = None
        self.canDash = True
        self.canJump = True
        self.invincibility = 0
        self.jumpSound = pygame.mixer.Sound("../assets/SFX_Jump_10.wav")
        self.SpriteSheet = pygame.image.load('../assets/adventurer-Sheet.png').convert_alpha()

        self.AnimationStates = {}
        self.initializeAnimations()

        self.Animation = self.AnimationStates["idle"]

    def initializeAnimations(self):

        runningFrames = [
            (67,45,20,28),
            (116,46,20,27),
            (166,48,20,25),
            (217,45,23,28),
            (266,46,20,27),
            (316,48,20,25)
        ]

        idleFrames = [
            (14,7,19,29),
            (66,6,17,30),
            (115,6,19,30),
            (163,7,20,29)
        ]

        jumpingFrames = [(117,81,19,27)]
        fallingFrames = [(118,112,17,31)]
        dashingFrames = [(155,132,34,15)]

        self.setAnimation("idle", idleFrames)
        self.setAnimation("running", runningFrames)
        self.setAnimation("jumping", jumpingFrames)
        self.setAnimation("falling", fallingFrames)
        self.setAnimation("dashing", dashingFrames)

    def setAnimation(self, key, frames):
        self.AnimationStates[key] = []
        for frame in frames:
            self.AnimationStates[key].append(pygame.transform.scale2x(self.SpriteSheet.subsurface(frame)).copy())
