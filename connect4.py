
import pygame
import sys
import numpy as np
import math


ROW_COUNT = 6
COLUMN_COUNT = 7
EVEN= 0
ODD = 1
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))  
    return board

def valid(board,position):
    for r in range(ROW_COUNT):
        if board[r][position] == 0:
            return True
    return False



def drop_piece(board,position,piece):
    for r in range(ROW_COUNT):
        if board[r][position] == 0:
            board[r][position] = piece
            return r
# Check for a win in all directions
def check_win(board, piece):
    # Horizontal Check
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):  # Stop at column 3 from the end
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical Check
    for r in range(ROW_COUNT - 3):  # Stop at row 3 from the end
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Diagonal Down-Right Check
    for r in range(ROW_COUNT - 3):  # Stop at row 3 from the end
        for c in range(COLUMN_COUNT - 3):  # Stop at column 3 from the end
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Diagonal Down-Left Check
    for r in range(3, ROW_COUNT):  # Start from row 3 to avoid out-of-bound errors
        for c in range(COLUMN_COUNT - 3):  # Stop at column 3 from the end
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False 

def is_full(board):
    return all(board[row][col] != " " for row in range(6) for col in range(7))

board = create_board()
game_over = False
turn = 0


'''Main game loop'''

while not game_over:
    if turn == 0:
        # player 1 move
        selection = input("Player 1 make your selection (0-6): ")
        turn += 1

        print(board)
        
        #player 2 move
    else:
        selection = input("Player 2 make your turn: ")
        turn = 0



