import random



    
class Random_Agent:
        def __init__(self):
            pass

        def best_move(self, board):
            # search for empty cells
            empty_cells = [(row, col) for row in range(6) for col in range(7)
                           if board[row][col] == 0]
            # get the column of a random empty cell
            row, col = random.choice(empty_cells)
            return col

    
    #Plays using a basic set of rules: win > block > random.
class Smart_Agent:
        def __init__(self):
            pass
        
        def get_available_moves(self, board):
            return [col for col in range(7) if board[0][col] == 0]

        def check_winner(self, board, col, piece):
            # Check if dropping the piece in the given column results in a win
            row = self.get_next_open_row(board, col)
            if row == -1:
                return False
            board[row][col] = piece
            win = self.check_win(board, piece)
            board[row][col] = 0  # Undo the move
            return win

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
        
        def best_move(self, board):
            # check for a winning move
            for col in self.get_available_moves(board):
                if self.check_winner(board, col, 2):  # Check if Player 2 can win
                    return col  # 

            # block opponent winning move
            for col in self.get_available_moves(board):
                if self.check_winner(board, col, 1):  
                    return col  # Block the winning move

            # Random move
            return random.choice(self.get_available_moves(board))

