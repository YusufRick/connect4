from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import copy
import pandas as pd

class MLAgent:
    def __init__(self):
        self.ai_piece    = 2
        self.model = RandomForestClassifier(n_estimators=100)
        self.trained = False
        self.board_map       = {'x': 1, 'o': 2, 'b': 0}
        self.result_map      = {'win':  0,
                                'draw': 1,
                                'loss': 2}

    def load_data(self, X, y):

        X = X.replace(self.board_map)
        X = X.infer_objects(copy=False).astype(int)
        y = y.replace(self.result_map).astype(int).values.ravel()
        self.X = X
        self.y = y

    def train(self):

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test
        self.trained = True

        accuracy = self.model.score(X_test, y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

    def evaluate(self):

        if not self.trained:
            print("Model not trained yet.")
            return
        predictions = self.model.predict(self.X_test)
        print("Classification Report:")
        print(classification_report(self.y_test, predictions))


    # How it works:
    # the bot check if its the first or second player.
    # if it's the first player (1), it will get the model to favor "win"
    #if it's the 2nd player, the model will favor "loss" to make sure first player lose.

    def best_move(self, board):
        if not self.trained:
            raise Exception("Model is not trained.")

        if self.ai_piece ==1:
            opponent_piece =2
        else:
            opponent_piece = 1
            
        best_col, best_score = -1, -1.0

        # Try each possible move
        for col in board.get_available_moves():
            # 1) Simulate our move
            b1 = copy.deepcopy(board)
            r1 = b1.get_next_open_row(col)
            b1.drop_piece(r1, col, self.ai_piece)

            # 2) Opponent’s best reply—to minimize our win-prob
            worst = 1.0
            for c2 in b1.get_available_moves():
                b2 = copy.deepcopy(b1)
                r2 = b2.get_next_open_row(c2)
                b2.drop_piece(r2, c2, opponent_piece)

                # Encode and get probs
                flat = [cell for row in b2.board for cell in row]
                df   = pd.DataFrame([flat], columns=self.X.columns).astype(int)
                probs = self.model.predict_proba(df)[0]

                # **YOUR LOGIC**: pick class 0 if you're P1, class 2 if you're P2
                if self.ai_piece == 1:
                    score = probs[0]   # P(first-player win)
                else:
                    score = probs[2]   # P(first-player loss) == P(second-player win)

                worst = min(worst, score)

            # 3) Maximize worst-case
            if worst > best_score:
                best_score, best_col = worst, col

        return best_col





