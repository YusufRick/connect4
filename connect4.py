
from ucimlrepo import fetch_ucirepo
import pygame
import sys
import numpy as np
import math
from classes.random_agent import Random_Agent
from classes.random_agent import Smart_Agent
from classes.minimax_agent import Minimax_Agent
from classes.minimax_agent2 import MiniMax2
from classes.ml_agent2 import MLAgent2
from classes.ml_agent import MLAgent
from classes.board import Board


#board constant
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

#load data from dataset library
connect_4 = fetch_ucirepo(id=26)

#colours
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

pygame.init()
#font style

BUTTON_FONT = pygame.font.SysFont("Arial", 30, bold=True)

# Homepage

# draw text to the screen
def draw_text(text, color, x, y, screen):
    font = pygame.font.SysFont("Arial", 40)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

#draw rectangle button and mouse click eventListener
def draw_button(x, y, w, h, text, screen):

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, BLUE, rect)

    txt_surf = BUTTON_FONT.render(text, True, YELLOW)
    txt_x    = x + (w - txt_surf.get_width()) // 2
    txt_y    = y + (h - txt_surf.get_height()) // 2
    screen.blit(txt_surf, (txt_x, txt_y))

    return rect

def HomePage():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")
    #title
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    title_surf = title_font.render("Welcome to Connect 4", True, YELLOW)
    title_x = (width - title_surf.get_width()) // 2
    title_y = height // 4  
    
    game_running = True
    while game_running:
        screen.fill(BLACK)
        
        # draw the bold, centered title
        screen.blit(title_surf, (title_x, title_y))
        
        # three buttons for model selection
        btn1 =draw_button((width-300)//2, title_y + 80, 300, 60, "Player vs Player", screen)
        btn2 =draw_button((width-300)//2, title_y + 160, 300, 60, "Player vs Bot",    screen)
        btn3=draw_button((width-300)//2, title_y + 240, 300, 60, "Bot vs Bot",       screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # On click, go to the appropriate setup function
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn1.collidepoint(mx, my):
                    start_player_vs_player()
                    return
                elif btn2.collidepoint(mx, my):
                    choose_bot_agent()
                    return
                elif btn3.collidepoint(mx, my):
                    choose_bot_v_bot()
                    return

        pygame.display.update()



# Choose Bot for player v bot
def choose_bot_agent():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Select Bot Agent")

    #function to train machine learning bot
    def _make_ml(bot):
        
        X = connect_4.data.features.replace({'x':1,'o':2,'b':0}).astype(int)
        y = connect_4.data.targets.replace({'win':0,'draw':1,'loss':2})
        bot.load_data(X, y)
        bot.train()
        return bot
    
    #list of agents
    options = [
        ("Random Agent",  lambda: Random_Agent(2,1,0)),
        ("Smart Agent",   lambda: Smart_Agent(2,1,0)),
        ("MiniMax Agent", lambda: Minimax_Agent(2,1,0)),
        ("MiniMax Agent 2", lambda: MiniMax2(2,1,0)),
        ("ML Agent",      lambda: _make_ml(MLAgent(2,1,0))),
        ("ML Agent 2",    lambda: _make_ml(MLAgent2(2,1,0))),
    ]

    cols       = 2
    spacing_x  = 40
    spacing_y  = 40
    btn_h      = 70
    btn_w      = (width - spacing_x * (cols + 1)) // cols
    #title
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    title_s    = title_font.render("Choose your Bot", True, YELLOW)
    title_x    = (width - title_s.get_width()) // 2
    title_y    = spacing_y

    while True:
        screen.fill(BLACK)

        # draw the title
        screen.blit(title_s, (title_x, title_y))

        # Draw option buttons in a grid
        btn_rects = []
        for idx, (label, factory) in enumerate(options):
            row = idx // cols

            # if selection is odd, centralised
            if idx == len(options) - 1 and len(options) % cols == 1:
                bx = (width - btn_w) // 2
            else:
                col = idx % cols
                bx  = spacing_x + col * (btn_w + spacing_x)

            by = title_y + title_s.get_height() + spacing_y + row * (btn_h + spacing_y)

            rect = draw_button(bx, by, btn_w, btn_h, label, screen)
            btn_rects.append((rect, factory))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                for rect, factory in btn_rects:
                    if rect.collidepoint(mx, my):
                        bot = factory()
                        return choose_player_order(bot)

        pygame.display.update()








# pvp
def start_player_vs_player():

    #initialized board
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
            # preview token on top
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE)) 
                posx = event.pos[0]
                #turn =0, colour red
                # turn = 1 colour yellow
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)


            #on click, drop the piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                # Get the column based on the mouse position
                col = int(posx // SQUARESIZE) 
                # Check if the column is not full
                if board.board[0][col] == 0:  
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

                        draw_text(f"Player {piece} wins!", YELLOW,width//4, height//13, screen)
                        pygame.display.update()
                        wait_for_exit(screen)
                        
                        game_over = True

                    if board.is_full():  # Check for a draw
                        board.draw_board( screen)
                        pygame.display.update()
                        pygame.time.wait(500)
                        print("It's a draw!")
                        draw_text("It's a draw!", YELLOW, width // 4, height//13, screen)
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

         
                    # Redraw the board after the move
                    board.draw_board(screen) 
                    print(board)

    wait_for_exit(screen)

# Bot v Bot
def choose_bot_v_bot():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Select Two Bot Agents")
    
    # function to train machine learning agent with dataset
    def _make_ml(cls, piece, opp, turn):
        bot = cls(piece, opp, turn)
        X = connect_4.data.features.replace({'x':1,'o':2,'b':0}).astype(int)
        y = connect_4.data.targets.replace({'win':0,'draw':1,'loss':2})
        bot.load_data(X, y)
        bot.train()
        return bot

    # definitions for both stages
    options_stage1 = [
        ("Random Agent",  lambda: Random_Agent(1, 2, 0)),
        ("Smart Agent",   lambda: Smart_Agent(1, 2, 0)),
        ("MiniMax Agent", lambda: Minimax_Agent(1, 2, 0)),
        ("MiniMax Agent 2", lambda: MiniMax2(1, 2, 0)),
        ("ML Agent",      lambda: _make_ml(MLAgent, 1, 2, 0)),
        ("ML Agent 2",    lambda: _make_ml(MLAgent2,1, 2, 0)),
    ]
    options_stage2 = [
        ("Random Agent",  lambda: Random_Agent(2, 1, 1)),
        ("Smart Agent",   lambda: Smart_Agent(2, 1, 1)),
        ("MiniMax Agent", lambda: Minimax_Agent(2, 1, 1)),
        ("MiniMax Agent 2", lambda: MiniMax2(2, 1, 1)),
        ("ML Agent",      lambda: _make_ml(MLAgent, 2, 1, 1)),
        ("ML Agent 2",    lambda: _make_ml(MLAgent2,2, 1, 1)),
    ]

    # grid layout 
    cols       = 2
    spacing_x  = 40
    spacing_y  = 40
    btn_h      = 70
    btn_w      = (width - spacing_x * (cols + 1)) // cols

    # prepare title font
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    stage1_s   = title_font.render("Choose the first Bot", True, YELLOW)
    stage2_s   = title_font.render("Choose the second Bot", True, YELLOW)
    title_x    = (width - stage1_s.get_width()) // 2
    title_y    = spacing_y

    bot1 = None

    # picking bot1
    while bot1 is None:
        screen.fill(BLACK)
        screen.blit(stage1_s, (title_x, title_y))

        btn_rects = []
        for idx, (label, factory) in enumerate(options_stage1):
            row = idx // cols
            col = idx % cols

            # center last if odd
            if idx == len(options_stage1) - 1 and len(options_stage1) % cols == 1:
                bx = (width - btn_w) // 2
            else:
                bx = spacing_x + col * (btn_w + spacing_x)

            by   = title_y + stage1_s.get_height() + spacing_y + row * (btn_h + spacing_y)
            rect = draw_button(bx, by, btn_w, btn_h, label, screen)
            btn_rects.append((rect, factory))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                for rect, factory in btn_rects:
                    if rect.collidepoint(mx, my):
                        bot1 = factory()
                        break

    # Pick bot 2
    bot2 = None
    while bot2 is None:
        screen.fill(BLACK)
        screen.blit(stage2_s, (title_x, title_y))

        btn_rects = []
        for idx, (label, factory) in enumerate(options_stage2):
            row = idx // cols
            col = idx % cols

            if idx == len(options_stage2) - 1 and len(options_stage2) % cols == 1:
                bx = (width - btn_w) // 2
            else:
                bx = spacing_x + col * (btn_w + spacing_x)

            by   = title_y + stage2_s.get_height() + spacing_y + row * (btn_h + spacing_y)
            rect = draw_button(bx, by, btn_w, btn_h, label, screen)
            btn_rects.append((rect, factory))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                for rect, factory in btn_rects:
                    if rect.collidepoint(mx, my):
                        bot2 = factory()
                        break

    # start bot v bot
    start_bot_vs_bot(bot1, bot2)




# Bot v Bot 
def start_bot_vs_bot(bot1, bot2):
    #initialise board
    board = Board()  
    game_over = False
    turn = 0
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4 - Bot vs Bot")

    while not game_over:
        board.draw_board(screen) # draw board
        pygame.display.update()
         # Bot 1's turn
        if turn == 0:  
            print("Bot 1 is thinking...")
            col = bot1.best_move(board)  
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, 1)  
            print(board.board)
            # check if bot 1 wins
            if board.check_win(1):  
                board.draw_board(screen)
                pygame.display.update()
                draw_text("Bot 1 wins!", YELLOW, width // 4, height//13, screen)
                pygame.display.update()
                wait_for_exit(screen)
                print("Bot 1 wins!")
                game_over = True

            turn = 1  # Switch to Bot 2

        if turn == 1:  # Bot 2's turn
            print("Bot 2 is thinking...")
            # get bot 2 best move
            col = bot2.best_move(board)  
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, 2)  
            print(board.board)

            # Bot 2 wins
            if board.check_win(2):  
                board.draw_board(screen)
                pygame.display.update()
                print("Bot 2 wins!")
                draw_text("Bot 2 wins!", YELLOW, width // 4, height//13, screen)
                pygame.display.update()
                wait_for_exit(screen)
                game_over = True

            turn = 0  # Switch to Bot 1
        # draw will end at bot's 2 turn since it has 42 blank space
        if board.is_full() and not game_over:  
            board.draw_board(screen)
            pygame.display.update()
            print("It's a draw!")
            game_over = True

    pygame.quit()



# player vs bot
def start_player_vs_bot(bot_agent, human_piece, bot_piece,turn):
    board = Board()
    game_over = False
    # piece 1 (red) piece 2 (yellow)

    # if player starts first, turn is set to 0
    # else turn starts at turn = 1

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

            # Show preview of human piece 
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    
                    pygame.draw.circle(screen, preview_color,(posx, SQUARESIZE//2), RADIUS)
                else:
                    
                    pygame.draw.circle(screen, YELLOW,(posx, SQUARESIZE//2), RADIUS)
                
            # Player's turn
            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)
                # Check if column is not full
                if board.board[0][col] == 0:  
                    row = board.get_next_open_row(col) 
                    board.drop_piece(row, col, human_piece) 
                    print(board.board)
                     # Check for a win for Player 1
                    if board.check_win(human_piece):  
                        board.draw_board(screen)
                        draw_text("Player 1 wins!", YELLOW, width // 4, height//13, screen)
                        pygame.display.update()
                        print("Player 1 wins!")
                        game_over = True
                    turn = 1  # Switch turn
        # Bot's turn
        if turn == 1 and not game_over:  
            print(f"Bot is thinking...")
            col = bot_agent.best_move(board)  

            row = board.get_next_open_row(col)  
            board.drop_piece(row, col, bot_piece) 

            print(board.board)
             # Check for a win for the Bot
            if board.check_win(bot_piece):  
                board.draw_board(screen)
                draw_text(" You Lose!", YELLOW, width // 4, height//13, screen)
                pygame.display.update()
                print("Bot wins!")
                game_over = True
            turn = 0  # Switch turn to player

        if board.is_full() and not game_over: 
            board.draw_board(screen)
            draw_text("Its a Draw!", YELLOW, width // 4, height//13, screen)
            pygame.display.update()
            print("It's a draw!")
            game_over = True
            break

    wait_for_exit(screen)


def choose_player_order(bot_agent):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Choose Turn Order")

    # title style
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    title_surf = title_font.render("Who moves first?", True, YELLOW)
    title_x = (width  - title_surf.get_width())  // 2
    title_y = height // 4

    # Button dimensions
    btn_w, btn_h = 300, 60
    btn_x = (width - btn_w) // 2
    
    first_btn_y = title_y + title_surf.get_height() + 40

    options = [
        ("You go first",  0),  # turn=0 human first
        ("Bot goes first",1),  # turn=1  bot first
    ]

    while True:
        screen.fill(BLACK)
        # draw title
        screen.blit(title_surf, (title_x, title_y))

        # draw buttons and track their rects
        btn_rects = []
        for i, (label, turn_val) in enumerate(options):
            y = first_btn_y + i * (btn_h + 20)
            rect = draw_button(btn_x, y, btn_w, btn_h, label, screen)
            btn_rects.append((rect, turn_val))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for rect, turn_val in btn_rects:
                    if rect.collidepoint(mx, my):
                        
                        if turn_val == 0:  # human first
                            human_piece = 1
                            bot_piece =2
                        else:              # bot first
                            human_piece =2
                            bot_piece = 1

                        #Assign piece numbers and turns
                        bot_agent.ai_piece = bot_piece
                        bot_agent.opponent = human_piece
                        bot_agent.turn = turn_val
                        start_player_vs_bot(bot_agent, human_piece, bot_piece, turn_val)
                        return




def wait_for_exit(screen):
    #wait until player click and go to homepage
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False
                HomePage()


if __name__ == "__main__":
    # 1) Initialize the mixer and start the music up front
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("assets/Subway-Surfers-Theme-Sound-Effect.mp3")
        pygame.mixer.music.set_volume(0.5)        
        pygame.mixer.music.play(-1)               
    except pygame.error as e:
        print("Could not load music:", e)

 
    HomePage()
