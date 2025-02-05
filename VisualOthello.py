import pygame
import sys
import time
from Othello import Othello
from AIplayer import AIPlayer

# Constants
WINDOW_SIZE = 600
LOG_WIDTH = 300
GRID_SIZE = 8
CELL_SIZE = (WINDOW_SIZE - 50) // GRID_SIZE  # Adjusted for extra label space
LABEL_SPACE = 50  # Space for row and column labels
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
FPS = 30

class VisualOthelloScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE + LOG_WIDTH, WINDOW_SIZE))
        pygame.display.set_caption("Othello")
        self.clock = pygame.time.Clock()
        self.game = Othello()
        self.move_log = []
        self.cursor_pos = (0, 0)  # Cursor starts at the top-left of the board

    def draw_board(self):
        """Draw the Othello board, discs, and grid labels."""
        self.screen.fill(GREEN)
        font = pygame.font.SysFont(None, 30)

        # Draw column labels
        for col in range(GRID_SIZE):
            label = font.render(chr(col + ord('a')), True, WHITE)
            self.screen.blit(label, (LABEL_SPACE + col * CELL_SIZE + CELL_SIZE // 2 - 10, LABEL_SPACE // 2 - 10))

        # Draw row labels
        for row in range(GRID_SIZE):
            label = font.render(str(row + 1), True, WHITE)
            self.screen.blit(label, (LABEL_SPACE // 2 - 10, LABEL_SPACE + row * CELL_SIZE + CELL_SIZE // 2 - 10))

        # Draw grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(LABEL_SPACE + col * CELL_SIZE, LABEL_SPACE + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)  # Draw grid lines

                # Highlight the cursor position
                if self.cursor_pos == (row, col):
                    pygame.draw.rect(self.screen, WHITE, rect, 2)

                # Draw discs
                if self.game.board[row][col] == 'X':
                    pygame.draw.circle(self.screen, BLACK, rect.center, CELL_SIZE // 3)
                elif self.game.board[row][col] == 'O':
                    pygame.draw.circle(self.screen, WHITE, rect.center, CELL_SIZE // 3)

    def draw_move_log(self, settings=None):
        """Draw the move log on the right side of the screen."""
        log_rect = pygame.Rect(WINDOW_SIZE, 0, LOG_WIDTH, WINDOW_SIZE)
        pygame.draw.rect(self.screen, WHITE, log_rect)

        font = pygame.font.SysFont(None, 30)
        log_title = font.render("Move Log", True, BLACK)
        self.screen.blit(log_title, (WINDOW_SIZE + 20, 20))

        # Show AI configuration if in AI mode
        if settings:
            ai1_info = font.render(f"AI1 Depth: {settings['AI1_depth']}, Heuristic: {settings['AI1_heuristic']}", True,
                                   BLACK)
            ai2_info = font.render(f"AI2 Depth: {settings['AI2_depth']}, Heuristic: {settings['AI2_heuristic']}", True,
                                   BLACK)
            self.screen.blit(ai1_info, (WINDOW_SIZE + 20, 50))
            self.screen.blit(ai2_info, (WINDOW_SIZE + 20, 80))

        # Display moves
        for i, move in enumerate(self.move_log[-15:], start=1):  # Show the last 15 moves
            move_text = font.render(f"{i}. {move}", True, BLACK)
            self.screen.blit(move_text, (WINDOW_SIZE + 20, 110 + i * 30))

    def update_move_log(self, player, move):
        """Update the move log with the latest move."""
        row, col = move
        self.move_log.append(f"{player}: {row + 1}{chr(col + ord('a'))}")

    def display_winner(self):
        """Display the winner on the screen."""
        black, white = self.game.count_discs()
        font = pygame.font.SysFont(None, 60)
        if black > white:
            text = font.render("Black wins!", True, BLACK)
        elif white > black:
            text = font.render("White wins!", True, BLACK)
        else:
            text = font.render("It's a draw!", True, BLACK)
        self.screen.blit(text, (WINDOW_SIZE // 4, WINDOW_SIZE // 2 - 30))
        pygame.display.flip()
        time.sleep(3)

    def get_human_move(self):
        """Allow the human to move using arrow keys and confirm with Enter."""
        valid_moves = self.game.valid_moves(self.game.current_player)
        if not valid_moves:
            return None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    row, col = self.cursor_pos
                    if event.key == pygame.K_UP:
                        row = (row - 1) % GRID_SIZE
                    elif event.key == pygame.K_DOWN:
                        row = (row + 1) % GRID_SIZE
                    elif event.key == pygame.K_LEFT:
                        col = (col - 1) % GRID_SIZE
                    elif event.key == pygame.K_RIGHT:
                        col = (col + 1) % GRID_SIZE
                    elif event.key == pygame.K_RETURN:
                        if self.cursor_pos in valid_moves:
                            return self.cursor_pos

                    self.cursor_pos = (row, col)
                    self.draw_board()
                    self.draw_move_log()
                    pygame.display.flip()

    def update_board(self, move, player):
        """Update the board and move log."""
        if move:
            self.game.make_move(move[0], move[1], player)
            self.update_move_log(player, move)
        self.draw_board()
        self.draw_move_log()
        pygame.display.flip()

    def configure_ai_settings(self):
        """Allow the user to configure AI settings for AI vs AI mode."""
        font = pygame.font.SysFont(None, 40)
        settings = {"AI1_depth": 3, "AI1_heuristic": 1, "AI2_depth": 3, "AI2_heuristic": 2}
        selected_option = 0
        options = [
            "AI 1 Depth: {}",
            "AI 1 Heuristic: {} (1: h1, 2: h2, 3: h3)",
            "AI 2 Depth: {}",
            "AI 2 Heuristic: {} (1: h1, 2: h2, 3: h3)",
            "Start Game"
        ]

        while True:
            self.screen.fill(GREEN)
            for i, option in enumerate(options):
                text_color = BLACK if i == selected_option else WHITE
                value = settings["AI1_depth"] if i == 0 else (
                    settings["AI1_heuristic"] if i == 1 else (
                        settings["AI2_depth"] if i == 2 else (
                            settings["AI2_heuristic"] if i == 3 else "")))
                rendered_text = font.render(option.format(value), True, text_color)
                self.screen.blit(rendered_text, (WINDOW_SIZE // 4, 100 + i * 60))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if selected_option in [0, 2]:  # Depth settings
                            key = "AI1_depth" if selected_option == 0 else "AI2_depth"
                            settings[key] = max(1, min(10, settings[key] + (1 if event.key == pygame.K_RIGHT else -1)))
                        elif selected_option in [1, 3]:  # Heuristic settings
                            key = "AI1_heuristic" if selected_option == 1 else "AI2_heuristic"
                            settings[key] = max(1, min(3, settings[key] + (1 if event.key == pygame.K_RIGHT else -1)))
                    elif event.key == pygame.K_RETURN and selected_option == 4:
                        return settings

    def run_game(self, mode, settings=None):
        """Run the Othello game."""
        if settings and mode == "ai_vs_ai":
            ai_player1 = AIPlayer(depth=settings["AI1_depth"], heuristic=settings["AI1_heuristic"])
            ai_player2 = AIPlayer(depth=settings["AI2_depth"], heuristic=settings["AI2_heuristic"])
        else:
            ai_player1 = AIPlayer(depth=3, heuristic=1)
            ai_player2 = AIPlayer(depth=3, heuristic=2)

        while not self.game.is_game_over():
            self.draw_board()
            self.draw_move_log(settings)
            pygame.display.flip()
            time.sleep(0.5)  # Delay to visualize moves

            if mode == "human_vs_human":
                move = self.get_human_move()
            elif mode == "human_vs_ai":
                if self.game.current_player == 'X':
                    move = self.get_human_move()
                else:
                    print("AI is thinking...")
                    _, move = ai_player2.minimax(self.game, ai_player2.depth, -float('inf'), float('inf'), True, 'O')
                    print(f"AI chose move: {move}")
            elif mode == "ai_vs_ai":
                if self.game.current_player == 'X':
                    print("AI Player 1 is thinking...")
                    _, move = ai_player1.minimax(self.game, ai_player1.depth, -float('inf'), float('inf'), True, 'X')
                    print(f"AI Player 1 chose move: {move}")
                else:
                    print("AI Player 2 is thinking...")
                    _, move = ai_player2.minimax(self.game, ai_player2.depth, -float('inf'), float('inf'), True, 'O')
                    print(f"AI Player 2 chose move: {move}")
            else:
                move = None

            self.update_board(move, self.game.current_player)
            self.game.current_player = 'O' if self.game.current_player == 'X' else 'X'

        self.draw_board()
        self.draw_move_log(settings)
        self.display_winner()

    def main_menu(self):
        """Display the main menu and allow mode selection."""
        font = pygame.font.SysFont(None, 60)
        menu_items = ["Human vs Human", "Human vs AI", "AI vs AI"]
        selected_index = 0

        while True:
            self.screen.fill(GREEN)
            for i, item in enumerate(menu_items):
                color = BLACK if i == selected_index else WHITE
                text = font.render(item, True, color)
                self.screen.blit(text, (WINDOW_SIZE // 4, 150 + i * 80))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:
                            self.run_game("human_vs_human")
                        elif selected_index == 1:
                            settings = self.configure_ai_settings()  # Reuse the AI settings method
                            self.run_game("human_vs_ai", settings)
                        elif selected_index == 2:
                            settings = self.configure_ai_settings()
                            self.run_game("ai_vs_ai", settings)
                        return


if __name__ == "__main__":
    visual_othello = VisualOthelloScreen()
    visual_othello.main_menu()