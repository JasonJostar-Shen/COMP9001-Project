import pygame

class Button:
    def __init__(self, x, y, width, height, text, font,
                 colorIdle=(255, 255, 255), 
                 colorHover=(200, 200, 200), 
                 colorPressed=(160, 160, 160),
                 colorBorder=(0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.colorIdle = colorIdle
        self.colorHover = colorHover
        self.colorPressed = colorPressed
        self.colorBorder = colorBorder
        self.hover = False
        self.pressed = False
        self.selected = False

    def draw(self, surface):
        color = self.colorIdle
        if self.pressed or self.selected:
            color = self.colorPressed
        elif self.hover and not self.selected:
            color = self.colorHover


        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, self.colorBorder, self.rect, width=2, border_radius=12)
        text = self.font.render(self.text, True, (0, 0, 0))
        textRect = text.get_rect(center=self.rect.center)
        surface.blit(text, textRect)

    def update(self, mousePos, isPressed):
        self.hover = self.rect.collidepoint(mousePos)
        self.pressed = self.hover and isPressed

    def isClicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)