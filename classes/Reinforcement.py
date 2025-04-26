import numpy as np
import random
import copy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import preprocessing
import pandas as pd


class MLAgent:
    def __init__(self, agent, opponent, turn, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.ai_piece = agent
        self.opponent = opponent
        self.turn = turn
        
        # Initialize Q-learning parameters
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}  # Q-table for Q-learning

        # For ML-based approach
        self.model = RandomForestClassifier(n_estimators=100)  # Or SVC
        self.trained = False

        # Mapping board symbols and game results to numeric values
        self.board_map = {'x': 1, 'o': 2, 'b': 0}
        self.result_map = {'win': 0, 'draw': 1, 'loss': 2}

    def get_state(self, board):
        """
        Convert the current board into a state tuple for Q-learning.
        """
        return tuple(tuple(row) for row in board)  # Tuples for immutability and hashing

    def choose_action(self, board, available_moves):
        """
        Choose an action (column) based on the epsilon-greedy strategy.
        """
        state = self.get_state(board)
        if random.uniform(0, 1) < self.epsilon:  # Explore
            return random.choice(available_moves)
        else:  # Exploit
            q_values = [self.q_table.get((state, move), 0) for move in available_moves]
            return available_moves[np.argmax(q_values)]

    def update_q_value(self, board, action, reward, next_board, available_moves):
        """
        Update Q-value using the Q-learning update rule.
        """
        state = self.get_state(board)
        next_state = self.get_state(next_board)
        best_next_action = max([self.q_table.get((next_state, move), 0) for move in available_moves], default=0)
        
        # Q-value update
        self.q_table[(state, action)] = self.q_table.get((state, action), 0) + self.alpha * (reward + self.gamma * best_next_action - self.q_table.get((state, action), 0))

    def load_data(self, X, y):
        """
        Preprocess and load training data for ML-based decision-making.
        """
        X = X.replace(self.board_map).astype(int)  # Convert 'x', 'o', 'b' to 1, 2, 0
        y = y.replace(self.result_map).astype(int).values.ravel()  # Convert results to numeric (win, draw, loss)
        self.X = X
        self.y = y

    def train(self):
        """
        Train the RandomForest or SVM model for the ML-based approach.
        """
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        
        # Scale the features to help SVM converge better
        scaler = preprocessing.StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
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
        Predict the best column for the AI to place its piece using Q-learning and/or ML-based model.
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

            if board.check_win(self.ai_piece):
                return col

            worst = 1.0
            for col2 in b1.get_available_moves():
                # 2) Simulate opponent's move
                b2 = copy.deepcopy(b1)
                r2 = b2.get_next_open_row(col2)
                b2.drop_piece(r2, col2, self.opponent)

                # 3) Use ML model (RandomForest or SVC) for predictions
                flat = [cell for row in b2.board for cell in row]
                df = pd.DataFrame([flat], columns=self.X.columns).astype(int)

                # Convert df to numpy array before prediction
                df_values = df.values  # Convert to numpy array
                probs = self.model.predict_proba(df_values)[0]

                if self.ai_piece == 1:
                    score = probs[0]  # Probability of first-player win
                else:
                    score = probs[2]  # Probability of first-player loss (second-player win)

                worst = min(worst, score)

            # Maximize worst-case scenario
            if worst > best_score:
                best_score, best_col = worst, col

        return best_col
