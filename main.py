import sys
import pygame as pg

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


class TicTacToe:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Tic Tac Toe")
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

    def run(self):
        self.draw_grid()
        player = 'X'
        game_over = False
        while game_over is False:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.check_draw():
                    game_over = True
                    break
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]  # X
                    mouseY = event.pos[1]  # Y
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    if self.board[clicked_row][clicked_col] is None:
                        self.board[clicked_row][clicked_col] = player
                        if self.check_win(player):
                            game_over = True
                        else:
                            player = 'O'
                            _, position = self.minimax(self.board, True)
                            if position:
                                self.board[position[0]][position[1]] = player
                                if self.check_win('O'):
                                    game_over = True
                                    break
                            player = 'X'

            self.draw_figures()
            pg.display.update()

        pg.time.wait(1000)
        self.screen.fill(BG_COLOR)
        self.show_msg("You won!" if self.check_win('X') else "You lost!" if self.check_win('O') else "Draw!")

    def minimax(self, board, is_maximizing):
        if self.check_win('O'):
            return 1, None
        elif self.check_win('X'):
            return -1, None
        elif self.check_draw():
            return 0, None

        if is_maximizing:
            best_score = -float('inf')
            best_position = None
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board[row][col] is None:
                        board[row][col] = 'O'
                        score, _ = self.minimax(board, False)
                        board[row][col] = None
                        if score > best_score:
                            best_score = score
                            best_position = (row, col)
            return best_score, best_position
        else:
            best_score = float('inf')
            best_position = None
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board[row][col] is None:
                        board[row][col] = 'X'
                        score, _ = self.minimax(board, True)
                        board[row][col] = None
                        if score < best_score:
                            best_score = score
                            best_position = (row, col)
            return best_score, best_position

    def draw_grid(self):
        pg.draw.line(self.screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pg.draw.line(self.screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        pg.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pg.draw.line(self.screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 'O':
                    pg.draw.circle(self.screen, CIRCLE_COLOR, (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == 'X':
                    pg.draw.line(self.screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                    pg.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

    def check_win(self, player):
        for col in range(BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True
        for row in range(BOARD_ROWS):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == player:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def check_draw(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] is None:
                    return False
        return True

    def show_msg(self, text):
        font = pg.font.SysFont(None, 100)
        text = font.render(text, True, (255, 255, 255))
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pg.display.update()
        pg.time.wait(2000)
        self.restart()

    def restart(self):
        self.__init__()
        self.run()


if __name__ == "__main__":
    TicTacToe().run()
