import pygame
from Utils.Setting import WIDTH,HEIGHT
from Class.Components.Button import Button
import Utils.GameUtils as GU

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
        self.buttons = list[Button]
        self.options = options
        self.optionColors = [(144, 238, 144),(135, 206, 250),(160, 32, 240)]
        self.initOpitons()
    
    
    def initOpitons(self):
        boxWidth, boxHeight, interval = 180, 100, 30
        width,height = self.screen.get_size()
        initX = (width - boxWidth * len(self.options) - interval * 2)//2
        y = height // 2
        self.buttons = []
        for i, option in enumerate(self.options):
            x = initX + i * (boxWidth + interval)
            text = GU.GetOptionText(option)
            btn = Button(x,y,boxWidth,boxHeight,text,self.optionFont,colorBorder=self.optionColors[option[2]])
            self.buttons.append(btn)
            
    def draw(self):
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.overlay,(0,0))
        title = self.titleFont.render("Upgrade!",True,(255,255,255))
        titleRect = title.get_rect(center=(self.screen.get_width() // 2,self.screen.get_height()//3))
        self.screen.blit(title,titleRect)
        
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()[0]
        for btn in self.buttons:
            btn.update(mousePos,mousePressed)
            btn.draw(self.screen)
        # for i,rect in enumerate(self.buttons):
        #     hover = rect.collidepoint(mousePos)
        #     color = (200, 200, 200) if hover else (255, 255, 255)
        #     pygame.draw.rect(self.screen, color, rect, border_radius=12)
        #     box = self.optionFont.render(self.options[i], True, (0, 0, 0))
        #     boxRect = box.get_rect(center=rect.center)
        #     self.screen.blit(box,boxRect)
        pygame.display.flip()
        
    def handleEvent(self,event):
        for i, btn in enumerate(self.buttons):
            if btn.isClicked(event):
                self.selected = i
                return self.options[i]
        return None