import random
from classes.board import Board



    
class Random_Agent:
        def __init__(self):
            pass

        def best_move(self, board):
        # Get the list of available columns
            available_moves = board.get_available_moves()

        # Choose a random column from the available moves
            col = random.choice(available_moves)
            return col

    
    #Plays using a basic set of rules: win > block > random.
class Smart_Agent:
        def __init__(self):
            pass
        
        
        def best_move(self, board):
            # check for a winning move
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                board.make_move(col,2)

                if board.check_win(2):
                    board.board[row][col]=0  # Check if Player 2 can win
                    return col  # 
                board.board[row][col]=0

            # block opponent winning move
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                board.make_move(col,1)
                if board.check_win(1):
                    board.board[row][col]=0
                    return col  # Block the winning move
                
                board.board[row][col] = 0

            # Random move
            return random.choice(board.get_available_moves())

