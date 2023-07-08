from Entity.entity import Entity


class EndBlock(Entity):
    """docstring for EndBlock"""

    def __init__(self, x, y, w, h):
        super(EndBlock, self).__init__(None, None, None)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check(self, player):
        if player.colliderect(self):
            return True

        return False
