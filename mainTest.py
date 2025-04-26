# test_ml_agent.py
from ucimlrepo import fetch_ucirepo
import pygame
import sys
import numpy as np
import math
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent
from classes.minimax_agent import Minimax_Agent
from classes.test_RandomForestClassifier import MLAgent

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
                    choose_player_order(Random_Agent(2,1,0))

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                    print("Smart Agent selected")
                    choose_player_order(Smart_Agent(2,1,0))

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 120 <= posy <= height // 2 + 120 + 60:
                    print("MiniMax Agent selected")
                    choose_player_order(Minimax_Agent(2,1,0))

                elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 220 <= posy <= height // 2 + 220 + 60:
                    print("ML Agent selected")
                    ml_agent = MLAgent(2,1,0)
                    X = connect_4.data.features
                    X = X.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)


                    y = connect_4.data.targets
                    y = y.replace({'win': 0, 'draw': 1, 'loss': 2})
                    ml_agent.load_data(X, y) 
                    ml_agent.train()
                    choose_player_order(ml_agent)  # Use ML Agent here

        pygame.display.update()

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
                    row = board.get_next_open_row(col)  
                    if turn ==0:
                        piece = 1
                    else:
                        piece = 2
                    board.drop_piece(row, col,piece)

                    board.draw_board(screen)
                    pygame.display.update()
                    

                    # check win for every turn
                    if board.check_win(piece): 
                        board.draw_board(screen)
                        pygame.display.update()
                        pygame.time.wait(500)

                        draw_text(f"Player {piece} wins!", WHITE,width//4, height//3, screen)
                        pygame.display.update()
                        wait_for_exit(screen)
                        
                        game_over = True

                    if board.is_full():  # Check for a draw
                        board.draw_board( screen)
                        pygame.display.update()
                        pygame.time.wait(500)
                        print("It's a draw!")
                        draw_text("It's a draw!", WHITE, width // 4, height // 3, screen)
                        pygame.display.update()
                        wait_for_exit(screen)

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

    wait_for_exit(screen)

# Bot v Bot
def choose_bot_v_bot():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Select Two Bot Agents")

    game_running = True
    bot1 = None  # Initialize bot1
    bot2 = None  # Initialize bot2

    while game_running:
        screen.fill(RED)
        
        if not bot1:  # First bot selection screen
            draw_text("Choose the first Bot", BLACK, width // 4, height // 4, screen)
            draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
            draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
            draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)
            draw_button(width // 4, height // 2 + 220, "ML Agent", screen)  # Add ML Agent option

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    posy = event.pos[1]

                    if width // 3 <= posx <= width // 3 + 200 and height // 2 - 80 <= posy <= height // 2 - 80 + 60:
                        print("Random Agent selected as Bot 1")
                        bot1 = Random_Agent(1,2,0)

                    elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                        print("Smart Agent selected as Bot 1")
                        bot1 = Smart_Agent(1,2,0)

                    elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 120 <= posy <= height // 2 + 120 + 60:
                        print("MiniMax Agent selected as Bot 1")
                        bot1 = Minimax_Agent(1,2,0)

                    elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 220 <= posy <= height // 2 + 220 + 60:
                        print("ML Agent selected as Bot 1")
                        bot1 = MLAgent(1,2,0)  # ML Agent, passing player and opponent pieces and turn
                        X = connect_4.data.features
                        X = X.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)


                        y = connect_4.data.targets
                        y = y.replace({'win': 0, 'draw': 1, 'loss': 2})
                        bot1.load_data(X, y) 
                        bot1.train()

            pygame.display.update()

        # After bot1 is selected, move to bot2 selection
        if bot1:
            screen.fill(RED)
            draw_text("Choose the second Bot", BLACK, width // 4, height // 4, screen)
            draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
            draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
            draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)
            draw_button(width // 4, height // 2 + 220, "ML Agent", screen)  # Add ML Agent option

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx2 = event.pos[0]
                    posy2 = event.pos[1]

                    if width // 3 <= posx2 <= width // 3 + 200 and height // 2 - 80 <= posy2 <= height // 2 - 80 + 60:
                        print("Random Agent selected as Bot 2")
                        bot2 = Random_Agent(2,1,1)

                    elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 20 <= posy2 <= height // 2 + 20 + 60:
                        print("Smart Agent selected as Bot 2")
                        bot2 = Smart_Agent(2,1,1)

                    elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 120 <= posy2 <= height // 2 + 120 + 60:
                        print("MiniMax Agent selected as Bot 2")
                        bot2 = Minimax_Agent(2,1,1)

                    elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 220 <= posy2 <= height // 2 + 220 + 60:
                        print("ML Agent selected as Bot 2")
                        bot2 = MLAgent(2,1,1)  # ML Agent, passing player and opponent pieces and turn

                    start_bot_vs_bot(bot1, bot2)  # Start Bot vs Bot game
                    return  # Exit the function after starting the game

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
            col = bot1.best_move(board)  # Bot 1 predicts move
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, 1)  # Make move for Bot 1
            print(board.board)

            if board.check_win(1):  # Bot 1 wins
                board.draw_board(screen)
                pygame.display.update()
                draw_text("Bot 1 wins!", WHITE, width // 4, height // 3, screen)
                pygame.display.update()
                wait_for_exit(screen)
                print("Bot 1 wins!")
                game_over = True

            turn = 1  # Switch to Bot 2

        if turn == 1:  # Bot 2's turn
            print("Bot 2 is thinking...")
            col = bot2.best_move(board)  # Bot 2 predicts move
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, 2)  # Make move for Bot 2
            print(board.board)

            if board.check_win(2):  # Bot 2 wins
                board.draw_board(screen)
                pygame.display.update()
                print("Bot 2 wins!")
                draw_text("Bot 2 wins!", WHITE, width // 4, height // 3, screen)
                pygame.display.update()
                wait_for_exit(screen)
                game_over = True

            turn = 0  # Switch to Bot 1

        if board.is_full() and not game_over:  # Check for a draw
            board.draw_board(screen)
            pygame.display.update()
            print("It's a draw!")
            game_over = True

    pygame.quit()


#choose bot v bot


def choose_bot_v_bot():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Select Two Bot Agents")

    game_running = True
    bot1 = None  # Initialize bot1
    bot2 = None  # Initialize bot2

    while game_running:
        screen.fill(RED)
        
        if not bot1:  # First bot selection screen
            draw_text("Choose the first Bot", BLACK, width // 4, height // 4, screen)
            draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
            draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
            draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)
            draw_button(width // 4, height // 2 + 220, "ML Agent", screen)  # Add ML Agent option

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    posy = event.pos[1]

                    if width // 3 <= posx <= width // 3 + 200 and height // 2 - 80 <= posy <= height // 2 - 80 + 60:
                        print("Random Agent selected as Bot 1")
                        bot1 = Random_Agent(1,2,0)

                    elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 20 <= posy <= height // 2 + 20 + 60:
                        print("Smart Agent selected as Bot 1")
                        bot1 = Smart_Agent(1,2,0)

                    elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 120 <= posy <= height // 2 + 120 + 60:
                        print("MiniMax Agent selected as Bot 1")
                        bot1 = Minimax_Agent(1,2,0)

                    elif width // 3 <= posx <= width // 3 + 200 and height // 2 + 220 <= posy <= height // 2 + 220 + 60:
                        print("ML Agent selected as Bot 1")
                        bot1 = MLAgent(1,2,0)
                        X = connect_4.data.features
                        X = X.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)


                        y = connect_4.data.targets
                        y = y.replace({'win': 0, 'draw': 1, 'loss': 2})
                        bot1.load_data(X, y) 
                        bot1.train()  

            pygame.display.update()

        # After bot1 is selected, move to bot2 selection
        if bot1:
            screen.fill(RED)
            draw_text("Choose the second Bot", BLACK, width // 4, height // 4, screen)
            draw_button(width // 4, height // 2 - 80, "Random Agent", screen)
            draw_button(width // 4, height // 2 + 20, "Smart Agent", screen)
            draw_button(width // 4, height // 2 + 120, "MiniMax Agent", screen)
            draw_button(width // 4, height // 2 + 220, "ML Agent", screen)  # Add ML Agent option

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx2 = event.pos[0]
                    posy2 = event.pos[1]

                    if width // 3 <= posx2 <= width // 3 + 200 and height // 2 - 80 <= posy2 <= height // 2 - 80 + 60:
                        print("Random Agent selected as Bot 2")
                        bot2 = Random_Agent(2,1,0)

                    elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 20 <= posy2 <= height // 2 + 20 + 60:
                        print("Smart Agent selected as Bot 2")
                        bot2 = Smart_Agent(2,1,0)

                    elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 120 <= posy2 <= height // 2 + 120 + 60:
                        print("MiniMax Agent selected as Bot 2")
                        bot2 = Minimax_Agent(2,1,0)

                    elif width // 3 <= posx2 <= width // 3 + 200 and height // 2 + 220 <= posy2 <= height // 2 + 220 + 60:
                        print("ML Agent selected as Bot 2")
                        bot2 = MLAgent(2,1,0)
                        X = connect_4.data.features
                        X = X.replace({'x': 1, 'o': 2, 'b': 0}).astype(int)


                        y = connect_4.data.targets
                        y = y.replace({'win': 0, 'draw': 1, 'loss': 2})
                        bot2.load_data(X, y) 
                        bot2.train()

                    start_bot_vs_bot(bot1, bot2)
                    return  # Exit the function after starting the game

            pygame.display.update()



# player vs bot
def start_player_vs_bot(bot_agent, human_piece, bot_piece,turn):
    board = Board()
    game_over = False
    # 0 = Red, 1 = Yellow

    if turn == 0:
        preview_color = RED
    else:
        preview_color = YELLOW

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
                if turn == 0:
                    # human goes by red piece
                    pygame.draw.circle(screen, preview_color,(posx, SQUARESIZE//2), RADIUS)
                else:
                    # bots turn change the piece to yellow
                    
                    pygame.draw.circle(screen, YELLOW,(posx, SQUARESIZE//2), RADIUS)
                

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  # Player's turn
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if board.board[0][col] == 0:  # Check if column is not full
                    row = board.get_next_open_row(col)  # Get next available row
                    board.drop_piece(row, col, human_piece)  # Drop the piece for Player 1
                    print(board.board)

                    if board.check_win(human_piece):  # Check for a win for Player 1
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
            board.drop_piece(row, col, bot_piece)  # Drop the piece for Bot

            print(board.board)

            if board.check_win(bot_piece):  # Check for a win for the Bot
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


def choose_player_order(bot_agent):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Choose Turn Order")

    while True:
        screen.fill(RED)
        draw_text("Who moves first?", BLACK, width//3, height//4, screen)
        draw_button(width//4, height//2 - 80, "You go first", screen)
        draw_button(width//4, height//2 + 20, "Bot goes first", screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                # bounds of “You go first” button
                if width//4 <= x <= width//4 + 400 and height//2 - 80 <= y <= height//2 - 80 + 70:
                    human_piece = 1
                    bot_piece = 2
                    turn = 0
                # bounds of “Bot goes first” button
                elif width//4 <= x <= width//4 + 400 and height//2 + 20 <= y <= height//2 + 20 + 70:
                    human_piece =2
                    bot_piece =1
                    turn = 1
                else:
                    continue
                
                bot_agent.ai_piece = bot_piece
                bot_agent.opponent = human_piece
                bot_agent.turn = turn
                start_player_vs_bot(bot_agent, human_piece, bot_piece,turn)
                return




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
