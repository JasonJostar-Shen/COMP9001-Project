import pygame
from Utils.Setting import STATUSWIDTH, HEIGHT, WIDTH
from Class.Objects.Player import Player
from Class.Components.Button import Button  

class StatusBar:
    def __init__(self, player: Player, onPause, onFast, onRestart, onQuit):
        self.player = player
        self.width = STATUSWIDTH
        self.color = (150, 150, 0) 
        self.front = pygame.font.SysFont(None, 20)
        self.surface = pygame.Surface((self.width, HEIGHT), pygame.SRCALPHA)
        self.surface.set_alpha(200)
        self.rect = self.surface.get_rect(topleft=(WIDTH, 0))
        
        self.onPause = onPause
        self.onFast = onFast
        self.onRestart = onRestart
        self.onQuit = onQuit
        
        self.buttons = []
        button_width = self.width - 10
        button_height = 30
        button_spacing = 10
        total_buttons = 4
        start_y = HEIGHT - (button_height * total_buttons + button_spacing * (total_buttons - 1)) - 5
        
        labels = ['Pasue(P)', 'Fast(F)', 'Restart(R)', 'Quit(ESC)']
        for i in range(total_buttons):
            y = start_y + i * (button_height + button_spacing)
            btn = Button(
                x=5, y=y,
                width=button_width,
                height=button_height,
                text=labels[i],
                font=self.front,
                colorIdle=self.color,          
                colorHover=(200, 200, 0),      
                colorPressed=(100, 100, 0),    
                colorBorder=(0, 0, 0)
            )
            self.buttons.append(btn)
    
    def update(self, screen, mouse_pos, mouse_pressed):
        self.surface.fill(self.color)
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
    
    def updateText(self):
        leftTopGap = (5, 10)
        interval = 30
        texts = [
            self.front.render(f"LV: {self.player.lv}", True, (0,0,0)),
            self.front.render(f"AS: {self.player.atkSpeed/1000.0:.1f}s", True, (0,0,0)),
            self.front.render(f"ATK: {self.player.atk}", True, (0,0,0)),
            self.front.render(f"Range: {self.player.range}", True, (0,0,0)), 
            self.front.render(f"Score: {self.player.score}", True, (0,0,0)),
            self.front.render(f"Kills: {self.player.kills}", True, (0,0,0))
        ]
        for i, text in enumerate(texts):
            self.surface.blit(text, (leftTopGap[0], leftTopGap[1] + i * interval))