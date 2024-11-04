import pygame as py
from board import Board
from piece import Piece

class Checkers:
    def __init__(self) -> None:
        py.init()
        self.cell_size = 50
        self.win = py.Window(title='Checkers')
        self.surf = self.win.get_surface()

    def setup(self):
        self.board = Board()
        self.sprites = py.sprite.Group()
        # self.pieces = self.create_pieces(self.board.grid)

    def create_pieces(self, grid):
        for row in grid:
            for (i, j) in row:
                if (i + j) % 2 == 1:
                    if len(self.sprites) == 12:
                        break
                    else:
                        Piece(self.sprites, self.cell_size, (i * self.cell_size, j * self.cell_size))
        print(len(self.sprites))
        return self.sprites

    def run(self):
        self.running = True

        while self.running:
            # event loop
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                    

            # update


            self.surf.fill((111,111,111))
            # draw
            self.board.draw(self.surf)
            
            # for sprite in self.sprites:
            #     self.surf.blit(sprite.resized_img, sprite.rect)


            self.win.flip()

        py.quit()
        raise SystemExit