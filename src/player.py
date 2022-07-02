from entity import *
from Particle import *
from graphics import *
from constants import ASSET_FILE_PATH

class Player(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Player, self).__init__(_input, _physics, _graphics)
        self.rect.center = 0, 0
        self.rect.w = 20
        self.rect.h = 45
        self.mass = 1
        self.ID = -1
        self.health = self.maxHealth = 3
        self.state = None
        self.canDash = True
        self.canJump = True
        self.invincibility = 0
        self.jumpSound = [
            pygame.mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump2_01.wav"),
            pygame.mixer.Sound(f"{ASSET_FILE_PATH}/sound/Jump_01.wav")
        ]
        self.slashSound = pygame.mixer.Sound(f"{ASSET_FILE_PATH}/sound/Sword_01.wav")
        self.SpriteSheet = pygame.image.load(f"{ASSET_FILE_PATH}/sprites/adventurer-Sheet.png").convert_alpha()
        self.isFacingRight = True
        self.hurtRect = pygame.Rect(self.rect)
        self.canHurt = False

        self.AnimationStates = {}
        self.frameIndex = 0
        self.initializeAnimations()

        self.Animation = self.AnimationStates["idle"]
        self.hits = {}

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
            (14,7,19,29),
            (66,6,17,30),
            (66,6,17,30),
            (115,6,19,30),
            (115,6,19,30),
            (163,7,20,29),
            (163,7,20,29)
        ]

        jumpingFrames = [(117,81,19,27)]
        fallingFrames = [(118,112,17,31)]
        dashingFrames = [(155,132,34,15)]
        attackingFrames = [
            (13,268,20,27),
            (13,268,20,27),
            (60,266,38,29),
            (102,274,32,21),
            (152,273,31,22)
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
            self.AnimationStates[key].append(pygame.transform.scale2x(self.SpriteSheet.subsurface(frame)).copy())

    def renew(self, world):

        if self.canHurt:
            if self.isFacingRight:
                self.hurtRect.centerx = self.rect.centerx + 30
            else:
                self.hurtRect.centerx = self.rect.centerx - 30
            self.hurtRect.centery = self.rect.centery - 14
            self.hurtRect.w = 30
            self.hurtRect.h = 10
            for entity in world.entities:
                if entity != self and self.hurtRect.colliderect(entity.rect) and not self.hits[entity]:
                    self.hits[entity] = True
                    entity.health -= 1
                    entity.rect.left = self.hurtRect.right
                    entity.velocity[0] = 2000
                    if not self.isFacingRight:
                        entity.rect.right = self.hurtRect.left
                        entity.velocity[0] = -2000
                    entity.velocity[1] = -150
                    particle = Particle(None, None, ExplosionGraphics(world.screen, world.explosion))
                    rect = world.explosion.get_rect()
                    particle.rect.center = self.rect.centerx - 15, self.rect.centery - 50
                    world.particles.append(particle)
        else:
            for entity in world.entities:
                self.hits[entity] = False

