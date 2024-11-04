import pygame as py

class Piece(py.sprite.Sprite):
    def __init__(self, groups, size, pos, img) -> None:
        super().__init__(groups)
        self.pos, self.size, self.groups = pos, size, groups

        self.image = img
        self.resized_img = py.transform.scale(self.image, (size, size))

        self.surf = py.Surface((size, size))
        self.rect = self.surf.get_frect(topleft = pos)

    def draw(self, surface):
        surface.blit(self.resized_img, self.rect)