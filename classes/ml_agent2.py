from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

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
        # replace x,o,b into integer for board state
        self.board_map       = {'x': 1, 'o': 2, 'b': 0}
        #replace win,loss and draw into integer
        self.result_map      = {'win':  0,'draw': 1,'loss': 2}


    # load data from imported dataset
    def load_data(self, X, y):
         # Preprocess the features dataset (board state)
        X = X.replace(self.board_map)
        X = X.infer_objects(copy=False).astype(int)
        y = y.replace(self.result_map).astype(int).values.ravel()
        self.X = X
        self.y = y

    #train the model
    def train(self):
        # Split data into training and test sets(20%)
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test
        self.trained = True

        accuracy = self.model.score(X_test, y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # check the roots of tree (win,lose,draw)
    def is_terminal(self, board):
        return board.check_win( self.ai_piece) or board.check_win(self.opponent) or board.is_full()


    def minimax(self,board,alpha,beta,depth,maximizingPlayer):

         #if it hits terminal or depth is 0, evaluate the board
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
                    #if alpha(ai) score is > than beta(opponent), stop exploring
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

                    #if alpha(ai) score is > than beta(opponent), stop exploring
                    if beta <= alpha:
                        break  # Alpha cut-off
                return best_col, min_eval

    def evaluate_board(self, board):

        # How it works:
        # the bot check if its the first or second player.
        # if it's the first player (1), it will get the model to favor "win"
        #if it's the 2nd player, the model will favor "loss" to make sure first player lose.
        # x is the first player while o is the second player based on the dataset
        if board.check_win(self.ai_piece):
            return 10000000  # AI wins
        
        if board.check_win(self.opponent):
            return -10000000  # Opponent wins

        # Evaluate using the ML model at the terminal state (win, loss, or draw)
        flat = [cell for row in board.board for cell in row]
        df = pd.DataFrame([flat], columns=self.X.columns).astype(int)

        prediction = self.model.predict_proba(df)[0]

        # If ai is the first player, seearch for win
        #If ai is the second player, search for loss( first player lose)
        if self.ai_piece == 1:  
            return prediction[0]  
        else:  
            return prediction[2]  




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
        #use minimax to search for the best move
        for col in board.get_available_moves():
            b1 = board.copy()
            r = b.get_next_open_row(col)
            b1.drop_piece(r, col, self.ai_piece)
            _, _score = self.minimax(b1, alpha=-math.inf, beta=+math.inf,depth =self.depth, maximizingPlayer=False)
            
            #keep track of the highest minimax score
            if _score > best_score:
                    best_score = _score
                    best_col = col


        #if column is not valid(in case) pick a random valid column.
        valid = board.get_available_moves()
        return best_col if best_col in valid else random.choice(valid)






