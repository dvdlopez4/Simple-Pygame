class Bar(object):
    def __init__(self, cTime=1, x=300, y=600, W=300):
        self.castTime = cTime * 1000
        self.progress = 0
        self.heal = False
        self.maxWidth = W
        self.height = 20
        self.bar = pygame.Rect(x,y,0,self.height)
        self.outerBar = pygame.Rect(x,y,self.maxWidth,self.height)
        self.totalTime = 0
        self.prevTime = 0
        self.curTime = 0


    def update(self, time):

        if self.heal:
            if self.progress <= 1:
                self.progress += time / self.castTime
                self.totalTime += time
                self.curTime = round(self.totalTime / 1000, 1)
                if self.curTime != self.prevTime:
                    self.prevTime = self.curTime
            else:
                self.heal = False
                return True

        else:
            self.loaded = False
            self.playing = False
            self.progress = 0.01
            self.totalTime = 0
            self.prevTime = time

        return False


    def draw(self, myfont, screen):
        self.bar.width = self.maxWidth * self.progress
        
        label = myfont.render("{}/{}".format(self.curTime, self.castTime / 1000), 1, (255,255,255))
        pygame.draw.rect(screen, (230,45,120), self.bar)
        pygame.draw.rect(screen, (255,255,255), self.outerBar, 3)
        screen.blit(label, ((self.outerBar.x) * 2, self.outerBar.y))