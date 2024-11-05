import pygame as py

class Piece(py.sprite.Sprite):
    def __init__(self, groups, size, pos, img, cell, board, player) -> None:
        super().__init__(groups)
        self.cell, self.pos, self.size, self.groups = cell, pos, size, groups
        self.board, self.player = board, player
        self.drag_pos = None

        self.image = img
        self.resized_img = py.transform.scale(self.image, (size, size))

        self.surf = py.Surface((size, size))
        self.rect = self.surf.get_frect(topleft = pos)

        # def moves
        self.moves = []
        if player == 1:
            self.get_moves('down')
        elif player == 2:
            self.get_moves('up')

    def draw(self, surface):
        surface.blit(self.resized_img, self.rect)

    def highlight(self, surface):
        py.draw.rect(surface, (0,200,0), self.rect, 2, self.size // 2 )
        # print(f'index = {self.cell.index}, i = {self.i}')
        for cell in self.moves:
            cell.highlight(surface)

    def get_moves(self, direction):
        if direction == 'down':
            i = self.cell.index + 8
        elif direction == 'up':
            i = self.cell.index - 8
        if 0 < i < len(self.board.grid) -1:
            if i % self.board.cols > 0 and self.board.grid[i-1].open:
                self.moves.append(self.board.grid[i-1])
            if i % self.board.cols < self.board.cols - 1 and self.board.grid[i+1].open:
                self.moves.append(self.board.grid[i+1])

    def update(self, board):
        # update board 
        self.board = board

        # update position
        self.rect.topleft = self.pos
        if self.drag_pos != None:
            self.rect.center = self.drag_pos

        # update available moves
        self.moves = []
        if self.player == 1:
            self.get_moves('down')
        elif self.player == 2:
            self.get_moves('up')