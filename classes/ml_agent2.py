from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import math
import random


class MLAgent2:
    def __init__(self,agent,opponent,turn):
        self.ai_piece    = agent
        self.opponent = opponent
        self.turn = turn
        self.depth = 5
        self.model = RandomForestClassifier(n_estimators=100)
        self.trained = False
        # replace the alphabet with vectors
        self.board_map       = {'x': 1, 'o': 2, 'b': 0}
        self.result_map      = {'win':  0,'draw': 1,'loss': 2}


    # load data from imported dataset
    def load_data(self, X, y):

        X = X.replace(self.board_map)
        X = X.infer_objects(copy=False).astype(int)
        y = y.replace(self.result_map).astype(int).values.ravel()
        self.X = X
        self.y = y

    #train the model
    def train(self):

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test
        self.trained = True

        accuracy = self.model.score(X_test, y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")
        gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
        gb_model.fit(X_train, y_train)

        gb_accuracy = gb_model.score(X_test, y_test)
        print(f"Gradient Boosting Accuracy: {gb_accuracy * 100:.2f}%")

    def is_terminal(self, board):
        return board.check_win( self.ai_piece) or board.check_win(self.opponent) or board.is_full()


    def minimax(self,board,alpha,beta,depth,maximizingPlayer):
        if depth == 0 or self.is_terminal(board):
            return None, self.evaluate_board(board)

        if maximizingPlayer:
                max_eval = -math.inf
                best_col = None
                for col in board.get_available_moves():  # Get columns
                    row = board.get_next_open_row(col)  
                    b_copy = board.copy()
                    b_copy.drop_piece(row, col, self.ai_piece)
                    _,eval = self.minimax(b_copy, alpha, beta, depth - 1, False)  # Minimize opponent's move
                    

                    if eval > max_eval:
                        max_eval= eval
                        best_col = col
                    
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # Beta cut-off
                        break
                return best_col, max_eval
        else:
                min_eval = math.inf
                best_col = None
                for col in board.get_available_moves():
                    row = board.get_next_open_row( col) 
                    b_copy = board.copy()
                    b_copy.drop_piece(row, col, self.opponent)
                    _,eval = self.minimax(b_copy,alpha,beta,depth - 1, True) # Maximizing bot moves
                    


                    if eval < min_eval:
                        min_eval = eval
                        best_col = col
                    beta = min(beta, min_eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
                return best_col, min_eval

    def evaluate_board(self, board):
        if board.check_win(self.ai_piece):
            return 10000000  # AI wins
        
        elif board.check_win(self.opponent):
            return -10000000  # Opponent wins

        # Evaluate using the ML model at the terminal state (win, loss, or draw)
        flat = [cell for row in board.board for cell in row]
        df = pd.DataFrame([flat], columns=self.X.columns).astype(int)

        if df.isnull().values.any():
            print("Warning: Board state has invalid values.")
            return 0  

        probs = self.model.predict_proba(df)[0]

        # If ai is the first player, seearch for win
        #If ai is the second player, search for loss( first player lose)
        if self.ai_piece == 1:  
            return probs[0]  
        else:  
            return probs[2]  



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
    # x is the first player while o is the second player based on the dataset

    # def best_move(self, board):
    #     if not self.trained:
    #         raise Exception("Model is not trained.")

    #     best_col, best_score = -1, -1.0

    #     # Try each available move
    #     for col in board.get_available_moves():
    #         b1 = copy.deepcopy(board)
    #         r1 = b1.get_next_open_row(col)
    #         b1.drop_piece(r1, col, self.ai_piece)

    #         if b1.check_win(self.ai_piece):  
    #             return col  

    #     # Step 2: If no blocking move is found, look for the AI's winning move.
    #     for col in board.get_available_moves():
    #         b1 = copy.deepcopy(board)
    #         r1 = b1.get_next_open_row(col)
    #         b1.drop_piece(r1, col, self.opponent)

    #         if b1.check_win(self.opponent):  
    #             return col

    #         # 2) Simulate opponent’s best reply (to minimize our winning probability)
    #         worst = 1.0  # Start with the worst value/ worst case
    #         for col2 in b1.get_available_moves():
    #             b2 = copy.deepcopy(b1)
    #             r2 = b2.get_next_open_row(col2)
    #             b2.drop_piece(r2, col2, self.opponent)

    #             # Encode the board state for prediction
    #             flat = [cell for row in b2.board for cell in row]
    #             df = pd.DataFrame([flat], columns=self.X.columns).astype(int)
                
    #             # Get predicted probabilities for this board state
    #             probs = self.model.predict_proba(df)[0]

    #             # Interpret probabilities based on the current turn
    #             # if ai piece is 1(first player) get the probability of "win"
    #             # else, get the probability of loss(first player losing)
    #             if self.ai_piece == 1:  
    #                 score = probs[0]  # Probability of first-player win
    #             else:  
    #                 score = probs[2]  
    #             # Update the worst case if the current score is worse
    #             worst = min(worst, score)

    #         # 3) Maximize worst-case scenario (minimax)
    #         if worst > best_score:  # get highest worst score
    #             best_score, best_col = worst, col

    #     return best_col


    def best_move(self, board):
        if not self.trained:
            raise Exception("Model is not trained.")
        
        moves = board.get_available_moves()


        # check if theres any winning move
        for col in moves:
            b = board.copy()
            r = b.get_next_open_row(col)
            b.drop_piece(r, col, self.ai_piece)
            if b.check_win(self.ai_piece):
                return col

        # check to block opponents winning move
        for col in moves:
            b = board.copy()
            r = b.get_next_open_row(col)
            b.drop_piece(r, col, self.opponent)
            if b.check_win(self.opponent):
                return col  


        best_col  = None
        best_score = -math.inf

        for col in board.get_available_moves():
            b1 = board.copy()
            r = b.get_next_open_row(col)
            b1.drop_piece(r, col, self.ai_piece)
            _, _score = self.minimax(b1, alpha=-math.inf, beta=+math.inf,
                                    depth=self.depth-1, maximizingPlayer=False)
            
        if _score > best_score:
                best_score = _score
                best_col = col



        valid = board.get_available_moves()
        return best_col if best_col in valid else random.choice(valid)






