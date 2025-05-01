import random



    
class Random_Agent:
        def __init__(self,agent,opponent,turn):
            self.agent = agent
            self.opponent = opponent
            self.turn = turn
            self.total_nodes = 0  

        def best_move(self, board):
        # Get the list of available columns
            self.total_nodes += 1 
            available_moves = board.get_available_moves()

        # Choose a random column from the available moves
            col = random.choice(available_moves)
            return col

    
    #Plays using a basic set of rules: win > block > random.
class Smart_Agent:
        def __init__(self,agent,opponent,turn):
            self.agent = agent
            self.opponent = opponent
            self.turn = turn
            self.total_nodes =0
        
        
        def best_move(self, board):
            # check for a winning move
            self.total_nodes += 1 
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                board.drop_piece(row,col,self.agent)

                if board.check_win(self.agent):
                    board.board[row][col]=0  # Check if Player 2 can win
                    return col  # 
                board.board[row][col]=0

            # block opponent winning move
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                board.drop_piece(row,col,self.opponent)
                if board.check_win(self.opponent):
                    board.board[row][col]=0
                    return col  # Block the winning move
                
                board.board[row][col] = 0

            # Random move
            return random.choice(board.get_available_moves())

