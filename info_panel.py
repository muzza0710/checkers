import pygame as py

class InfoPanel:
    def __init__(self, size, pos):
        self.surf = py.Surface((size[0], size[1]))
        self.rect = self.surf.get_frect(topleft = pos)
        self.pos = py.Vector2(self.rect.x, self.rect.y)
        self.font = py.Font(None, 54)
        self.text_color = 'black'

    def draw(self, surface):
        self.surf.fill((200,200,200))
        surface.blit(self.surf, self.rect)

    def print(self, surface, text, pos= None, color= None):
        padding = py.Vector2(10,10)
        if color is None:
            color = self.text_color
        if pos is None:
            pos = self.pos + padding
        text = self.font.render(text, True, color)
        rect = text.get_frect(topleft = pos)

        surface.blit(text, rect)