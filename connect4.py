import pygame
import sys
import numpy as np
import math
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent





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
def draw_text(text, color, x, y, screen):
    font = pygame.font.SysFont("Arial", 40)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(x, y, text, screen):
    pygame.draw.rect(screen, BLUE, (x, y, 400, 70))
    draw_text(text, WHITE, x + 20, y + 15, screen)

def HomePage():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")
    
    # Main game loop for the home screen
    game_running = True
    while game_running:
        screen.fill(WHITE)
        
        draw_text("Welcome to Connect 4", BLACK, width // 3, height // 4, screen)
        draw_button(width // 3, height // 2 - 80, "Player vs Player", screen)
        draw_button(width // 3, height // 2 + 20, "Player vs Bot", screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]

                if width // 3 <= posx <= width // 3 + 200 and height // 2 - 80 <= posy <= height // 2 - 80 + 60:
                    print("Player vs Player selected")
                    start_player_vs_player()

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                    print("Player vs Bot selected")
                    start_player_vs_bot()

        pygame.display.update()


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

# pvp
def start_player_vs_player():
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

def start_player_vs_bot():
    # Create bot instances (you can choose which bot to play)
    random_bot = Random_Agent()
    smart_bot = Smart_Agent()

    # Example of how you might use the bot for moves:
    board = create_board()
    game_over = False
    turn = 0  # 0 = Player 1 (Red), 1 = Bot (Yellow)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")

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

                if turn == 0:  # Player 1's turn
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:  # Bot's turn (Player 2)
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  # Only allow player to make a move if it's their turn
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)  # Get the column based on the mouse position

                if board[0][col] == 0:  # Check if the column is not full
                    row = get_next_open_row(board, col)  # Get the next available row
                    drop_piece(board, row, col, 1)  # Drop the player's piece

                    if check_win(board, 1):  # Check if the player wins
                        draw_board(board, screen)
                        pygame.display.update()
                        pygame.time.wait(500)
                        print("Player 1 wins!")
                        game_over = True
                        break

                    turn = 1  # Switch turn to bot

        if turn == 1 and not game_over:  # Bot's turn (after player)
            print("Bot is thinking...")

            # Use the smart bot to make a move
            col = smart_bot.smart_agent_move(board)

            row = get_next_open_row(board, col)  # Get the next available row for the bot
            drop_piece(board, row, col, 2)  # Drop the bot's piece

            if check_win(board, 2):  # Check if the bot wins
                draw_board(board, screen)
                pygame.display.update()
                pygame.time.wait(500)
                print("Bot wins!")
                game_over = True
                break

            turn = 0  # Switch turn to player

        if is_full(board) and not game_over:  # Check for a draw
            draw_board(board, screen)
            pygame.display.update()
            pygame.time.wait(500)
            print("It's a draw!")
            game_over = True
            break

         



if __name__ == "__main__":
    HomePage()
