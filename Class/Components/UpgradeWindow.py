import pygame
from Utils.Setting import WIDTH,HEIGHT

class UpgradeWindow:
    def __init__(self,screen,options):
        self.bg = screen.copy()
        self.screen = screen
        self.overlay = pygame.Surface(screen.get_size(),pygame.SRCALPHA)
        self.selected = -1
        self.overlay.fill((0,0,0))
        self.overlay.set_alpha(180)
        self.titleFont = pygame.font.SysFont('arial',48)
        self.optionFont = pygame.font.SysFont('arial',20)
        self.boxs = []
        self.options = options
        self.initOpitons()
    
    
    def initOpitons(self):
        boxWidth = 180
        boxHeight = 100
        interval = 30
        width,height = self.screen.get_size()
        initX = (width - boxWidth * len(self.options) - interval * 2)//2
        y = height // 2
        self.boxs = []
        for i in range(len(self.options)):
            rect = pygame.Rect(initX + i * (boxWidth + interval),y,boxWidth,boxHeight)
            self.boxs.append(rect)
            
    def draw(self):
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.overlay,(0,0))
        title = self.titleFont.render("Upgrade!",True,(255,255,255))
        titleRect = title.get_rect(center=(self.screen.get_width() // 2,self.screen.get_height()//3))
        self.screen.blit(title,titleRect)
        
        mousePos = pygame.mouse.get_pos()
        for i,rect in enumerate(self.boxs):
            hover = rect.collidepoint(mousePos)
            color = (200, 200, 200) if hover else (255, 255, 255)
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            box = self.optionFont.render(self.options[i], True, (0, 0, 0))
            boxRect = box.get_rect(center=rect.center)
            self.screen.blit(box,boxRect)
        pygame.display.flip()
        
    def handleEvent(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.boxs):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    return i
        return None