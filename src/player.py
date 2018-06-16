from entity import *
from DamageBlock import *

class Player(Entity):
    """docstring for Player"""
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
        self.running = []
        self.running.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((67,45,20,28))).copy())
        self.running.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((116,46,20,27))).copy())
        self.running.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((166,48,20,25))).copy())
        self.running.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((217,45,23,28))).copy())
        self.running.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((266,46,20,27))).copy())
        self.running.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((316,48,20,25))).copy())
        self.idle = []
        self.idle.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((14,7,19,29))).copy())
        self.idle.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((66,6,17,30))).copy())
        self.idle.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((115,6,19,30))).copy())
        self.idle.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((163,7,20,29))).copy())
        self.jumping = []
        self.jumping.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((117,81,19,27))).copy())
        self.falling = []
        self.falling.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((118,112,17,31))).copy())
        self.dashing = []
        self.dashing.append(pygame.transform.scale2x(self.SpriteSheet.subsurface((155,132,34,15))).copy())

        self.Animation = self.idle
