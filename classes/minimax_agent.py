class Minimax_Agent:

    def __init__(self,ai_player = 2,opponents=1):
        
        self.ai_player = ai_player
        self.opponents = opponents
    
    # check win/lose or draw
    def is_terminal(self, board):
        return board.check_win( self.ai_player) or board.check_win(self.opponents) or board.is_full()

    def minimax(self,board,alpha,beta,depth,maximizingPlayer):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate_board(board)

        if maximizingPlayer:
                max_eval = float('-inf')
                for col in board.get_available_moves():  # Get columns
                    row = board.get_next_open_row(col)  
                    board.make_move(col, self.ai_player)  
                    eval = self.minimax(board, alpha, beta, depth - 1, False)  # Minimize opponent's move
                    board.board[row][col] = 0  

                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # Beta cut-off
                        break
                return max_eval
        else:
                min_eval = float('inf')
                for col in board.get_available_moves():
                    row = board.get_next_open_row( col) 
                    board.make_move(col,self.opponents)
                    eval = self.minimax(board,alpha,beta,depth - 1, True) # Maximizing bot moves
                    board.board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
                return min_eval

        

    def evaluate_board(self, board):
        if board.check_win(self.ai_player):
            return 1000000  # AI wins
        elif board.check_win(self.opponents):
            return -10000000  # Opponent wins

        score = 0
        available_moves = board.get_available_moves()

        for col in available_moves:
            row = board.get_next_open_row(col)
        
            board.board[row][col] = self.ai_player
            if board.check_win(self.ai_player):
                score += 100  # Reward AI for winning

        # Simulate the opponent's move
            board.board[row][col] = self.opponents
            if board.check_win(self.opponents):
                score -= 10000  # Penalize if it allows the opponent to win

        # Undo the move
            board.board[row][col] = 0

        return score

    
        
    def best_move(self,board):
        #fetching the best move for minimax agent
        best_val = float('-inf')
        move = None
        for col in board.get_available_moves():
            row = board.get_next_open_row(col)
            board.make_move(col, self.ai_player)
            move_val = self.minimax(board, float('-inf'), float('inf'),5,False) # depth can be customizable
            board.board[row][col] = 0
            if move_val > best_val:
                best_val = move_val
                move = col
        return move
        
    # Check if the board is full / draw
    # def is_full(self,board):
    #     return all(board[row][col] != 0 for row in range(6) for col in range(7))

    # # get available moves
    # def get_available_moves(self, board):
    #         return [col for col in range(7) if board[0][col] == 0]
    

    # def make_move(self,board,col,piece):
    #     row = self.get_next_open_row(board,col)
    #     if row != -1:
    #         board[row][col] = piece
        

    # # get the lowest row
    # def get_next_open_row(self, board, col):
    #     for r in range(5, -1, -1):  # Start from the bottom row
    #         if board[r][col] == 0:
    #             return r
    #     return -1

    # def check_win(self, board, piece):
    #     # Horizontal Check
    #     for r in range(6):
    #         for c in range(4):
    #             if all(board[r][c+i] == piece for i in range(4)):
    #                 return True

    #     # Vertical Check
    #     for r in range(3):
    #         for c in range(7):
    #             if all(board[r+i][c] == piece for i in range(4)):
    #                 return True

    #     # Diagonal Down-Right Check
    #     for r in range(3):
    #         for c in range(4):
    #             if all(board[r+i][c+i] == piece for i in range(4)):
    #                 return True

    #     # Diagonal Down-Left Check
    #     for r in range(3):
    #         for c in range(3, 7):
    #             if all(board[r+i][c-i] == piece for i in range(4)):
    #                 return True

    #     return False
    

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