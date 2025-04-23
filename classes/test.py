import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.svm import SVC

class ML_Agent:
    def __init__(self):
        pass

    def rotate_board_anticlockwise(self, board):
        return np.array(board).T[::-1]  # Rotate the board 90 degrees anticlockwise
    
    # Preprocess the dataset to replace 'x', 'o', and 'b' with 1, -1, and 0 respectively
    def preprocess_data(self, data):
        processed_boards = []
        processed_labels = []

        # Define column names manually for the 7x6 grid and 'Outcome'
        columns = [f'{chr(97 + c)}{r+1}' for c in range(7) for r in range(6)]  # 'a1' to 'g6'
        columns.append('Outcome')  # Last column is for the outcome ('win', 'draw', 'loss')

        # Set column names after reading the data (no header in CSV)
        data.columns = columns
        
        # Process each row in the dataset
        for index, row in data.iterrows():
            # Reshape the row into 7 columns and 6 rows (board layout)
            board_state = row.values[:-1].reshape(7, 6)  # Get the 7x6 board state
            board_state = self.replace_characters(board_state)  # Convert 'x', 'o', 'b' to 1, -1, 0
            rotated_board = self.rotate_board_anticlockwise(board_state)  # Rotate 90 degrees anticlockwise
            processed_boards.append(rotated_board)
            processed_labels.append(row['Outcome'])  # The last column is the outcome label

        return np.array(processed_boards), np.array(processed_labels)

    # Convert 'x', 'o', and 'b' to numerical values
    def replace_characters(self, board_state):
        # Replace 'x' -> 1, 'o' -> -1, 'b' -> 0
        board_state = np.where(board_state == 'x', 1, board_state)
        board_state = np.where(board_state == 'o', -1, board_state)
        board_state = np.where(board_state == 'b', 0, board_state)
        return board_state

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

    # Check if there are any blocking moves for the AI 
    def check_block_move(self, board, player):
        for c in range(7):
            row = self.get_next_open_row(board, c)
            if row != -1:  # If the column isn't full
                board[row][c] = player  # Temporarily make the move for the player
                if self.check_win(board, player):  # Check if this move results in a win
                    board[row][c] = 0  # Reset the move
                    return c  # This is the blocking move
                board[row][c] = 0  # Reset the move
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
data = pd.read_csv('assets/connect-4.csv', header=None)  # No header in CSV file

# Train the model
model, scaler = ML_Agent().train_model(data)

# Example board state (you should replace this with actual board data from the game)
turn_count = 10  # For example, after 10 moves

board = np.array([
    [1, -1, 1, 0, -1, 1],
    [-1, 1, 0, -1, 0, 1],
    [0, 1, -1, 1, 0, -1],
    [-1, 1, 0, 1, -1, 0],
    [1, 0, 1, 0, 1, -1],
    [-1, 1, 0, -1, 1, 0]
])

# Get the best move from the ML Agent
best_move = ML_Agent().best_move(board, model, scaler, turn_count)
print(f"Best move predicted: {best_move}")
