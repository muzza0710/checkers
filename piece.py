import pygame as py

class Piece(py.sprite.Sprite):
    def __init__(self, groups, size, pos, img, cell) -> None:
        super().__init__(groups)
        self.cell, self.pos, self.size, self.groups = cell, pos, size, groups
        self.drag_pos = None

        self.image = img
        self.resized_img = py.transform.scale(self.image, (size, size))

        self.surf = py.Surface((size, size))
        self.rect = self.surf.get_frect(topleft = pos)

    def draw(self, surface):
        surface.blit(self.resized_img, self.rect)

    def highlight(self, surface):
        py.draw.rect(surface, (0,200,0), self.rect, 2, self.size // 2 )

    def update(self):
        self.rect.topleft = self.pos
        if self.drag_pos != None:
            self.rect.center = self.drag_pos