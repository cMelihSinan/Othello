class Othello:
    def __init__(self):
        """Initialize the Othello board and set the starting player."""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.current_player = 'X'

    def initialize_board(self):
        """Set up the initial board configuration."""
        self.board[3][3], self.board[3][4] = 'O', 'X'
        self.board[4][3], self.board[4][4] = 'X', 'O'

    def print_board(self):
        """Print the current state of the board with better visualization."""
        print("\n    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        for i in range(8):
            row = f"{i+1} | " + " | ".join(self.board[i]) + " |"
            print(row)
            print("  +---+---+---+---+---+---+---+---+")
    def __init__(self):
        """Initialize the Othello board and set the starting player."""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.current_player = 'X'

    def initialize_board(self):
        """Set up the initial board configuration."""
        self.board[3][3], self.board[3][4] = 'O', 'X'
        self.board[4][3], self.board[4][4] = 'X', 'O'

    def print_board(self):
        """Print the current state of the board."""
        print("  a b c d e f g h")
        for i in range(8):
            print(f"{i+1} " + " ".join(self.board[i]))

    def valid_moves(self, player):
        """Return a list of valid moves for the current player."""
        opponent = 'O' if player == 'X' else 'X'
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        moves = []

        for row in range(8):
            for col in range(8):
                if self.board[row][col] != '.':
                    continue
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                        while 0 <= r < 8 and 0 <= c < 8:
                            r += dr
                            c += dc
                            if not (0 <= r < 8 and 0 <= c < 8):
                                break
                            if self.board[r][c] == '.':
                                break
                            if self.board[r][c] == player:
                                moves.append((row, col))
                                break
        return moves

    def make_move(self, row, col, player):
        """Execute a move and flip the opponent's pieces as necessary."""
        opponent = 'O' if player == 'X' else 'X'
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        self.board[row][col] = player
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flips = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                flips.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                for rr, cc in flips:
                    self.board[rr][cc] = player

    def is_game_over(self):
        """Check if the game is over (no valid moves for either player)."""
        return not self.valid_moves('X') and not self.valid_moves('O')

    def count_discs(self):
        """Count the number of discs for each player."""
        black, white = 0, 0
        for row in self.board:
            black += row.count('X')
            white += row.count('O')
        return black, white