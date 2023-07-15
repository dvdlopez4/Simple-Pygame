from Util.constants import ASSET_FILE_PATH
from pygame import image, transform, Rect


class PlayerAnimationComponent(object):
    def __init__(self):
        self.SpriteSheet = image.load(
            f"{ASSET_FILE_PATH}/sprites/adventurer-Sheet.png").convert_alpha()
        self.AnimationStates = {}
        self.frameIndex = 0
        self.initialize()
        self.Animation = self.AnimationStates["idle"]
        self.count = 0

        self.directionFacing = 1

    def get_next_frame(self, Entity, position: Rect):
        if self.frameIndex > len(self.Animation) - 1:
            self.frameIndex = 0

        animation_frame = self.Animation[self.frameIndex] if self.directionFacing > 0 else transform.flip(
            self.Animation[self.frameIndex], True, False)

        if self.count <= 0:
            self.count = 5
            self.frameIndex += 1

        self.count -= 1

        return animation_frame

    def initialize(self):
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
            (60, 266, 38, 29),
            (102, 274, 32, 21),
            (152, 273, 31, 22)
        ]

        self.add_animation("idle", idleFrames)
        self.add_animation("running", runningFrames)
        self.add_animation("jumping", jumpingFrames)
        self.add_animation("falling", fallingFrames)
        self.add_animation("dashing", dashingFrames)
        self.add_animation("attacking", attackingFrames)

    def add_animation(self, key, frames):
        self.AnimationStates[key] = []
        for frame in frames:
            self.AnimationStates[key].append(transform.scale2x(
                self.SpriteSheet.subsurface(frame)).copy())

    def set_animation_state(self, key):
        if key not in self.AnimationStates:
            return

        self.frameIndex = 0
        self.Animation = self.AnimationStates[key]

    def get_current_animation_rect(self):
        return self.Animation[self.frameIndex].get_rect()

    def is_on_last_frame(self):
        if len(self.AnimationStates) <= 0:
            return False

        return (len(self.Animation) - 1) == self.frameIndex
