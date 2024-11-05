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
        self.player_sprites = py.sprite.Group()
        self.board_sprites = py.sprite.Group()

        self.board = Board(self.board_sprites, cell_size=self.cell_size)
        self.player1_pieces = self.create_pieces(self.board.grid, self.p1_img, num_pieces= 4)
        self.player2_pieces = self.create_pieces(self.board.grid, self.p2_img, reverse=True, num_pieces= 4)

        self.moving_piece = None 

    def run(self):
        self.running = True
        temp = None

        while self.running:
            # event loop
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.MOUSEBUTTONUP and event.button == 1: 
                    if temp and temp.open:
                        self.moving_piece.pos = temp.rect.topleft
                        self.moving_piece.cell.open = True
                        self.moving_piece.cell = temp
                        temp.open = False

                    self.moving_piece.drag_pos = None
                    self.moving_piece = None 
                    temp = None
                    

            # update
            self.surf.fill((111,111,111))

            for sprite in self.player_sprites:
                if sprite.rect.collidepoint(py.mouse.get_pos()):
                    if py.mouse.get_pressed()[0] and not self.moving_piece:
                        self.moving_piece = sprite

            if self.moving_piece != None:
                self.moving_piece.drag_pos = py.mouse.get_pos()
                temp = self.check_mouse_collision(self.board_sprites)


            self.player_sprites.update()
    
            # draw
            self.board.draw(self.surf)

            for sprite in self.board_sprites:
                if sprite.rect.collidepoint(py.mouse.get_pos()) and sprite.open:
                    sprite.highlight(self.surf)

            if temp:
                temp.highlight(self.surf)

            for sprite in self.player_sprites:
                sprite.draw(self.surf)
            if self.moving_piece: self.moving_piece.draw(self.surf)
                
            
            # for i, piece in enumerate(self.player1_pieces):
            #     text = self.font.render(str(piece.cell.open), 1, 'black')
            #     rect = text.get_frect(center = piece.rect.center)
            #     self.surf.blit(text, rect)

            # for i, piece in enumerate(self.player2_pieces):
            #     text = self.font.render(str(piece.cell.open), 1, 'black')
            #     rect = text.get_frect(center = piece.rect.center)
            #     self.surf.blit(text, rect)

            for i, cell in enumerate(self.board_sprites):
                if cell.open:
                    text = self.font.render(str(cell.open), 1, 'white')
                    rect = text.get_frect(center = cell.rect.center)
                    self.surf.blit(text, rect)



            self.win.flip()



        py.quit()
        raise SystemExit
    

    def create_pieces(self, grid, img, reverse= False, num_pieces= 12):
        pieces = []
        if reverse == True: grid.reverse()
        for cell in grid:
                if (cell.open):
                    if len(pieces) == num_pieces:
                        break
                    else:
                        pieces.append(Piece(self.player_sprites, self.cell_size, cell.pos, img, cell))
                        cell.open = False
        return pieces

    def check_mouse_collision(self, group):
        for obj in group:
            if obj.rect.collidepoint(py.mouse.get_pos()):
                if obj.open:
                    return obj
        return False
        