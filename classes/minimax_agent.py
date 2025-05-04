import math
import random

class Minimax_Agent:
    def __init__(self, ai_player, opponent, turn):
        self.ai_player = ai_player
        self.opponent  = opponent
        self.turn      = turn
        self.depth     = 5
        self.total_nodes = 0  # initialize node expansion count
        self.total_prunes = 0  # initialize prune count
        self.max_depth_reached = 0 

    
    #check the roots for each tree
    def is_terminal(self, board):
        return (
            board.check_win(self.ai_player) or
            board.check_win(self.opponent) or
            board.is_full()
        )
    # if ai wins, rewards inf
    # if opponent wins penalized -inf
    # 0 if draw
    def evaluate_board(self, board):
        if board.check_win(self.ai_player):
            return math.inf
        if board.check_win(self.opponent):
            return -math.inf
        return 0
    

    #

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        self.total_nodes+= 1
        current_level = self.depth - depth
        if current_level > self.max_depth_reached:
            self.max_depth_reached = current_level

        #if it reach depth 0, evaluate the board
        if depth == 0 or self.is_terminal(board):
            return None, self.evaluate_board(board)

        if maximizing_player:

            #start with worst score
            value, best_col = -math.inf, None

            #try every possible move,
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                # skip if column is full
                if row is None:
                    continue
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.ai_player)

                # recursive the miniax function
                _, score = self.minimax(b_copy, depth-1, alpha, beta, False)

                # if the move is better, replace it with current move
                if score > value:
                    value, best_col = score, col

                #update alpha
                alpha = max(alpha, value)

                #if alpha (the ai) is better than beta(opponents), stop explore
                if alpha >= beta:
                    self.total_prunes +=1  #  prune count + 1

                    break
            return best_col, value

        else:
            #minimizing opponents move
            #start with worst score
            value, best_col = math.inf, None
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                if row is None:
                    continue
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.opponent)
                _, score = self.minimax(b_copy, depth-1, alpha, beta, True)


                #if this move is worst, replace with current move
                if score < value:
                    value, best_col = score, col
                beta = min(beta, value)

                #if alpha is > than beta, stop exploring
                if alpha >= beta:
                    self.total_prunes +=1  # prune count + 1
                    

                    break
            return best_col, value

    def best_move(self, board):
        # 1) check if theres an instant win
        for col in board.get_available_moves():
            row = board.get_next_open_row(col)
            if row is None:
                continue
            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.ai_player)
            if b_copy.check_win(self.ai_player):
                return col

        # 2) block opponents winning move
        for col in board.get_available_moves():
            row = board.get_next_open_row(col)
            if row is None:
                continue
            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.opponent)
            if b_copy.check_win(self.opponent):
                return col

        # 3) use minimax to get best move
        col, _ = self.minimax(board, self.depth, -math.inf, math.inf, True)
        valid = board.get_available_moves()
        return col if col in valid else random.choice(valid)
