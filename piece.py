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
        if self.player == 1:
            self.moves = self.get_moves('down', self.cell.index)
        elif self.player == 2:
            self.moves = self.get_moves('up', self.cell.index)

    def draw(self, surface):
        surface.blit(self.resized_img, self.rect)

    def highlight(self, surface, color= (0,200,0)):
        py.draw.rect(surface, color, self.rect, 2, self.size // 2 )
        # print(f'index = {self.cell.index}, i = {self.i}')
        if self.moves:
            for cell in self.moves:
                cell.highlight(surface, (0,0,200))
        if self.take_moves:
            for cell in self.take_moves:
                cell.highlight(surface, color)

    def get_moves(self, direction, index):
        if direction == 'down':
            dir = 8
        elif direction == 'up':
            dir = -8
        i = index + dir
        self.take_moves = []

        # left move
        if 0 < i < len(self.board.grid) -1:
            if i % self.board.cols > 0:
                if self.board.grid[i-1].occupied != self.player and self.board.grid[i-1].occupied:
                    try:   
                        j = self.board.grid[i-1].index
                        if 0 < j < len(self.board.grid) -1 and j % self.board.cols > 0:     
                            moves = self.board.grid[j-1 + dir] if not self.board.grid[j-1 + dir].occupied else None
                            if moves:
                                self.take_moves.append(moves)
                    except Exception as e: 
                        print(e, '1')
                elif not self.board.grid[i-1].occupied:
                    self.moves.append(self.board.grid[i-1])
                
            # right move
            if i % self.board.cols < self.board.cols - 1:
                if self.board.grid[i+1].occupied != self.player and self.board.grid[i+1].occupied:
                    try:
                        j = self.board.grid[i+1].index
                        if 0 < j < len(self.board.grid) -1 and j % self.board.cols < self.board.cols - 1:
                            moves = self.board.grid[j+1+ dir] if not self.board.grid[j+1+dir].occupied else None
                        if moves:
                            self.take_moves.append(moves)
                    except Exception as e: 
                        print(e, '2')
                elif not self.board.grid[i+1].occupied:
                    self.moves.append(self.board.grid[i+1])

        if self.take_moves:
            self.moves = self.take_moves
                

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
            self.get_moves('down', self.cell.index)
        elif self.player == 2:
            self.get_moves('up', self.cell.index)