import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import sklearn


class ML_Agent:
    def __init__(self):
        pass

    def preprocess_data(self, data):

        data = data.replace({'X': 1, 'O': -1, 'b': 0})
        return data
    
    def board_to_features(self,board, turn_count):

        features = []
        for pos in board:
            if pos == 'X':
                features.append(1)
            elif pos == 'O':
                features.append(-1)
            else:
                features.append(0)


        features.append(turn_count)
        return features
    
    def train_model(self,data):
    # Features (board positions) and Target (BestMove)
        X = data[['TL', 'TM', 'TR', 'ML', 'MM', 'MR', 'BL', 'BM', 'BR']]
        y = data['BestMove']

    # Add turn count as a feature for model training (which will be added during the game loop)

        X['turn_count'] = data['BestMove'] % 9 # Using the BestMove as an indicator

    # Scale features to normalize them
        scaler = preprocessing.StandardScaler()
        X_scaled = scaler.fit_transform(X)

    # Train a Support Vector Machine (SVM) model
        model = SVC(kernel='linear', random_state=42)
        model.fit(X_scaled, y)

        return model, scaler, X_scaled, y
    
    def check_win(self, board, piece):
            # Horizontal Check
            for r in range(6):
                for c in range(4):
                    if all(board[r][c+i] == piece for i in range(4)):
                        return True

            # Vertical Check
            for r in range(3):
                for c in range(7):
                    if all(board[r+i][c] == piece for i in range(4)):
                        return True

            # Diagonal Down-Right Check
            for r in range(3):
                for c in range(4):
                    if all(board[r+i][c+i] == piece for i in range(4)):
                        return True

            # Diagonal Down-Left Check
            for r in range(3):
                for c in range(3, 7):
                    if all(board[r+i][c-i] == piece for i in range(4)):
                        return True

            return False
    
    def check_block_move(self,board, player):
        for i in range(9):
            if board[i] == 'b':  # Empty space
                board[i] = player  # Temporarily make the move for the player
                if self.check_win(board, player):  # Check if this move results in a win
                    board[i] = 'b'  # Reset the move
                    return i  # This is the blocking move
                board[i] = 'b'  # Reset the move
        return -1  # No blocking move needed
    
    def get_best_move(self,model, scaler, board, turn_count):
 
    # Check if there are any winning or blocking opportunities
        block_move = self.check_block_move(board, 'O')  # Check if we need to block opponent
        if block_move != -1:
            return block_move  # Block the opponent if a win is imminent

    # If no immediate blocking is needed, predict based on the trained model
        board_features = np.array(self.board_to_features(board, turn_count)).reshape(1, -1)
        board_features_scaled = scaler.transform(board_features)
        return model.predict(board_features_scaled)[0]


