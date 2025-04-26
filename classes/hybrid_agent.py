import copy
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class MLAgent:
    def __init__(self, agent, opponent, turn):
        self.ai_piece = agent
        self.opponent = opponent
        self.turn = turn
        self.model = RandomForestClassifier(n_estimators=100)
        self.trained = False
        self.board_map = {'x': 1, 'o': 2, 'b': 0}
        self.result_map = {'win': 0, 'draw': 1, 'loss': 2}

    def load_data(self, X, y):
        X = X.replace(self.board_map).astype(int)
        y = y.replace(self.result_map).astype(int).values.ravel()
        self.X = X
        self.y = y

    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test
        self.trained = True

    def best_move(self, board):
        # Use ML model to choose the best move based on long-term strategy
        best_col, best_score = -1, -1.0
        for col in board.get_available_moves():
            b1 = copy.deepcopy(board)
            r1 = b1.get_next_open_row(col)
            b1.drop_piece(r1, col, self.ai_piece)
            flat = [cell for row in b1.board for cell in row]
            df = pd.DataFrame([flat], columns=self.X.columns).astype(int)
            probs = self.model.predict_proba(df)[0]
            score = probs[0] if self.ai_piece == 1 else probs[2]  # win for ai_piece 1, loss for ai_piece 2
            if score > best_score:
                best_score, best_col = score, col
        return best_col

class MinimaxAgent:
    def __init__(self, ai_piece, opponent, depth=3):
        self.ai_piece = ai_piece
        self.opponent = opponent
        self.depth = depth

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.check_win(self.ai_piece) or board.check_win(self.opponent):
            return self.evaluate_board(board)

        available_moves = board.get_available_moves()
        if maximizing_player:
            max_eval = -float('inf')
            best_move = None
            for move in available_moves:
                new_board = copy.deepcopy(board)
                row = new_board.get_next_open_row(move)
                new_board.drop_piece(row, move, self.ai_piece)
                eval_score = self.minimax(new_board, depth-1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval if depth == self.depth else best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in available_moves:
                new_board = copy.deepcopy(board)
                row = new_board.get_next_open_row(move)
                new_board.drop_piece(row, move, self.opponent)
                eval_score = self.minimax(new_board, depth-1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval if depth == self.depth else best_move

    def evaluate_board(self, board):
        # Evaluation function to assign scores to the board based on winning/losing scenarios
        if board.check_win(self.ai_piece):
            return 10  # Positive score for AI win
        elif board.check_win(self.opponent):
            return -10  # Negative score for opponent win
        else:
            return 0  # Draw or neutral

class HybridAgent:
    def __init__(self, agent, opponent, turn, depth=3):
        self.ml_agent = MLAgent(agent, opponent, turn)
        self.minimax_agent = MinimaxAgent(agent, opponent, depth)

    def best_move(self, board):
        # First, try to block or win using minimax
        best_move = self.minimax_agent.minimax(board, self.minimax_agent.depth, True)
        if best_move is not None:
            return best_move

        # If no immediate threat or winning move, use ML agent
        return self.ml_agent.best_move(board)

# Example usage:
# board = some Board object that has methods like get_available_moves, drop_piece, etc.
# hybrid_agent = HybridAgent(ai_piece=1, opponent=2, turn=1)
# best_move = hybrid_agent.best_move(board)
