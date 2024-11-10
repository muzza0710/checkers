import pygame as py
from board import Board
from piece import Piece
from info_panel import InfoPanel

PIECES = 1

class Checkers:
    def __init__(self) -> None:
        py.init()
        self.font = py.Font(None, 50)
        
        self.cell_size = 75
        self.rows, self.cols = 8,8
        info_panel_size = [(self.cols * self.cell_size) * 0.4, self.rows * self.cell_size]
        self.window_size = (self.cols * self.cell_size + info_panel_size[0], self.rows * self.cell_size)
        self.win = py.Window(title='Checkers', size=self.window_size)
        self.surf = self.win.get_surface()
        self.player_moves = []

        self.p1_img = py.image.load('assets\checker_white_blank.png').convert_alpha()
        self.p1_king_img = py.image.load('assets\checker_white.webp').convert_alpha()

        self.p2_img = py.image.load('assets\checker_red_blank.png').convert_alpha()
        self.p2_king_img = py.image.load('assets\checker_red.webp').convert_alpha()

        self.info_panel = InfoPanel(info_panel_size, (self.cols * self.cell_size, 0) )

    def setup(self):
        # Groups
        self.player_sprites = py.sprite.Group()
        self.board_sprites = py.sprite.Group()

        # Board
        self.board = Board(self.board_sprites, cell_size=self.cell_size)

        # Pieces
        self.player1_pieces = self.create_pieces(self.board.grid, self.p1_img, self.p1_king_img, 1, num_pieces= PIECES)
        self.player2_pieces = self.create_pieces(self.board.grid, self.p2_img, self.p2_king_img, 2, reverse=True, num_pieces= PIECES)

        # Dragging
        self.moving_piece = None 
        self.temp_cell = None
        self.player_turn = self.player2_pieces

        return True

    def run(self):
        self.running = True
        self.game_over = False
        self.game_in_progress = False

        while self.running:
            # event loop
            self.check_events()
            if self.game_in_progress:
                self.game_loop()
            elif not self.game_over:
                self.start_screen()
            if self.game_over:
                self.info_panel.print(self.surf,'Enter to', 2)
                self.info_panel.print(self.surf,'Restart', 3)
                self.info_panel.print(self.surf,'Esc to exit', 6)

            # debug
            self.debug(False)
        
            self.win.flip()
        py.quit()
        raise SystemExit

    def check_events(self):
        for event in py.event.get():
            # Quit condition
            if event.type == py.QUIT or event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                self.running = False
            
            # After dragging a piece
            if event.type == py.MOUSEBUTTONUP and event.button == 1: 
                self.move_piece()

            # debug
            if event.type == py.KEYDOWN and event.key == py.K_SPACE:
                if self.moving_piece and self.moving_piece.moves:
                    print(f'take = {self.moving_piece.take_moves}, normal = {[move["move"].index for move in self.moving_piece.moves]}')

            if not self.game_in_progress or self.game_over:
                if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                    self.game_in_progress = self.setup()
                    self.game_over = False

    def check_winner(self) -> str:
        if len(self.player1_pieces) == 0:
            return 'Red Wins!'
        elif len(self.player2_pieces) == 0:
            return 'White Wins'
        else:
            return None

    def create_pieces(self, grid, img, king_img, player, reverse= False, num_pieces= 12):
        pieces = []
        board = grid[:]
        if reverse == True: board = reversed(grid[:])
        for cell in board:
                if not cell.occupied:
                    if len(pieces) == num_pieces:
                        break
                    else:
                        piece = Piece(self.player_sprites, self.cell_size, cell.pos, img, king_img, cell, self.board, player)
                        pieces.append(piece)
                        cell.occupied = player
                        cell.piece = piece
        return pieces

    def check_mouse_collision(self, group):
        for obj in group:
            if obj.rect.collidepoint(py.mouse.get_pos()):
                if not obj.occupied:
                    return obj
        return False
    
    def debug(self, run):
        if run:
            for i, piece in enumerate(self.player1_pieces):
                text = self.font.render(str(piece.cell.occupied), 1, 'black')
                rect = text.get_frect(center = piece.rect.center)
                self.surf.blit(text, rect)

            for i, piece in enumerate(self.player2_pieces):
                text = self.font.render(str(piece.cell.index), 1, 'black')
                rect = text.get_frect(center = piece.rect.center)
                self.surf.blit(text, rect)

            for i, cell in enumerate(self.board_sprites):
                    text = self.font.render(str(cell.occupied), 1, 'blue')
                    rect = text.get_frect(center = cell.rect.center)
                    self.surf.blit(text, rect)

    def drag_piece(self):
        for sprite in self.player_sprites:
            if sprite.rect.collidepoint(py.mouse.get_pos()):
                if py.mouse.get_pressed()[0] and not self.moving_piece and sprite in self.player_turn:
                    self.moving_piece = sprite

        # if a piece is being moved set its position and potential new cell
        if self.moving_piece != None:
            self.moving_piece.drag_pos = py.mouse.get_pos()
            self.temp_cell = self.check_mouse_collision(self.board_sprites)

    def get_player_moves(self):
        self.player_moves = []
        moves = []
        for piece in self.player_turn:
            if piece.take_moves:
                self.player_moves.extend(move for move in piece.take_moves)
            if piece.moves:
                moves.extend(move for move in piece.moves)
        if len(self.player_moves) == 0:
            self.player_moves = moves

    def move_piece(self):
        takeing = False
        if self.temp_cell and not self.temp_cell.occupied:
            for d in self.moving_piece.moves:
                if d['move'] == self.temp_cell and any(move_dict['move'] == self.temp_cell for move_dict in self.player_moves):
                    if 'piece' in d:
                        piece = d['piece'].cell.remove_piece()
                        if piece in self.player1_pieces: 
                            self.player1_pieces.remove(piece)
                            takeing = True
                        if piece in self.player2_pieces: 
                            self.player2_pieces.remove(piece)
                            takeing = True
                    self.moving_piece.pos = self.temp_cell.rect.topleft
                    self.moving_piece.cell.occupied = False
                    self.moving_piece.cell.piece = None
                    self.temp_cell.piece = self.moving_piece
                    self.temp_cell.occupied = self.moving_piece.player
                    self.moving_piece.cell = self.temp_cell
                    self.moving_piece.update(self.board)
                    if not takeing or len(self.moving_piece.take_moves) == 0:
                        self.player_turn = self.player2_pieces if self.player_turn == self.player1_pieces else self.player1_pieces
        
        # clear moving piece and temp cell
        if self.moving_piece:
            self.moving_piece.drag_pos = None
            self.moving_piece = None 
            self.temp_cell = None    

    def show_info_panel(self, winner_text, info_text):
        self.info_panel.draw(self.surf)
        self.info_panel.row_height = self.cell_size
        if winner_text: 
            self.info_panel.print(self.surf, winner_text)
        else:
            self.info_panel.print(self.surf, info_text)
        
        # self.info_panel.print(self.surf, 'testing new line', line=7)


    # state functions
    def game_loop(self):
        # UPDATE
        self.surf.fill((111,111,111))
        winner_text = self.check_winner()
        if winner_text:
            self.game_over = True
            

        # Player_moves
        self.get_player_moves()

        # select moving piece if clicked on
        self.drag_piece()

        # update player pieces
        self.player_sprites.update(self.board)
        self.board_sprites.update()
        info_text = 'White Move' if self.player_turn == self.player1_pieces else 'Red Move'


        # DRAW
        self.board.draw(self.surf)

        # higlight hovered cells that are open
        for sprite in self.board_sprites:
            if sprite.rect.collidepoint(py.mouse.get_pos()) and not self.moving_piece and not sprite.occupied:
                sprite.highlight(self.surf)

        # highlight cell moving piece will occupy
        if self.temp_cell:
            self.temp_cell.highlight(self.surf)

        # higlight moves for hovered pieces for the play whose turn it is
        for sprite in self.player_sprites:
            sprite.draw(self.surf)
            if sprite.rect.collidepoint(py.mouse.get_pos()) and not self.moving_piece and sprite in self.player_turn:
                sprite.highlight(self.surf)

        # highlight and draw moving piece last so its always on top
        if self.moving_piece: 
            self.moving_piece.highlight(self.surf)
            self.moving_piece.draw(self.surf)

        # draw info panel
        self.show_info_panel(winner_text, info_text)

    def start_screen(self):
        self.surf.fill('blue')
        text = self.font.render('Press enter to start', True, 'Black')
        rect = text.get_frect(center = (self.window_size[0]// 2 , self.window_size[1] // 2))
        self.surf.blit(text, rect)
        self.game_over = False

        