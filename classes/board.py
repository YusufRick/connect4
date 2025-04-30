import numpy as np
import pygame

#board constant
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

#colours
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


class Board:

    def __init__(self):
        self.board = self.create_board()

    # 6 rows, 7 col
    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))  
        return board
    # drop piece
    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
    #check if board is full
    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(COLUMN_COUNT))

    # Get available moves
    def get_available_moves(self):
        return [col for col in range(7) if self.board[0][col] == 0]
    
    # Get the lowest row on the selected column
    def get_next_open_row(self, col):
        for r in range(5, -1, -1):  
            if self.board[r][col] == 0:
                return r
        return -1

    def check_win(self, piece):
        # Horizontal Check
        for r in range(6):
            for c in range(4):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return True

        # Vertical Check
        for r in range(3):
            for c in range(7):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return True

        # Diagonal Down-Right Check
        for r in range(3):
            for c in range(4):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return True

        # Diagonal Down-Left Check
        for r in range(3):
            for c in range(3, 7):
                if all(self.board[r+i][c-i] == piece for i in range(4)):
                    return True

        return False
    
    def copy(self):
        new_board = Board()
        new_board.board = np.copy(self.board)
        return new_board

        # Draw the blue grid
        # Draw empty circles in black
        # Draw red and yellow pieces on board
    def draw_board(self, screen):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
