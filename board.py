import pygame as py

red = (200,0,0)

class Board:
    def __init__(self, groups, rows= 8, cols = 8, cell_size = 50,) -> None:
        self.groups, self.rows, self.cols, self.cell_size = groups, rows, cols, cell_size
        self.grid = [Cell(self.cell_size, (i % rows * self.cell_size, i // cols * self.cell_size), red if ((i// cols) + (i % rows)) % 2 == 0 else 'black', self.groups) for i in range(rows * cols)]
        self.font = py.font.SysFont('arial', 16)
        

    def draw(self, surf):
        for cell in self.grid:
                surf.blit(cell.surf, cell.rect)
                # if cell.open:
                #     text = self.font.render(str(cell.pos), True, 'grey')
                #     surf.blit(text, cell.rect)


class Cell(py.sprite.Sprite):
    def __init__(self, size, pos, color, groups) -> None:
        super().__init__(groups)
        self.size, self.pos, self.color = size, pos, color
        self.open = True if self.color == 'black' else False

        self.surf = py.Surface((size, size))
        self.surf.fill(color)
        self.rect = self.surf.get_frect(topleft= self.pos)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)   

    def highlight(self, surface):
        py.draw.rect(surface, (0,200,0), self.rect, 2)
        
