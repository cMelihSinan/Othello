import copy
import math
from random import choice

class AIPlayer:
    def __init__(self, depth, heuristic):
        """Initialize the AI with a specific depth and heuristic."""
        self.depth = depth
        self.heuristic = heuristic

    def evaluate(self, game, player):
        opponent = 'O' if player == 'X' else 'X'
        if self.heuristic == 1:  # Disc difference
            return sum(row.count(player) for row in game.board) - sum(row.count(opponent) for row in game.board)
        elif self.heuristic == 2:  # Corner control
            corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
            return sum(1 for r, c in corners if game.board[r][c] == player)
        elif self.heuristic == 3:  # Mobility advantage
            return self.heuristic_mobility(game, player)

    def heuristic_corners(self, board, player):
        """Heuristic to prioritize corners."""
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        return sum(1 for r, c in corners if board[r][c] == player)

    def heuristic_mobility(self, game, player):
        """Evaluate mobility by counting the number of valid moves."""
        return len(game.valid_moves(player))

    def minimax(self, game, depth, alpha, beta, maximizing, player):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or game.is_game_over():
            return self.evaluate(game, player), None

        moves = game.valid_moves(player)
        if not moves:
            return self.evaluate(game, player), None

        opponent = 'O' if player == 'X' else 'X'
        best_moves = []
        if maximizing:
            max_eval = -math.inf
            for move in moves:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move[0], move[1], player)
                eval_score, _ = self.minimax(game_copy, depth - 1, alpha, beta, False, opponent)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_moves = [move]
                elif eval_score == max_eval:
                    best_moves.append(move)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, choice(best_moves)
        else:
            min_eval = math.inf
            for move in moves:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move[0], move[1], player)
                eval_score, _ = self.minimax(game_copy, depth - 1, alpha, beta, True, opponent)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_moves = [move]
                elif eval_score == min_eval:
                    best_moves.append(move)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, choice(best_moves)