import pygame

class ProgressBar:
    def __init__(self,width,height,center,maxValue,frame=1,initFull=True,title=None,
                 fillColor=(144, 238, 144),bgColor=(255, 182, 193),outlineColor=(0,0,0),fontColor=(0,0,0)):
        self.width = width
        self.height = height
        self.center = center
        self.maxValue = maxValue
        self.value = maxValue if initFull else 0
        self.isText = title != None
        if self.isText:
            self.title = title
            self.font = pygame.font.SysFont('arial',self.height)
        self.fillColor = fillColor
        self.bgColor = bgColor
        self.outlineColor = outlineColor
        self.fontColor = fontColor
        self.curValue = self.value
        self.frame = frame
        
            
    def update(self,value,pos=None):
        self.value = value
        if self.curValue > self.value:
            self.curValue -= (self.curValue - self.value)//self.frame
            self.curValue = self.curValue if self.curValue > self.value else self.value
        elif self.curValue < self.value:
            self.curValue += (self.value - self.curValue)//self.frame
            self.curValue = self.curValue if self.curValue < self.value else self.value
        if pos: self.center = pos
        
    def setValue(self,value):
        self.value = value
        self.curValue = value
    
    def draw(self,screen):
        bgRect = pygame.Rect(0,0,self.width,self.height)
        bgRect.center = self.center
        fillRect = pygame.Rect(0,0,self.width*(self.curValue/self.maxValue),self.height)
        fillRect.midleft = bgRect.midleft
        outlineRect = pygame.Rect(0,0,self.width,self.height)
        outlineRect.center = bgRect.center
        
        pygame.draw.rect(screen,self.bgColor,bgRect)
        pygame.draw.rect(screen,self.fillColor,fillRect)
        pygame.draw.rect(screen,self.outlineColor,outlineRect,1)
        if self.isText:
            text = self.font.render(f'{self.title}: {self.value}/{self.maxValue}',True,self.fontColor)
            textRect = text.get_rect()
            textRect.center = self.center
            screen.blit(text,textRect)