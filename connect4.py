import pygame
import sys
import numpy as np
import math
import classes


ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE


BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)

pygame.init()

#Homepage

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

# Check if the board is full / draw
def is_full(board):
    return all(board[row][col] != 0 for row in range(ROW_COUNT) for col in range(COLUMN_COUNT))

def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):  # Loop from the bottom row (ROW_COUNT-1) to the top row (0)
        if board[r][col] == 0:  #
            return r
    return -1  #if column is full return -1

# Draw the game board
def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

            # Draw the pieces (Player 1 - Red, Player 2 - Yellow)
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

# Main game loop
def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 = Player 1 (Red), 1 = Player 2 (Yellow)


    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")

    # Game loop
    while not game_over:
        draw_board(board, screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Clear the top row where the preview is drawn
                posx = event.pos[0]

                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)



            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)  # Get the column based on the mouse position

                if board[0][col] == 0:  # Check if the column is not full
                    row = get_next_open_row(board, col)  # Get the next available row
                    drop_piece(board, row, col, 1 if turn == 0 else 2)
                    

                    # check win for every turn
                    if check_win(board, 1 if turn == 0 else 2): 
                        draw_board(board, screen)
                        pygame.display.update()
                        pygame.time.wait(500)
                        if turn == 0:
                            print("Player 1 wins!")
                        else:
                            print("Player 2 wins!")
                        game_over = True

                        # switching turns
                    if turn == 0:
                        turn+=1
                    else:
                        turn =0
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

         

                    draw_board(board, screen)  # Redraw the board after the move

                    if is_full(board):  # Check for a draw
                        draw_board(board, screen)
                        pygame.display.update()
                        pygame.time.wait(500)
                        print("It's a draw!")
                        game_over = True

    pygame.quit()  #Quit


def HomePage():

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")
    # home screen display 2 options to play player v player or vs bot.
    for event in pygame.event.get():
     if event.type == pygame.MOUSEBUTTONDOWN:
         posx = event.pos[0]
        
         



if __name__ == "__main__":
    main()
