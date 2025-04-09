import random

class RandomAgent:
    def __init__(self):
        pass

    def random_agent_move(self, board):
        # search for empty cells
        empty_cells = [(row, col) for row in range(6) for col in range(7)
                       if board[row][col] == 0]
        

        row, col = random.choice(empty_cells)
        # get the column
        return col
