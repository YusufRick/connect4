import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

class ML_Agent:
    def __init__(self):
        pass


    def rotate_board_anticlockwise(self,board):
        return np.array(board).T[::-1]
    
    # # Preprocesses the dataset to replace 'x', 'o', and 'b' with 1, -1, and 0 respectively
    # def preprocess_data(self,data):
    #     processed_boards = []
    #     for index, row in data.iterrows():
    #         board_state = row.values[:-1].reshape(7, 6)  # reshape into 7 rows and 6 columns
    #         rotated_board = self.rotate_board_anticlockwise(board_state)
    #         processed_boards.append(rotated_board)
    #     return processed_boards

    def preprocess_data(self, data):
        processed_boards = []
        processed_labels = []

        # Define column names manually for the 7x6 grid and 'Outcome'
        columns = [f'{chr(97 + c)}{r+1}' for c in range(7) for r in range(6)]  # 'a1' to 'g6'
        columns.append('Outcome')  # Last column is for the outcome ('win', 'draw', 'loss')

        # Make sure the DataFrame has no column headers initially, and set them manually
        data.columns = columns
        
        # Process each row
        for index, row in data.iterrows():
            # Reshape the row into 7 columns and 6 rows (board layout)
            board_state = row.values[:-1].reshape(7, 6)  # Get the 7x6 board state
            rotated_board = self.rotate_board_anticlockwise(board_state)  # Rotate 90 degrees anticlockwise
            processed_boards.append(rotated_board)
            processed_labels.append(row['Outcome'])  # The last column is the outcome label

        return np.array(processed_boards), np.array(processed_labels)

    # Convert a board to feature vector including the turn count
    def board_to_features(self, board, turn_count):
        features = []
        for r in range(6):  # 6 rows in the board
            for c in range(7):  # 7 columns in the board
                features.append(board[r][c])
        features.append(turn_count)  # Add turn count as the last feature
        return features

    def train_model(self, data):
        # Preprocess the data
        boards, labels = self.preprocess_data(data)

        # Flatten the board states and prepare features and labels
        X = []
        for board in boards:
            features = self.board_to_features(board, 0)  # Assuming no turn count initially
            X.append(features)

        # Normalize the features
        scaler = preprocessing.StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train a Support Vector Machine (SVM) model
        model = SVC(kernel='linear', random_state=42)
        model.fit(X_scaled, labels)

        return model, scaler
    # Train model using SVM (Support Vector Machine)
    # def train_model(self, data):
    #     # Features (board positions) and Target (BestMove)
    #     X = data[[  'a1','a2','a3','a4','a5','a6',
    #                 'b1','b2','b3','b4','b5','b6',  
    #                 'c1','c2','c3','c4','c5','c6',  
    #                 'd1','d2','d3','d4','d5','d6', 
    #                 'e1','e2','e3','e4','e5','e6',  
    #                 'f1','f2','f3','f4','f5','f6',  
    #                 'g1','g2','g3','g4','g5','g6']]  

    #     y = data['BestMove']  # function to get best move
        

    #     # Scale features to normalize them
    #     scaler = preprocessing.StandardScaler()
    #     X_scaled = scaler.fit_transform(X)

    #     # Train a Support Vector Machine (SVM) model
    #     model = SVC(kernel='linear', random_state=42)
    #     model.fit(X_scaled, y)

    #     return model, scaler
    
    def classify_board(self, board):
            if self.check_win(board, 1):  # Player 1 wins
                return 1  # Class 1 = Win
            elif self.check_win(board, -1):  # Player 2 wins
                return 2  # Class 2 = Loss for Player 1 (since the model would be for Player 1)
            elif self.is_full(board):  # Draw
                return 3  # Class 3 = Draw
            else:
                return 0  

    
    # Check if there are any blocking moves for the AI 
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
    
    def best_move(self, board, model, scaler, turn_count):
        return self.get_best_move(model, scaler, board, turn_count)
        
# Loading data
data = pd.read_csv('assets/connect-4.csv', header=None)
data = ML_Agent().preprocess_data(data)  # Preprocess the data

# Train the model
model, scaler = ML_Agent().train_model(data)


turn_count = 10





# replace a6-a1 samoai habis
#rotate the board
#No header

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
