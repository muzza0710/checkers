import pygame as py
from board import Board
from piece import Piece

class Checkers:
    def __init__(self) -> None:
        py.init()
        self.font = py.Font(None, 20)
        self.cell_size = 75
        self.win = py.Window(title='Checkers', size=(8 * self.cell_size, 8 * self.cell_size))
        self.surf = self.win.get_surface()

        self.p1_img = py.image.load('assets\checker_white.webp').convert_alpha()
        self.p2_img = py.image.load('assets\checker_red.webp').convert_alpha()

    def setup(self):
        self.board = Board(cell_size=self.cell_size)
        self.sprites = py.sprite.Group()
        self.player1_pieces = self.create_pieces(self.board.grid, self.p1_img)
        self.player2_pieces = self.create_pieces(self.board.grid, self.p2_img, reverse=True)

    def create_pieces(self, grid, img, reverse= False):
        pieces = []
        if reverse == True: grid.reverse()
        for cell in grid:
                if (cell.open):
                    if len(pieces) == 12:
                        break
                    else:
                        pieces.append(Piece(self.sprites, self.cell_size, cell.pos, img))
        return pieces

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
            for sprite in self.sprites:
                sprite.draw(self.surf)
            
            # for i, piece in enumerate(self.player1_pieces):
            #     text = self.font.render(str(i), 1, 'grey')
            #     rect = text.get_frect(center = piece.rect.center)
            #     self.surf.blit(text, rect)

            # for i, piece in enumerate(self.player2_pieces):
            #     text = self.font.render(str(i), 1, 'grey')
            #     rect = text.get_frect(center = piece.rect.center)
            #     self.surf.blit(text, rect)


            self.win.flip()

        py.quit()
        raise SystemExit