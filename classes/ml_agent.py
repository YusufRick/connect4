import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

class ML_Agent:
    def __init__(self):
        pass

    # Preprocesses the dataset to replace 'x', 'o', and 'b' with 1, -1, and 0 respectively
    def preprocess_data(self, data):
        data = data.replace({'x': 1, 'o': -1, 'b': 0})
        return data

    # Convert a board to feature vector including the turn count
    def board_to_features(self, board, turn_count):
        features = []
        for pos in board:
            if pos == 'x':
                features.append(1)
            elif pos == 'o':
                features.append(-1)
            else:
                features.append(0)
        features.append(turn_count)  # Add turn count as the last feature
        return features
    
    def get_Best_Move(self):
        pass

    # Train model using SVM (Support Vector Machine)
    def train_model(self, data):
        # Features (board positions) and Target (BestMove)
        X = data[[  'a1','a2','a3','a4','a5','a6',
                    'b1','b2','b3','b4','b5','b6',  
                    'c1','c2','c3','c4','c5','c6',  
                    'd1','d2','d3','d4','d5','d6', 
                    'e1','e2','e3','e4','e5','e6',  
                    'f1','f2','f3','f4','f5','f6',  
                    'g1','g2','g3','g4','g5','g6']]  

        y = data['BestMove']  # function to get best move
        

        # Scale features to normalize them
        scaler = preprocessing.StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train a Support Vector Machine (SVM) model
        model = SVC(kernel='linear', random_state=42)
        model.fit(X_scaled, y)

        return model, scaler

    # Check if the current board has a winning configuration for the given player
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
    
    # Check if there are any blocking moves for the AI (to stop opponent from winning)
    def check_block_move(self, board, player):
        for i in range(9):
            if board[i] == 0:  # Empty space
                board[i] = player  # Temporarily make the move for the player
                if self.check_win(board, player):  # Check if this move results in a win
                    board[i] = 0  # Reset the move
                    return i  # This is the blocking move
                board[i] = 0  # Reset the move
        return -1  # No blocking move needed
    
    # Get the best move based on the trained model and current board state
    def get_best_move(self, model, scaler, board, turn_count):
        # Check if there are any winning or blocking opportunities
        block_move = self.check_block_move(board, -1)  # Opponent is 'o' (-1)
        if block_move != -1:
            return block_move  # Block the opponent if a win is imminent

        # If no immediate blocking is needed, predict based on the trained model
        board_features = np.array(self.board_to_features(board, turn_count)).reshape(1, -1)
        board_features_scaled = scaler.transform(board_features)
        return model.predict(board_features_scaled)[0]
        
# Loading data
data = pd.read_csv('../connect+4/connect-4.csv')  # Replace with your file path
data = ML_Agent().preprocess_data(data)  # Preprocess the data

# Train the model
model, scaler = ML_Agent().train_model(data)

# Example usage in a game

turn_count = 10  # Example turn count

# Get the best move from the ML Agent
best_move = ML_Agent().get_best_move(model, scaler, board, turn_count)
print(f"Best move predicted: {best_move}")


# replace a6-a1 samoai habis
#rotate the board

''' draw
b,b,b,b,b,b,b,
b,b,b,b,b,b,b,
o,x,o,b,b,b,b,
b,b,b,b,x,o,x,
b,b,b,b,b,o,b,
b,b,b,b,b,b,x,

b,b,b,b,b,b,x,
b,b,b,b,b,o,b,
b,b,b,b,x,o,x,
o,x,o,b,b,b,b,
b,b,b,b,b,b,b,
b,b,b,b,b,b,b,draw

b,b,b,b,b,b,
x,b,b,b,b,b,
o,b,b,b,b,b,
x,o,x,o,x,o,
b,b,b,b,b,b,
b,b,b,b,b,b,
b,b,b,b,b,b,draw

b,b,b,b,b,b,
b,b,b,b,b,b,
x,o,b,b,b,b,
x,o,x,o,x,o,
b,b,b,b,b,b,
b,b,b,b,b,b,
b,b,b,b,b,b,win



'''
