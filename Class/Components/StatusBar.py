import pygame
from Utils.Setting import STATUSWIDTH, HEIGHT, WIDTH
from Class.Objects.Player import Player
from Class.Components.Button import Button
import math

class StatusBar:
    def __init__(self, player: Player, onPause, onFast, onRestart, onQuit):
        self.player = player
        self.width = STATUSWIDTH
        self.color = (80, 80, 80) 
        self.font = pygame.font.SysFont(None, 20)
        self.fontColor = (42, 191, 206)
        self.surface = pygame.Surface((self.width, HEIGHT), pygame.SRCALPHA)
        # self.surface.set_alpha(255)
        self.rect = self.surface.get_rect(topleft=(WIDTH, 0))
        self.borderColor = (42, 191, 206)
        self.onPause = onPause
        self.onFast = onFast
        self.onRestart = onRestart
        self.onQuit = onQuit
        self.breathAlpha = 0     
        self.breath_speed = 2   
        self.breath_direction = 1
        
        self.buttons = []
        button_width = self.width - 20
        button_height = 30
        button_spacing = 10
        total_buttons = 4
        start_y = HEIGHT - (button_height * total_buttons + button_spacing * (total_buttons - 1)) - 10
        
        labels = ['Pasue(P)', 'Fast(F)', 'Restart(R)', 'Quit(ESC)']
        for i in range(total_buttons):
            y = start_y + i * (button_height + button_spacing)
            btn = Button(
                x=10, y=y,
                width=button_width,
                height=button_height,
                text=labels[i],
                font=self.font,
                colorIdle=self.color,          
                colorHover=(100, 100, 100),      
                colorPressed=(38, 38, 38),    
                colorBorder=self.borderColor,
                colorFont=self.borderColor
            )
            self.buttons.append(btn)
    
    def update(self, screen, mouse_pos, mouse_pressed):
        self.breathAlpha += self.breath_direction * self.breath_speed
        if self.breathAlpha >= 255 or self.breathAlpha <= 0:
            self.breath_direction *= -1
        self.breathAlpha = max(0, min(255, self.breathAlpha))
        
        breathBorderColor = (*self.borderColor, int(self.breathAlpha))
        
        # self.surface.fill((0, 0, 0, 0))
        self.surface.fill((*self.color, 255))
        pygame.draw.rect(self.surface, breathBorderColor, self.surface.get_rect(), width=5)
        
        self.updateText()
        
        local_x = mouse_pos[0] - self.rect.x
        local_y = mouse_pos[1] - self.rect.y
        local_pos = (local_x, local_y)
        
        for btn in self.buttons:
            btn.update(local_pos, mouse_pressed)
            if btn.pressed:
                if btn.text == 'Pasue(P)':
                    self.onPause()
                elif btn.text == 'Fast(F)':
                    self.onFast()
                elif btn.text == 'Restart(R)':
                    self.onRestart()
                elif btn.text == 'Quit(ESC)':
                    self.onQuit()
                btn.selected = not btn.selected
            btn.draw(self.surface)
        
        screen.blit(self.surface, self.rect.topleft)
        
        
        # pygame.draw.rect(self.surface, (), self.surface.get_rect(), 5)
    
    def updateText(self):
        leftTopGap = (10, 10)
        interval = 30
        texts = [
            self.font.render(f"LV: {self.player.lv}", True, self.fontColor),
            self.font.render(f"AS: {self.player.atkSpeed/1000.0:.1f}s", True, self.fontColor),
            self.font.render(f"ATK: {self.player.atk}", True, self.fontColor),
            self.font.render(f"Range: {self.player.range}", True, self.fontColor), 
            self.font.render(f"Score: {self.player.score}", True, self.fontColor),
            self.font.render(f"Kills: {self.player.kills}", True, self.fontColor),
            self.font.render(f"Bounces: {self.player.bounce}", True, self.fontColor)
        ]
        for i, text in enumerate(texts):
            self.surface.blit(text, (leftTopGap[0], leftTopGap[1] + i * interval))