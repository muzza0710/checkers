import pygame as py
from board import Board
from piece import Piece
from info_panel import InfoPanel
import sys

PIECES = 8
CELL_SIZE = 75
ROWS, COLS = 8, 8

class Checkers:
    def __init__(self) -> None:
        py.init()
        self.font = py.Font(None, 20)
        info_panel_size = [(COLS * CELL_SIZE) * 0.4, ROWS * CELL_SIZE]
        self.win = py.Window('Checkers', (COLS * CELL_SIZE + info_panel_size[0], ROWS * CELL_SIZE))
        self.surf = self.win.get_surface()

        self.p1_img = self.load_image('assets/checker_white_blank.png')
        self.p1_king_img = self.load_image('assets/checker_white.webp')
        self.p2_img = self.load_image('assets/checker_red_blank.png')
        self.p2_king_img = self.load_image('assets/checker_red.webp')

        self.info_panel = InfoPanel(info_panel_size, (COLS * CELL_SIZE, 0))

    def load_image(self, path):
        try:
            return py.image.load(path).convert_alpha()
        except py.error as e:
            print(f"Could not load image {path}: {e}")
            sys.exit(1)

    def setup(self):
        self.player_sprites = py.sprite.Group()
        self.board_sprites = py.sprite.Group()
        self.board = Board(self.board_sprites, cell_size=CELL_SIZE)
        self.player1_pieces = self.create_pieces(self.board.grid, self.p1_img, 1, num_pieces=PIECES)
        self.player2_pieces = self.create_pieces(self.board.grid, self.p2_img, 2, reverse=True, num_pieces=PIECES)
        self.moving_piece = None 

    def run(self):
        self.running = True
        temp_cell = None
        player_turn = self.player1_pieces

        while self.running:
            self.handle_events(player_turn, temp_cell)
            self.update_screen(player_turn, temp_cell)
        py.quit()
        raise SystemExit

    def handle_events(self, player_turn, temp_cell):
        for event in py.event.get():
            if event.type == py.QUIT or event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                self.running = False
            if event.type == py.MOUSEBUTTONUP and event.button == 1:
                self.handle_mouse_up(player_turn, temp_cell)

    def handle_mouse_up(self, player_turn, temp_cell):
        if temp_cell and not temp_cell.occupied:
            for d in self.moving_piece.moves:
                if d['move'] == temp_cell:
                    if 'piece' in d:
                        d['piece'].cell.remove_piece()
                    self.moving_piece.pos = temp_cell.rect.topleft
                    self.moving_piece.cell.occupied = False
                    self.moving_piece.cell.piece = None
                    temp_cell.piece = self.moving_piece
                    temp_cell.occupied = self.moving_piece.player
                    self.moving_piece.cell = temp_cell
                    player_turn = self.player2_pieces if player_turn == self.player1_pieces else self.player1_pieces
        if self.moving_piece:
            self.moving_piece.drag_pos = None
            self.moving_piece = None 
            temp_cell = None

    def update_screen(self, player_turn, temp_cell):
        self.surf.fill((111, 111, 111))
        for sprite in self.player_sprites:
            if sprite.rect.collidepoint(py.mouse.get_pos()):
                if py.mouse.get_pressed()[0] and not self.moving_piece and sprite in player_turn:
                    self.moving_piece = sprite
        if self.moving_piece:
            self.moving_piece.drag_pos = py.mouse.get_pos()
            temp_cell = self.check_mouse_collision(self.board_sprites)

        info_text = 'White Move' if player_turn == self.player1_pieces else 'Red Move'

        self.player_sprites.update(self.board)
        self.board_sprites.update()
        self.board.draw(self.surf)
        for sprite in self.board_sprites:
            if sprite.rect.collidepoint(py.mouse.get_pos()) and not self.moving_piece and not sprite.occupied:
                sprite.highlight(self.surf)
        if temp_cell:
            temp_cell.highlight(self.surf)
        for sprite in self.player_sprites:
            sprite.draw(self.surf)
            if sprite.rect.collidepoint(py.mouse.get_pos()) and not self.moving_piece and sprite in player_turn:
                sprite.highlight(self.surf)
        if self.moving_piece:
            self.moving_piece.highlight(self.surf)
            self.moving_piece.draw(self.surf)
        self.info_panel.draw(self.surf)
        self.info_panel.print(self.surf, info_text)
        self.win.flip()

    def create_pieces(self, grid, img, player, reverse=False, num_pieces=12):
        pieces = []
        board = grid[::-1] if reverse else grid
        for cell in board:
            if not cell.occupied:
                if len(pieces) == num_pieces:
                    break
                piece = Piece(self.player_sprites, CELL_SIZE, cell.pos, img, cell, self.board, player)
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

