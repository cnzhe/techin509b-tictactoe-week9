from logic import make_empty_board, get_winner
from datetime import datetime
import logging
import csv
import os

# Configure the logging settings
logging.basicConfig(
    filename = 'logs/tic_tac_toe.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

# Create a Game class to manage the game logic and the mode
class Game:
    def __init__(self, mode):
        self.board = make_empty_board()
        self.winner = None
        self.player = 'X'  # Player 'X' starts
        self.moves = 0  # Track the number of moves
        self.mode = mode
        # Use dependency injection to pass the Bot instance
        if mode == "single":
            from bot import Bot
            self.bot = Bot()

    def record_winner(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        winner_data = {
            'Timestamp': timestamp,
            'Winner': 'Draw' if self.winner is None else self.winner,
            'Player_X': 'Human' if self.mode == 'two' else 'Human' if self.player == 'X' else 'Bot',
            'Player_O': 'Human' if self.mode == 'two' else 'Bot' if self.player == 'X' else 'Human',
            'Mode': self.mode,
            'Moves_Played': self.moves,
        }

        # Create the CSV file if it doesn't exist
        csv_file_path = 'logs/winners.csv'
        is_new_file = not os.path.isfile(csv_file_path)

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Timestamp', 'Winner', 'Player_X', 'Player_O', 'Mode', 'Moves_Played'])

            if is_new_file:
                writer.writeheader()  # Write header only if the file is newly created

            writer.writerow(winner_data)

    def print_board(self):
        """Prints the Tic-Tac-Toe board."""
        for i, row in enumerate(self.board):
            formatted_row = [cell if cell is not None else ' ' for cell in row]
            print(" | ".join(formatted_row))
            if i < 2:  # Add two dashes below the first and second rows
                print("-" * 9)

    def play(self):
        while self.winner is None and self.moves < 9:
            # Show the board to the user
            self.print_board()
            print(f"Player {self.player}'s turn.")

            if self.mode == "single" and self.player == 'O':
                # Single-player mode: Bot's turn
                row, col = self.bot.make_move(self.board)
            else:
                row = int(input("Enter the row (0, 1, or 2): "))
                col = int(input("Enter the column (0, 1, or 2): "))

            if self.board[row][col] is not None:
                print("Invalid move. Cell already occupied.")
                continue

            logging.info(f"Player {self.player} made a move at row {row}, column {col}.")

            # Update the board.
            self.board[row][col] = self.player

            # Update who's turn it is.
            self.player = 'O' if self.player == 'X' else 'X'
            self.moves += 1

            # Check for a winner
            self.winner = get_winner(self.board)
  
            # Log the winner
            if self.winner:
                self.record_winner()


        # Show the final board to the user.
        self.print_board()

        if self.winner == 'X':
            logging.info("Player X won the game!")
            print("Player X won!")
        elif self.winner == 'O':
            logging.info("Player O won the game!")
            print("Player O won!")
        else:
            logging.info("The game ended in a draw.")
            print("It's a draw!")


if __name__ == '__main__':
    mode = input("Choose the game mode (single/two): ").lower()
    game = Game(mode)
    game.play()