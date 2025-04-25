# test_ml_agent.py
from ucimlrepo import fetch_ucirepo
import pygame
import sys
import numpy as np
import math
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent
from classes.minimax_agent import Minimax_Agent
from classes.test import MLAgent

from classes.board import Board

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
connect_4 = fetch_ucirepo(id=26)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

pygame.init()

# Homepage
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


# Choose Bot
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
                    ml_agent = MLAgent()
                    X = connect_4.data.features
                    X = X.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)


                    y = connect_4.data.targets
                    y = y.replace({'win': 0, 'draw': 1, 'loss': 2})
                    ml_agent.load_data(X, y) 
                    ml_agent.train()
                    start_player_vs_bot(ml_agent)  # Use ML Agent here

        pygame.display.update()


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


# player vs bot
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
                        draw_text("Player 1 wins!", WHITE, width // 4, height // 3, screen)
                        pygame.display.update()
                        print("Player 1 wins!")
                        game_over = True
                    turn = 1  # Switch turn

        if turn == 1 and not game_over:  # Bot's turn
            print(f"Bot is thinking... {bot_agent}")
            col = bot_agent.best_move(board)  # Get best move from bot

            row = board.get_next_open_row(col)  # Get the next available row
            board.drop_piece(row, col, 2)  # Drop the piece for Bot

            print(board.board)

            if board.check_win(2):  # Check for a win for the Bot
                board.draw_board(screen)
                draw_text(" You Lose!", WHITE, width // 4, height // 3, screen)
                pygame.display.update()
                print("Bot wins!")
                game_over = True
            turn = 0  # Switch turn to player

        if board.is_full() and not game_over:  # Check for a draw
            board.draw_board(screen)
            draw_text("Its a Draw!", WHITE, width // 4, height // 3, screen)
            pygame.display.update()
            print("It's a draw!")
            game_over = True
            break

    wait_for_exit(screen)


def wait_for_exit(screen):
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    HomePage()
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1, 0.0)
