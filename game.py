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
        # Groups
        self.player_sprites = py.sprite.Group()
        self.board_sprites = py.sprite.Group()

        # Board
        self.board = Board(self.board_sprites, cell_size=self.cell_size)

        # Pieces
        self.player1_pieces = self.create_pieces(self.board.grid, self.p1_img, 1, num_pieces= 8)
        self.player2_pieces = self.create_pieces(self.board.grid, self.p2_img, 2, reverse=True, num_pieces= 8)

        # Dragging
        self.moving_piece = None 

    def run(self):
        self.running = True
        temp_cell = None

        while self.running:
            # event loop
            for event in py.event.get():
                # Quit condition
                if event.type == py.QUIT:
                    self.running = False
                
                # After dragging a piece
                if event.type == py.MOUSEBUTTONUP and event.button == 1: 
                    if temp_cell and temp_cell.open and temp_cell in self.moving_piece.moves:
                        self.moving_piece.pos = temp_cell.rect.topleft
                        self.moving_piece.cell.open = True
                        self.moving_piece.cell = temp_cell
                        temp_cell.open = False

                    if self.moving_piece:
                        self.moving_piece.drag_pos = None
                        self.moving_piece = None 
                        temp_cell = None
                    

            # update
            self.surf.fill((111,111,111))

            # select moving piece if clicked on
            for sprite in self.player_sprites:
                if sprite.rect.collidepoint(py.mouse.get_pos()):
                    if py.mouse.get_pressed()[0] and not self.moving_piece:
                        self.moving_piece = sprite

            # if a piece is being moved set its position and potential new cell
            if self.moving_piece != None:
                self.moving_piece.drag_pos = py.mouse.get_pos()
                temp_cell = self.check_mouse_collision(self.board_sprites)

            # update player pieces
            self.player_sprites.update(self.board)
    
            # draw
            self.board.draw(self.surf)

            # higlight hovered cells that are open
            for sprite in self.board_sprites:
                if sprite.rect.collidepoint(py.mouse.get_pos()) and not self.moving_piece: # and sprite.open:
                    sprite.highlight(self.surf)
                    # print(sprite.open, sprite.index, self.board.grid[sprite.index].open)

            if temp_cell:
                temp_cell.highlight(self.surf)

            for sprite in self.player_sprites:
                sprite.draw(self.surf)
                if sprite.rect.collidepoint(py.mouse.get_pos()) and not self.moving_piece:
                    sprite.highlight(self.surf)
            if self.moving_piece: 
                self.moving_piece.highlight(self.surf)
                self.moving_piece.draw(self.surf)
                
            
            # for i, piece in enumerate(self.player1_pieces):
            #     text = self.font.render(str(piece.cell.open), 1, 'black')
            #     rect = text.get_frect(center = piece.rect.center)
            #     self.surf.blit(text, rect)

            # for i, piece in enumerate(self.player2_pieces):
            #     text = self.font.render(str(piece.cell.index), 1, 'black')
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
    

    def create_pieces(self, grid, img, player, reverse= False, num_pieces= 12):
        pieces = []
        board = grid[:]
        if reverse == True: board = reversed(grid[:])
        for cell in board:
                if (cell.open):
                    if len(pieces) == num_pieces:
                        break
                    else:
                        pieces.append(Piece(self.player_sprites, self.cell_size, cell.pos, img, cell, self.board, player))
                        cell.open = False
        return pieces

    def check_mouse_collision(self, group):
        for obj in group:
            if obj.rect.collidepoint(py.mouse.get_pos()):
                if obj.open:
                    return obj
        return False
        