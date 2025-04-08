import pygame
import sys
import numpy as np
import math


ROW_COUNT = 6
COLUMN_COUNT = 7
EVEN = 0
ODD = 1

# Create the board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))  
    return board

# Drop the piece on the board (bottom to top)
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check for a win in all directions
def check_win(board, piece):
    # Horizontal Check
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical Check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Diagonal Down-Right Check
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Diagonal Down-Left Check
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

# Check if the board is full
def is_full(board):
    return all(board[row][col] != 0 for row in range(ROW_COUNT) for col in range(COLUMN_COUNT))

# Get the next available row for a given column (starts from the bottom)
def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):  # Loop from the bottom row (ROW_COUNT-1) to the top row (0)
        if board[r][col] == 0:  # If there's an empty spot (0)
            return r
    return -1  # Return -1 if no empty spot is found (column is full)

# Print the board for visual debugging
def print_board(board):
    for r in range(ROW_COUNT):
        print("|", end="")
        for c in range(COLUMN_COUNT):
            print(" " + str(int(board[r][c])) + " |", end="")
        print("\n" + "----" * COLUMN_COUNT)

# Main game loop
board = create_board()
game_over = False
turn = 0

while not game_over:
    print_board(board)
    
    if turn == 0:  # Player 1's turn
        while True:
            try:
                col = int(input("Player 1, make your selection (0-6): "))
                if col < 0 or col >= 7:
                    print("Invalid column. Please enter a number between 0 and 6.")
                    continue

                row = get_next_open_row(board, col)
                if row != -1:  # If we found a valid row
                    drop_piece(board, row, col, 1)
                    break
                else:
                    print("Column is full. Try a different column.")
            except ValueError:
                print("Invalid input. Please enter an integer between 0 and 6.")
                continue

        if check_win(board, 1):
            print_board(board)
            print("Player 1 wins!")
            game_over = True
        else:
            turn += 1  # Switch turn to Player 2

    else:  # Player 2's turn
        while True:
            try:
                col = int(input("Player 2, make your selection (0-6): "))
                if col < 0 or col >= 7:
                    print("Invalid column. Please enter a number between 0 and 6.")
                    continue

                row = get_next_open_row(board, col)
                if row != -1:  # If we found a valid row
                    drop_piece(board, row, col, 2)
                    break
                else:
                    print("Column is full. Try a different column.")
            except ValueError:
                print("Invalid input. Please enter an integer between 0 and 6.")
                continue

        if check_win(board, 2):
            print_board(board)
            print("Player 2 wins!")
            game_over = True
        else:
            turn = 0  # Switch turn to Player 1

    # Check for a draw
    if is_full(board) and not game_over:
        print_board(board)
        print("It's a draw!")
        game_over = True
