class Minimax_Agent:

    def __init__(self,ai_player =1,opponents =2):
        
        self.ai_player = ai_player
        self.opponents = opponents
    
    def is_terminal(self, board):
        return self.check_win(board, 1) or self.check_win(board, 2) or self.is_full(board)

    def minimax(self,board,alpha,beta,depth,maximizingPlayer):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate_board(board)

        if maximizingPlayer:
                max_eval = float('-inf')
                for col in self.get_available_moves(board):  # Get columns
                    row = self.get_next_open_row(board, col)  
                    self.make_move(board,col, self.ai_player)  
                    eval = self.minimax(board, alpha, beta, depth - 1, False)  # Minimize opponent's move
                    board[row][col] = 0  

                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # Beta cut-off
                        break
                return max_eval
        else:
                min_eval = float('inf')
                for col in self.get_available_moves(board):
                    row = self.get_next_open_row(board, col) 
                    self.make_move(board,col,self.opponents)
                    eval = self.minimax(board,alpha,beta,depth - 1, True) # Maximizing bot moves
                    board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
                return min_eval

        

    def evaluate_board(self, board):
        if self.check_win(board, 2):
            return 1000000 # Bot wins
        elif self.check_win(board, 1):
            return -100000  # opponent wins
        return 0 
        
    def best_move(self,board):
        #fetching the best move for minimax agent
        best_val = float('-inf')
        move = None
        for col in self.get_available_moves(board):
            row = self.get_next_open_row(board,col)
            self.make_move(board, col, self.ai_player)
            move_val = self.minimax(board, float('-inf'), float('inf'),3,False) # depth can be customizable
            board[row][col] = 0
            if move_val > best_val:
                best_val = move_val
                move = col
        return move
        
    # Check if the board is full / draw
    def is_full(self,board):
        return all(board[row][col] != 0 for row in range(6) for col in range(7))

    def get_available_moves(self, board):
            return [col for col in range(7) if board[0][col] == 0]
    
    def make_move(self,board,col,piece):
        row = self.get_next_open_row(board,col)
        if row != -1:
            board[row][col] = piece
        


    def get_next_open_row(self, board, col):
        for r in range(5, -1, -1):  # Start from the bottom row
            if board[r][col] == 0:
                return r
        return -1

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