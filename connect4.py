import pygame
import sys
import numpy as np
import math
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent
from classes.minimax_agent import Minimax_Agent

from classes.board import Board



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
    screen = pygame.display.set_mode((width , height))
    pygame.display.set_caption("Connect 4")
    
    game_running = True
    while game_running:
        screen.fill(RED)
        
        draw_text("Welcome to Connect 4", BLACK, width // 3, height // 4, screen)
        draw_button(width // 4, height // 2 - 80, "Player vs Player", screen)
        draw_button(width // 4, height // 2 + 20, "Player vs Bot", screen)
        draw_button(width // 4, height // 2 + 120, "Bot vs Bot", screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]

                # Player vs Player selected
                if width // 3 <= posx <= width // 3 + 200 and height // 2 - 80 <= posy <= height // 2 - 80 + 60:
                    print("Player vs Player selected")
                    start_player_vs_player()

                # Player vs Bot selected
                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                    print("Player vs Bot selected")
                    choose_bot_agent()

                # Player vs MiniMax Agent selected
                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 120 <= posy <= height // 2 + 120 + 60:
                    print("Bot v Bot")
                    choose_bot_v_bot()

        pygame.display.update()


#ChooseBot

def choose_bot_agent():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Select Bot Agent")

    game_running = True
    while game_running:
        screen.fill(RED)
        
        draw_text("Choose your Bot", BLACK, width // 4, height // 4, screen)
        draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
        draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
        draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)
        draw_button(width // 4, height // 2 + 220, "ML Agent", screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]

                if width // 3 <= posx <= width // 3 + 200 and height // 2 - 80 <= posy <= height // 2 - 80 + 60:
                    print("Random Agent selected")
                    start_player_vs_bot(Random_Agent())

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                    print("Smart Agent selected")
                    start_player_vs_bot(Smart_Agent())

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 120 <= posy <= height // 2 + 120 + 60:
                    print("MiniMax Agent selected")
                    start_player_vs_bot(Minimax_Agent())

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 220 <= posy <= height // 2 + 220 + 60:
                    print("ML Agent selected")
                    start_player_vs_bot(ML_Agent())

        pygame.display.update()


# # Create the board
# def create_board():
#     board = np.zeros((ROW_COUNT, COLUMN_COUNT))  
#     return board

# # Drop the piece on the board (bottom to top)
# def drop_piece(board, row, col, piece):
#     board[row][col] = piece

# # Check for a win in all directions
# def check_win(board, piece):
#     # Horizontal Check
#     for r in range(ROW_COUNT):
#         for c in range(COLUMN_COUNT - 3):
#             if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
#                 return True

#     # Vertical Check
#     for r in range(ROW_COUNT - 3):
#         for c in range(COLUMN_COUNT):
#             if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
#                 return True

#     # Diagonal Down-Right Check
#     for r in range(ROW_COUNT - 3):
#         for c in range(COLUMN_COUNT - 3):
#             if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
#                 return True

#     # Diagonal Down-Left Check
#     for r in range(3, ROW_COUNT):
#         for c in range(COLUMN_COUNT - 3):
#             if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
#                 return True

#     return False

# # Check if the board is full / draw
# def is_full(board):
#     return all(board[row][col] != 0 for row in range(ROW_COUNT) for col in range(COLUMN_COUNT))

# def get_next_open_row(board, col):
#     for r in range(ROW_COUNT - 1, -1, -1):  # Loop from the bottom row (ROW_COUNT-1) to the top row (0)
#         if board[r][col] == 0:  #
#             return r
#     return -1  #if column is full return -1

# # Draw the game board
# def draw_board(board, screen):
#     for c in range(COLUMN_COUNT):
#         for r in range(ROW_COUNT):
#             pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
#             pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

#             # Draw the pieces (Player 1 - Red, Player 2 - Yellow)
#             if board[r][c] == 1:
#                 pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
#             elif board[r][c] == 2:
#                 pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)



# Bot v Bot
def choose_bot_v_bot():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Select Two Bot Agents")

    game_running = True
    while game_running:
        screen.fill(RED)
        
        draw_text("Choose the first Bot", BLACK, width // 4, height // 4, screen)
        draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
        draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
        draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]

                if width // 3 <= posx <= width // 3 + 200 and height // 2 - 80 <= posy <= height // 2 - 80 + 60:
                    print("Random Agent selected as Bot 1")
                    bot1 = Random_Agent()

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                    print("Smart Agent selected as Bot 1")
                    bot1 = Smart_Agent()

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 120 <= posy <= height // 2 + 120 + 60:
                    print("MiniMax Agent selected as Bot 1")
                    bot1 = Minimax_Agent()

                # Proceed to select the second bot after the first is chosen
                screen.fill(RED)
                draw_text("Choose the second Bot", BLACK, width // 4, height // 4, screen)
                draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
                draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
                draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)

                for event2 in pygame.event.get():
                    if event2.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event2.type == pygame.MOUSEBUTTONDOWN:
                        posx2 = event2.pos[0]
                        posy2 = event2.pos[1]

                        if width // 3 <= posx2 <= width // 3 + 200 and height // 2 - 80 <= posy2 <= height // 2 - 80 + 60:
                            print("Random Agent selected as Bot 2")
                            bot2 = Random_Agent()

                        elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 20 <= posy2 <= height // 2 + 20 + 60:
                            print("Smart Agent selected as Bot 2")
                            bot2 = Smart_Agent()

                        elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 120 <= posy2 <= height // 2 + 120 + 60:
                            print("MiniMax Agent selected as Bot 2")
                            bot2 = Minimax_Agent()

                        start_bot_vs_bot(bot1, bot2)
                        return

                pygame.display.update()


# Bot v Bot Game Loop
def start_bot_vs_bot(bot1, bot2):
    board = Board()  # Use Board class to manage the game state
    game_over = False
    turn = 0  # 0 = Bot 1, 1 = Bot 2
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4 - Bot vs Bot")

    while not game_over:
        board.draw_board(screen)  # Use the draw_board method from Board class
        pygame.display.update()

        if turn == 0:  # Bot 1's turn
            print("Bot 1 is thinking...")
            col = bot1.best_move(board.board)  # Bot 1 predicts move
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, 1)  # Make move for Bot 1

            if board.check_win(1):  # Bot 1 wins
                board.draw_board(screen)
                pygame.display.update()
                print("Bot 1 wins!")
                game_over = True

            turn = 1  # Switch to Bot 2

        if turn == 1:  # Bot 2's turn
            print("Bot 2 is thinking...")
            col = bot2.best_move(board.board)  # Bot 2 predicts move
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, 2)  # Make move for Bot 2

            if board.check_win(2):  # Bot 2 wins
                board.draw_board(screen)
                pygame.display.update()
                print("Bot 2 wins!")
                game_over = True

            turn = 0  # Switch to Bot 1

        if board.is_full() and not game_over:  # Check for a draw
            board.draw_board(screen)
            pygame.display.update()
            print("It's a draw!")
            game_over = True

    pygame.quit()


# pvp
def start_player_vs_player():
    board = Board()
    game_over = False
    turn = 0  # 0 = Player 1 (Red), 1 = Player 2 (Yellow)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")

    # Game loop
    while not game_over:
        board.draw_board(screen)
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

                if board.board[0][col] == 0:  # Check if the column is not full
                    row = board.get_next_open_row(board, col)  # Get the next available row
                    board.drop_piece(board, row, col, 1 if turn == 0 else 2)
                    

                    # check win for every turn
                    if board.check_win(board, 1 if turn == 0 else 2): 
                        board.draw_board(screen)
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

         

                    board.draw_board(screen)  # Redraw the board after the move
                    print(board)

                    if board.is_full():  # Check for a draw
                        board.draw_board( screen)
                        pygame.display.update()
                        pygame.time.wait(500)
                        print("It's a draw!")
                        game_over = True

    pygame.quit()  #Quit



# player v bot
def start_player_vs_bot(bot_agent):
    board = Board()
    game_over = False
    turn = 0  # 0 = Player 1 (Red), 1 = Bot (Yellow)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")

    while not game_over:
        board.draw_board(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  # Player's turn
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if board.board[0][col] == 0:  # Check if column is not full
                    row = board.get_next_open_row(col)  # Get next available row
                    board.drop_piece(row, col, 1)  # Drop the piece for Player 1
                    print(board.board)

                    if board.check_win(1):  # Check for a win for Player 1
                        board.draw_board(screen)
                        pygame.display.update()
                        print("Player 1 wins!")
                        game_over = True
                    turn = 1  # Switch to bot

        if turn == 1 and not game_over:  # Bot's turn
            print(f"Bot is thinking... {bot_agent}")
            col = bot_agent.best_move(board)  # Get best move from bot

            row = board.get_next_open_row(col)  # Get the next available row
            board.drop_piece(row, col, 2)  # Drop the piece for Bot

            print(board.board)

            if board.check_win(2):  # Check for a win for the Bot
                board.draw_board(screen)
                pygame.display.update()
                print("Bot wins!")
                game_over = True
            turn = 0  # Switch back to player

        if board.is_full() and not game_over:  # Check for a draw
            board.draw_board(screen)
            pygame.display.update()
            print("It's a draw!")
            game_over = True
            break



         



if __name__ == "__main__":
    HomePage()
