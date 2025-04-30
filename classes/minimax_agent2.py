import random
import math

class MiniMax2:
    def __init__(self, agent, opponent, turn):
        self.ai_piece  = agent
        self.opponent  = opponent
        self.turn      = turn
        self.depth = 5

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.opponent

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, board_obj, piece):
        """
        board_obj: your Board instance, which has a .board attribute (6×7 numpy array)
        piece:     1 or 2
        """
        arr = board_obj.board
        score = 0
        center_col = 7 // 2

        # favor the center column
        center_array = list(arr[:, center_col])
        score += center_array.count(piece) * 3

        # horizontal windows
        for r in range(6):
            row_array = list(arr[r, :])
            for c in range(7 - 3):
                window = row_array[c : c + 4]
                score += self.evaluate_window(window, piece)

        # vertical windows
        for c in range(7):
            col_array = list(arr[:, c])
            for r in range(6 - 3):
                window = col_array[r : r + 4]
                score += self.evaluate_window(window, piece)

        # positive-slope diagonals
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [arr[r + i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # negative-slope diagonals
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [arr[r + 3 - i, c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return board.check_win(self.opponent) or board.check_win(self.ai_piece) or board.is_full()

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_available_moves()
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_win(self.ai_piece):
                    return (None, 100000000000000)
                elif board.check_win(self.opponent):
                    return (None, -100000000000000)
                else:
                    return None, 0
            else:
                
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
                if alpha >= beta:
                    break
            return column, value
        else:
            value, column = math.inf, random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.opponent)
                _, eval = self.minimax(b_copy, depth - 1, alpha, beta, True)
                if eval < value:
                    value, column = eval, col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def best_move(self, board):
        for col in range(7):
            row = board.get_next_open_row(col)
            if row == -1:
                continue

            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.ai_piece)

            if b_copy.check_win(self.ai_piece):
                return col

        # kick off the recursive minimax from the current position
        col, _score = self.minimax(board,self.depth,alpha=-math.inf,beta=+math.inf,maximizingPlayer=True)

        valid = board.get_available_moves()
        return col if col in valid else random.choice(valid)
