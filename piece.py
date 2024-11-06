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
        self.take_pieces = []
        if self.player == 1:
            self.moves = self.get_moves('down', self.cell.index)
        elif self.player == 2:
            self.moves = self.get_moves('up', self.cell.index)

    def draw(self, surface):
        surface.blit(self.resized_img, self.rect)

    def highlight(self, surface, color= (0,200,0)):
        py.draw.rect(surface, color, self.rect, 2, self.size // 2 )
        if len(self.moves) > 0:
            for d in self.moves:
                if d['move']:
                    d['move'].highlight(surface, (0,0,200))
        if self.take_moves:
            for t in self.take_moves:
                if t['move']:
                    t['move'].highlight(surface, color)
                    py.draw.rect(surface, (200,0,0), t['piece'].rect, 2, self.size // 2 )
        # if self.take_pieces:
        #     for piece in self.take_pieces:
        #            py.draw.rect(surface, (200,0,0), piece.rect, 2, self.size // 2 )

    def get_moves(self, direction, index):
        if direction == 'down':
            dir = 8
        elif direction == 'up':
            dir = -8
        i = index + dir
        self.take_moves = []
        self.take_pieces = []

        # left move
        if 0 < i < len(self.board.grid) -1:
            if i % self.board.cols > 0:
                if self.board.grid[i-1].occupied != self.player and self.board.grid[i-1].occupied:
                    try:   
                        j = self.board.grid[i-1].index
                    except Exception as e: 
                        print(e, '1')
                    if 0 < j + dir < len(self.board.grid) -1 and j % self.board.cols > 0:     
                        move = {'move': self.board.grid[j-1 + dir] if not self.board.grid[j-1 + dir].occupied else None, 'piece': None}
                        if move['move']:
                            self.take_moves.append(move)
                            if self.board.grid[j].piece:
                                move['piece'] = self.board.grid[j].piece
                    
                if not self.board.grid[i-1].occupied:
                    move = {'move': self.board.grid[i-1]}
                    self.moves.append(move)
                
            # right move
            if i % self.board.cols < self.board.cols - 1:
                if self.board.grid[i+1].occupied != self.player and self.board.grid[i+1].occupied:
                    try:
                        j = self.board.grid[i+1].index
                    except Exception as e: 
                        print(e, '2')
                    if 0 < j + dir < len(self.board.grid) -1 and j % self.board.cols < self.board.cols - 1:
                        move = {'move' :self.board.grid[j+1+ dir] if not self.board.grid[j+1+dir].occupied else None}
                        if move['move']:
                            self.take_moves.append(move)
                            if self.board.grid[j].piece:
                                move['piece'] = self.board.grid[j].piece
                                self.take_pieces.append(move)
                    
                if not self.board.grid[i+1].occupied:
                    self.moves.append({'move': self.board.grid[i+1]})
                    
        if len(self.take_moves) > 0:
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