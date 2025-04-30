import math
import random

class Minimax_Agent:
    def __init__(self, ai_player, opponent, turn):
        self.ai_player = ai_player
        self.opponent  = opponent
        self.turn      = turn
        self.depth     = 5

    def is_terminal(self, board):
        return (
            board.check_win(self.ai_player) or
            board.check_win(self.opponent) or
            board.is_full()
        )

    def evaluate_board(self, board):
        if board.check_win(self.ai_player):
            return math.inf
        if board.check_win(self.opponent):
            return -math.inf
        return 0

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal(board):
            return None, self.evaluate_board(board)

        if maximizing_player:
            value, best_col = -math.inf, None
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                # skip if column is full
                if row is None:
                    continue
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.ai_player)
                _, score = self.minimax(b_copy, depth-1, alpha, beta, False)
                if score > value:
                    value, best_col = score, col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value

        else:
            value, best_col = math.inf, None
            for col in board.get_available_moves():
                row = board.get_next_open_row(col)
                if row is None:
                    continue
                b_copy = board.copy()
                b_copy.drop_piece(row, col, self.opponent)
                _, score = self.minimax(b_copy, depth-1, alpha, beta, True)
                if score < value:
                    value, best_col = score, col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def best_move(self, board):
        # 1) immediate win?
        for col in board.get_available_moves():
            row = board.get_next_open_row(col)
            if row is None:
                continue
            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.ai_player)
            if b_copy.check_win(self.ai_player):
                return col

        # 2) block opponent’s win?
        for col in board.get_available_moves():
            row = board.get_next_open_row(col)
            if row is None:
                continue
            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.opponent)
            if b_copy.check_win(self.opponent):
                return col

        # 3) full minimax
        col, _ = self.minimax(board, self.depth, -math.inf, math.inf, True)
        valid = board.get_available_moves()
        return col if col in valid else random.choice(valid)
