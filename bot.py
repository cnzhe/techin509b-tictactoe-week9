import random

# Implement a Bot class to handle the bot logic for the single-player mode
class Bot:
    def make_move(self, board):
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
        return random.choice(available_moves)