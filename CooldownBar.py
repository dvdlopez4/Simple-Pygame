class CooldownBar(object):
    def __init__(self):
        self.bar = pygame.Rect(100,550,50,0)
        self.maxHeight = 50
        self.outerBar = pygame.Rect(100,500,50,50)
        self.cdTime = 1500
        self.coolDown = False
        self.progress = 0
        self.totTime = 0

    def update(self, time):
        if self.coolDown and self.progress <= 1:
            self.progress += time / self.cdTime
            self.totTime += time
        else:
            self.coolDown = False
            self.totTime = self.cdTime / 1000
            self.progress = 1
            return True
        return False

    def draw(self, screen, myfont):
        color = (255,255,255)
        self.bar.height = self.maxHeight * -self.progress
        pygame.draw.rect(screen, (230,45,120), self.bar)
        if self.progress == 1:
            color = (230, 180, 120)
        pygame.draw.rect(screen, color, self.outerBar, 3)
        label = myfont.render("{}".format(round(self.totTime / 1000)), 1, (255,255,255))
        if self.progress != 1:
            screen.blit(label, ((self.outerBar.centerx - 14), self.outerBar.centery - 20))