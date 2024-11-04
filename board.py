import pygame as py

red = (200,0,0)

class Board:
    def __init__(self, rows= 8, cols = 8, cell_size = 50) -> None:
        self.rows, self.cols, self.cell_size = rows, cols, cell_size
        self.grid = [Cell(self.cell_size, (i // rows * self.cell_size, i % cols * self.cell_size), red if ((i// rows) + (i % cols)) % 2 == 0 else 'black') for i in range(rows * cols)]
        self.font = py.font.SysFont('arial', 16)
        

    def draw(self, surf):
        for cell in self.grid:
                surf.blit(cell.surf, cell.rect)
                # if cell.open:
                #     text = self.font.render(str(cell.pos), True, 'grey')
                #     surf.blit(text, cell.rect)


class Cell:
    def __init__(self, size, pos, color) -> None:
        self.size, self.pos, self.color = size, pos, color
        self.open = True if self.color == 'black' else False

        self.surf = py.Surface((size, size))
        self.surf.fill(color)
        self.rect = self.surf.get_frect(topleft= self.pos)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)        

    def higlight(self, surface):
        py.draw.rect(surface, (0,200,0), self.rect, 2)
        
