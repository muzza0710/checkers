# copilots attempt

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Create the display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Load images
CROWN = pygame.transform.scale(pygame.image.load('assets/checker_black.webp'), (44, 25))

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col

    @property
    def x(self):
        return self.col * SQUARE_SIZE + SQUARE_SIZE // 2

    @property
    def y(self):
        return self.row * SQUARE_SIZE + SQUARE_SIZE // 2

def create_board():
    board = []
    for row in range(ROWS):
        board.append([None] * COLS)
    for row in range(3):
        for col in range(row % 2, COLS, 2):
            board[row][col] = Piece(row, col, RED)
    for row in range(5, 8):
        for col in range(row % 2, COLS, 2):
            board[row][col] = Piece(row, col, BLUE)
    return board

def draw_board(win, board):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece is not None:
                piece.draw(win)

def get_piece_at(mouse_pos, board):
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return board[row][col]

def main():
    board = create_board()
    run = True
    clock = pygame.time.Clock()
    selected_piece = None

    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_piece = get_piece_at(pos, board)

            if event.type == pygame.MOUSEBUTTONUP and selected_piece is not None:
                pos = pygame.mouse.get_pos()
                new_row = pos[1] // SQUARE_SIZE
                new_col = pos[0] // SQUARE_SIZE
                selected_piece.move(new_row, new_col)
                selected_piece = None

        draw_board(WIN, board)
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
