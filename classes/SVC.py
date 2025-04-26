from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import preprocessing
import copy
import pandas as pd

class MLAgent:
    def __init__(self, agent, opponent, turn):
        self.ai_piece = agent
        self.opponent = opponent
        self.turn = turn
        self.model = SVC(kernel='linear', random_state=42, probability=True)  # Linear SVC for classification
        self.trained = False
        # Mapping board symbols and game results to numeric values
        self.board_map = {'x': 1, 'o': 2, 'b': 0}  # 'x' -> 1, 'o' -> 2, 'b' -> 0
        self.result_map = {'win': 0, 'draw': 1, 'loss': 2}  # 'win' -> 0, 'draw' -> 1, 'loss' -> 2

    def load_data(self, X, y):
        """
        Preprocess the data by encoding the board and the results.
        """
        X = X.replace(self.board_map).astype(int)  # Convert 'x', 'o', 'b' to 1, 2, 0
        y = y.replace(self.result_map).astype(int).values.ravel()  # Convert results to numeric (win, draw, loss)
        self.X = X
        self.y = y

    def train(self):
        """
        Train the SVM model on the board state and the corresponding results.
        """
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        
        # Scale the features to help SVM converge better
        scaler = preprocessing.StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train the SVC model
        self.model.fit(X_train_scaled, y_train)
        
        # Store the test data for evaluation
        self.X_test = X_test_scaled
        self.y_test = y_test
        self.trained = True

        # Evaluate the model's accuracy
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

    def evaluate(self):
        """
        Evaluate the performance of the trained model.
        """
        if not self.trained:
            print("Model is not trained yet.")
            return
        
        predictions = self.model.predict(self.X_test)
        print("Classification Report:")
        print(classification_report(self.y_test, predictions))

    def best_move(self, board):
        """
        Predict the best column for the AI to place its piece.
        Simulates the AI move and opponent's move, and selects the best column based on model probabilities.
        """
        if not self.trained:
            raise Exception("Model is not trained.")

        best_col, best_score = -1, -1.0

        # Try each possible move
        for col in board.get_available_moves():
            # 1) Simulate AI's move
            b1 = copy.deepcopy(board)
            r1 = b1.get_next_open_row(col)
            b1.drop_piece(r1, col, self.ai_piece)

            worst = 1.0
            for col2 in b1.get_available_moves():
                # 2) Simulate opponent's move
                b2 = copy.deepcopy(b1)
                r2 = b2.get_next_open_row(col2)
                b2.drop_piece(r2, col2, self.opponent)

                # Flatten the board to a 1D array
                flat = [cell for row in b2.board for cell in row]
                df = pd.DataFrame([flat], columns=self.X.columns).astype(int)
                probs = self.model.predict_proba(df)[0]  # Get the predicted probabilities

                # Choose the score based on the turn
                if self.turn == 1:  # If it's the bot's turn, favor the win
                    score = probs[0]  # Probability of first-player win
                else:  # If it's the opponent's turn, favor the loss
                    score = probs[2]  # Probability of first-player loss (which is second-player win)

                worst = min(worst, score)

            # 3) Maximize worst-case scenario
            if worst > best_score:
                best_score, best_col = worst, col

        return best_col
