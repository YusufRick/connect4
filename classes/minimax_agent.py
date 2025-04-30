import random
class Minimax_Agent:

    def __init__(self,ai_player ,opponents,turn):
        
        self.ai_player = ai_player
        self.opponent = opponents
        self.turn = turn
        self.depth = 5
    
    # check win/lose or draw
    def is_terminal(self, board):
        return board.check_win(self.ai_player) or board.check_win(self.opponent) or board.is_full()

    #How it works:
    # maximizing agents move and minimizing opponents move

    def minimax(self,board,alpha,beta,depth,maximizingPlayer):
        if depth == 0 or self.is_terminal(board):
            return None, self.evaluate_board(board)

        if maximizingPlayer:
                max_eval = float('-inf')
                best_col = None
                for col in board.get_available_moves():  # Get columns
                    row = board.get_next_open_row(col)  
                    b_copy = board.copy()
                    b_copy.drop_piece(row, col, self.ai_piece)
                    _,eval = self.minimax(board, alpha, beta, depth - 1, False)  # Minimize opponent's move
                    

                    if eval > max_eval:
                        max_eval= eval
                        best_col = col
                    
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # Beta cut-off
                        break
                return best_col, max_eval
        else:
                min_eval = float('inf')
                best_col = None
                for col in board.get_available_moves():
                    row = board.get_next_open_row( col) 
                    b_copy = board.copy()
                    b_copy.drop_piece(row, col, self.ai_piece)
                    _,eval = self.minimax(board,alpha,beta,depth - 1, True) # Maximizing bot moves
                    


                    if eval < min_eval:
                        min_eval = eval
                        best_col = col
                        beta = min(beta, min_eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
                return best_col, min_eval

        
    # if a move results in agent winning, reward with infinite points
    # if a move will result in opponents winning, give a -inf points
    # simulate all available moves
    # everytime theres a winning moves, +100 points
    # if opponents wins in the simulation, undo move to cut off branch
    def evaluate_board(self, board):
        if board.check_win(self.ai_player):
            return 1000000  # AI wins
        
        elif board.check_win(self.opponent):
            return -10000000  # Opponent wins


        return 0

    
        
    def best_move(self, board):

        for col in range(7):
            row = board.get_next_open_row(col)
            if row == -1:
                continue

            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.ai_piece)

            if b_copy.check_win(self.ai_piece):
                return col

        # Block opponent's winning move
        for col in range(7):
            row = board.get_next_open_row(col)
            b_copy = board.copy()
            b_copy.drop_piece(row, col, self.opponent)

            if b_copy.check_win(self.opponent):
                return col
            
        col, _score = self.minimax(board,alpha = float('-inf'),beta  = float('inf'),depth = self.depth, maximizingPlayer = True)
        # fallback if no moves
        valid = board.get_available_moves()
        if  not valid.contains(col):
            col = random.choice(valid)
        return col
        
        

# function minimax(node, depth, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, minimax(child, depth − 1, FALSE))
#         return value
#     else (* minimizing player *)
#         value := +∞
#         for each child of node do
#             value := min(value, minimax(child, depth − 1, TRUE))
#         return value