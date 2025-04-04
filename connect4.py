
import pygame
import sys
import numpy as np
import math


ROW_COUNT = 6
COLUMN_COUNT = 7
EVEN=0
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



