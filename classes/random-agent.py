import random

class RandomAgent:
    def __init__(self):
        pass

    def random_agent_move(board):
        empty_cells = [(row,col) for row in range(6) for col in range(7)
                       if board[row][col] == " "]
        return random.choice(empty_cells)