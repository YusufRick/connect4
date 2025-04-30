
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from ucimlrepo import fetch_ucirepo
import random

class MLAgent:
    def __init__(self, ai_piece, opponent, turn):
        self.turn = turn
        self.ai_piece = ai_piece
        self.opponent = opponent
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.X = None
        self.y = None
        self.trained = False
        self.board_map = {'x': 1, 'o': 2, 'b': 0}  # Encoding for board states
        self.result_map = {'win': 0, 'loss': 1, 'draw': 2}  # Encoding for outcomes

    def load_data(self, X, y):
 
        # Preprocess the features dataset (board state)
        X = X.replace(self.board_map)
        X = X.astype(int)
        
        # Preprocess the outcome labels
        y = y.replace(self.result_map).astype(int).values.ravel()

        self.X = X
        self.y = y

    def train(self):
 
        if self.X is None or self.y is None:
            raise ValueError("Data not loaded.")
        
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        
        # Train the RandomForest model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = self.model.score(X_test, y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")
        print(classification_report(y_test, y_pred))
        
        self.trained = True

    def best_move(self, board):
        if not self.trained:
            raise Exception("Model not trained yet.")
        
        best_col = -1
        best_score = 3
        center_col=3
        best_distance = float('inf')

        # Check for winning move (maximize AI's win)
        for col in range(7):
            row = board.get_next_open_row(col)
            if row == -1:
                continue

            b1 = board.copy()
            b1.drop_piece(row, col, self.ai_piece)

            if b1.check_win(self.ai_piece):
                return col

        # Block opponent's winning move
        for col in range(7):
            row = board.get_next_open_row(col)
            b1 = board.copy()
            b1.drop_piece(row, col, self.opponent)

            if b1.check_win(self.opponent):
                return col

        #  Evaluate each possible move using ML model
        for move_col in range(7):
        # find where our piece would land
            move_row = board.get_next_open_row(move_col)
            if move_row < 0:
                continue
            b1 = board.copy()
            b1.drop_piece(row, col, self.ai_piece)

            # flatten to a 42‐element list in UCI order (a1,a2…a6,b1,…g6)
            
            flat = []
            for c in range(7):
                for r in range(5, -1, -1):           
                    flat.append(int(b1.board[r][c]))

            # convert into 1d array to match dataset format
            # print(flat)
            

            # build the single-row DataFrame for your model
            input_df = pd.DataFrame([flat], columns=self.model.feature_names_in_)
            pred = self.model.predict(input_df)[0]

            # If Ai move first, look for "win"
            # if Ai is the second player, look for "loss"
            if self.ai_piece == 1:
                
                if pred == 0:
                    return move_col
                if pred == 2:
                    score = 1 
                else:
                    score =2
            else:
                
                if pred == 1:
                    return move_col
                if pred == 2:
                    score = 1 
                else:
                    score=2

            # closest distance to centre
            dist = abs(move_col - center_col)
            if (score < best_score) or (score == best_score and dist < best_distance):
                best_score, best_col, best_distance = score, move_col, dist

        return best_col