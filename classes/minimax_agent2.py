import random
import math

class MiniMax2:
    def __init__(self, agent, opponent, turn):
        self.ai_piece  = agent
        self.opponent  = opponent
        self.turn      = turn
        self.depth = 5

        # reward based on how many pieces in a row
        #penalized if opponents can connect 3 pieces
    def evaluate_window(self, window, piece):
        score = 0
        

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(self.opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score

    #favoring center column
    def score_position(self, board_obj, piece):

        arr = board_obj.board
        score = 0
        center_col = 7 // 2

        # centre column
        center_array = list(arr[:, center_col])
        score += center_array.count(piece) * 3

        # horizontal 
        for r in range(6):
            row_array = list(arr[r, :])
            for c in range(7 - 3):
                window = row_array[c : c + 4]
                score += self.evaluate_window(window, piece)

        # vertical 
        for c in range(7):
            col_array = list(arr[:, c])
            for r in range(6 - 3):
                window = col_array[r : r + 4]
                score += self.evaluate_window(window, piece)

        # diagonals
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [arr[r + i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [arr[r + 3 - i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score
    # check the roots of tree (win,lose,draw)
    def is_terminal_node(self, board):
        return board.check_win(self.opponent) or board.check_win(self.ai_piece) or board.is_full()

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_available_moves()
        is_terminal = self.is_terminal_node(board)

        #if it hits terminal or depth is 0, evaluate the board
        if depth == 0 or is_terminal:

            if is_terminal:

                #if ai wins, rewards with inf
                #if opponent wins penalized -inf
                if board.check_win(self.ai_piece):
                    return (None, math.inf)
                elif board.check_win(self.opponent):
                    return (None, -math.inf)
                else:
                    return None, 0
            else:
                #if terminal havent been reached, score the position
                return None, self.score_position(board, self.ai_piece)

        if maximizingPlayer:
            value, column = -math.inf, random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.ai_piece)
                _, eval = self.minimax(b_copy, depth - 1, alpha, beta, False)
                if eval > value:
                    value, column = eval, col
                alpha = max(alpha, value)

                #if alpha(ai) score is > than beta(opponent), stop exploring
                if alpha >= beta:
                    break
            return column, value
        else:

            #minimizing opponents move
            value, column = math.inf, random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.opponent)
                _, eval = self.minimax(b_copy, depth - 1, alpha, beta, True)
                if eval < value:
                    value, column = eval, col
                beta = min(beta, value)

                #if alpha(ai) score is > than beta(opponent), stop exploring
                if alpha >= beta:
                    break
            return column, value

    def best_move(self, board):

        #check every possible move
        for col in range(7):
            row = board.get_next_open_row(col)
            if row == -1:
                continue

            b_copy = board.copy()
            #check if theres an instant win
            b_copy.drop_piece(row, col, self.ai_piece)
            if b_copy.check_win(self.ai_piece):
                return col

        # use minimax based on current position.
        col, _score = self.minimax(board,self.depth,alpha=-math.inf,beta=+math.inf,maximizingPlayer=True)
        # if not, use random moves in all available moves.
        valid = board.get_available_moves()
        return col if col in valid else random.choice(valid)
