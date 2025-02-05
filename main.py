from Othello import Othello
from AIplayer import AIPlayer
import time


def get_human_move(game, player):
    """Prompt the user for a move and validate it."""
    moves = game.valid_moves(player)
    if not moves:
        print(f"No valid moves for {player}. Turn skipped.")
        return None

    print(f"Valid moves for {player}: {[(r + 1, chr(c + ord('a'))) for r, c in moves]}")
    while True:
        user_input = input(f"{player}'s turn. Enter move (row col, e.g., 4 d): ").strip().lower()
        try:
            row, col = user_input.split()
            row = int(row) - 1
            col = ord(col) - ord('a')
            if (row, col) in moves:
                return row, col
            else:
                print("Invalid move. Please choose from the valid moves.")
        except (ValueError, IndexError):
            print("Invalid input format. Please enter as 'row col' (e.g., 4 d).")


def human_vs_human():
    """Start a human vs. human game."""
    game = Othello()
    while not game.is_game_over():
        game.print_board()
        move = get_human_move(game, game.current_player)
        if move:
            game.make_move(*move, game.current_player)
        game.current_player = 'O' if game.current_player == 'X' else 'X'

    game.print_board()
    black, white = game.count_discs()
    print(f"Game Over! Final Score - Black: {black}, White: {white}")
    print("Winner:", "Black" if black > white else "White" if white > black else "Draw")


def human_vs_ai():
    """Start a human vs. AI game."""
    game = Othello()
    ai_player = AIPlayer(depth=3, heuristic=1)
    while not game.is_game_over():
        game.print_board()
        if game.current_player == 'X':
            move = get_human_move(game, 'X')
        else:
            print(f"AI ('O') is thinking...")
            time.sleep(0.5)  # Add delay for AI's move
            _, move = ai_player.minimax(game, ai_player.depth, -float('inf'), float('inf'), True, 'O')

        if move:
            game.make_move(*move, game.current_player)
        game.current_player = 'O' if game.current_player == 'X' else 'X'

    game.print_board()
    black, white = game.count_discs()
    print(f"Game Over! Final Score - Black: {black}, White: {white}")
    print("Winner:", "Black" if black > white else "White" if white > black else "Draw")


def ai_vs_ai():
    """Start an AI vs. AI game with configurable settings."""
    game = Othello()

    # Configure AI players
    depth1 = int(input("Enter depth for AI Player 1 (X): "))
    heuristic1 = int(input("Choose heuristic for AI Player 1 (1: h1, 2: h2, 3: h3): "))
    ai_player1 = AIPlayer(depth=depth1, heuristic=heuristic1)

    depth2 = int(input("Enter depth for AI Player 2 (O): "))
    heuristic2 = int(input("Choose heuristic for AI Player 2 (1: h1, 2: h2, 3: h3): "))
    ai_player2 = AIPlayer(depth=depth2, heuristic=heuristic2)

    while not game.is_game_over():
        game.print_board()
        if game.current_player == 'X':
            print(f"AI Player 1 ('X') is thinking...")
            _, move = ai_player1.minimax(game, ai_player1.depth, -float('inf'), float('inf'), True, 'X')
        else:
            print(f"AI Player 2 ('O') is thinking...")
            _, move = ai_player2.minimax(game, ai_player2.depth, -float('inf'), float('inf'), True, 'O')

        if move:
            game.make_move(*move, game.current_player)
        game.current_player = 'O' if game.current_player == 'X' else 'X'

    game.print_board()
    black, white = game.count_discs()
    print(f"Game Over! Final Score - Black: {black}, White: {white}")
    print("Winner:", "Black" if black > white else "White" if white > black else "Draw")


def main():
    print("Welcome to Othello!")
    print("1. Human vs. Human")
    print("2. Human vs. AI")
    print("3. AI vs. AI")
    choice = input("Choose game mode (1/2/3): ").strip()

    if choice == '1':
        human_vs_human()
    elif choice == '2':
        human_vs_ai()
    elif choice == '3':
        ai_vs_ai()
    else:
        print("Invalid choice. Exiting game.")


if __name__ == "__main__":
    main()