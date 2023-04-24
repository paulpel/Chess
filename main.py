import pygame
import os
import numpy as np


class Chess:
    def __init__(self) -> None:
        self.size = 800

        self.assets = os.path.join(os.getcwd(), "Assets")
        self.win = pygame.display.set_mode((self.size, self.size))
        self.fill = (154, 140, 152)
        self.fps = 60
        pygame.display.set_caption("Chess")

        pygame_icon = pygame.image.load(os.path.join(self.assets, "chess.png"))
        pygame.display.set_icon(pygame_icon)

        pygame.font.init()
        font_size = int(self.size / 8)
        self.my_font = pygame.font.SysFont("segoeuisymbol", font_size)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.board = ((201, 173, 167), (74, 78, 105))
        self.current_pos = None
        self.figure = None
        self.white_turn = True
        self.available = []

        self.chrs = {
            "p": self.my_font.render("\u265F", True, self.black),
            "r": self.my_font.render("\u265C", True, self.black),
            "k": self.my_font.render("\u265E", True, self.black),
            "b": self.my_font.render("\u265D", True, self.black),
            "ki": self.my_font.render("\u265A", True, self.black),
            "q": self.my_font.render("\u265B", True, self.black),
            "P": self.my_font.render("\u2659", True, self.white),
            "R": self.my_font.render("\u2656", True, self.white),
            "K": self.my_font.render("\u2658", True, self.white),
            "B": self.my_font.render("\u2657", True, self.white),
            "KI": self.my_font.render("\u2654", True, self.white),
            "Q": self.my_font.render("\u2655", True, self.white),
        }

        self.position = [
            ["R", "K", "B", "Q", "KI", "B", "K", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "k", "b", "q", "ki", "b", "k", "r"],
        ]
        self.position = np.transpose(self.position)
        self.position = np.flip(self.position, axis=1)

    def main(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if self.current_pos:
                        new_pos = (int(x / (self.size / 8)), int(y / (self.size / 8)))
                        self.move(self.current_pos, new_pos, self.figure)
                        self.available = []
                    else:
                        self.current_pos = (
                            int(x / (self.size / 8)),
                            int(y / (self.size / 8)),
                        )
                        self.figure = self.position[self.current_pos[0]][
                            self.current_pos[1]
                        ]
                        self.available = self.available_moves(
                            self.current_pos, self.figure
                        )

                    if (
                        self.figure == "-"
                        or (self.white_turn and self.figure.islower())
                        or (not self.white_turn and self.figure.isupper())
                    ):
                        self.current_pos = None
                        self.available = []

            self.draw_board(self.current_pos, self.available)

        pygame.quit()

    def available_moves(self, pos, figure):
        possible = []
        row_p = pos[1]
        col_p = pos[0]
        if figure == "P":
            if self.position[col_p][row_p - 1] == "-":
                possible.append((col_p, row_p - 1))
                if row_p == 6 and self.position[col_p][row_p - 2] == "-":
                    possible.append((col_p, row_p - 2))
            if col_p != 0:
                if self.position[col_p - 1][row_p - 1].islower():
                    possible.append((col_p - 1, row_p - 1))
            if col_p != 7:
                if self.position[col_p + 1][row_p - 1].islower():
                    possible.append((col_p + 1, row_p - 1))
        elif figure == "p":
            if self.position[col_p][row_p + 1] == "-":
                possible.append((col_p, row_p + 1))
                if row_p == 1 and self.position[col_p][row_p + 2] == "-":
                    possible.append((col_p, row_p + 2))
            if col_p != 0:
                if self.position[col_p - 1][row_p + 1].isupper():
                    possible.append((col_p - 1, row_p + 1))
            if col_p != 7:
                if self.position[col_p + 1][row_p + 1].isupper():
                    possible.append((col_p + 1, row_p + 1))
        elif figure in ("k", "K"):
            moves = [
                [2, 1],
                [1, 2],
                [-2, 1],
                [-2, -1],
                [2, -1],
                [-1, -2],
                [-1, 2],
                [1, -2],
            ]
            possible = self.check_moves(moves, figure, col_p, row_p, True)
        elif figure in ("b", "B"):
            moves = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
            possible = self.check_moves(moves, figure, col_p, row_p)
        elif figure in ("r", "R"):
            moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            possible = self.check_moves(moves, figure, col_p, row_p)
        elif figure in ("q", "Q"):
            moves = [
                [1, 0],
                [0, 1],
                [-1, 0],
                [0, -1],
                [1, 1],
                [-1, 1],
                [1, -1],
                [-1, -1],
            ]
            possible = self.check_moves(moves, figure, col_p, row_p)
        elif figure in ("ki", "KI"):
            moves = [
                [1, 0],
                [0, 1],
                [-1, 0],
                [0, -1],
                [1, 1],
                [-1, 1],
                [1, -1],
                [-1, -1],
            ]
            possible = self.check_moves(moves, figure, col_p, row_p, True)
        else:
            for i in range(8):
                for j in range(8):
                    possible.append((i, j))
        return possible

    def check_moves(self, moves, figure, col_p, row_p, brk=False):
        possible = []
        for move in moves:
            x, y = col_p, row_p
            cont = False
            while True:
                x += move[0]
                y += move[1]
                dest = (x, y)
                if 0 <= x < 8 and 0 <= y < 8:
                    if self.position[dest[0]][dest[1]] == "-":
                        # checkmate check
                        possible.append(dest)
                    else:
                        cont = True
                        if self.position[x][y].islower() != figure.islower():
                            possible.append(dest)
                        break
                else:
                    cont = True
                    break
                if brk:
                    break
            if cont:
                continue
        return possible

    def move(self, current, dest, figure):
        if dest in self.available:
            self.position[current[0]][current[1]] = "-"
            self.position[dest[0]][dest[1]] = figure
            self.white_turn = not self.white_turn
        else:
            self.current_pos = None

    def draw_board(self, highlight=None, available=None):
        self.win.fill(self.fill)
        size_sqr = self.size / 8
        for i in range(8):
            for j in range(8):
                if i % 2 == j % 2:
                    pygame.draw.rect(
                        self.win,
                        self.board[0],
                        (i * size_sqr, j * size_sqr, size_sqr, size_sqr),
                    )
                else:
                    pygame.draw.rect(
                        self.win,
                        self.board[1],
                        (i * size_sqr, j * size_sqr, size_sqr, size_sqr),
                    )

        s = pygame.Surface((size_sqr, size_sqr))
        s.fill((80, 200, 120))
        if highlight:
            s.set_alpha(100)
            self.win.blit(s, (highlight[0] * size_sqr, highlight[1] * size_sqr))

        for move in available:
            s.set_alpha(50)
            self.win.blit(s, (move[0] * size_sqr, move[1] * size_sqr))

        for i in range(8):
            for j in range(8):
                if self.position[i][j] != "-":
                    self.t = self.win.blit(
                        self.chrs[self.position[i][j]],
                        (i * size_sqr, j * size_sqr - size_sqr / 5),
                    )

        pygame.display.update()


if __name__ == "__main__":
    chess_obj = Chess()
    chess_obj.main()
