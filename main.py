import pygame
import os

class Chess:
    def __init__(self) -> None:
        self.size = 800

        self.assets = os.path.join(os.getcwd(), "Assets")
        self.win = pygame.display.set_mode((self.size, self.size))
        self.fill = (154, 140, 152)
        self.fps = 60
        pygame.display.set_caption('Chess')

        pygame_icon = pygame.image.load(os.path.join(self.assets, "chess.png"))
        pygame.display.set_icon(pygame_icon)

        pygame.font.init()
        font_size = int(self.size/8)
        seguisy80 = pygame.font.SysFont("segoeuisymbol", font_size)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.board = ((201, 173, 167), (74, 78, 105))

        self.chrs = {
            'b_pawn': seguisy80.render('\u265F', True, self.black),
            'b_rook': seguisy80.render('\u265C', True, self.black),
            'b_knight': seguisy80.render('\u265E', True, self.black),
            'b_bishop': seguisy80.render('\u265D', True, self.black),
            'b_king': seguisy80.render('\u265A', True, self.black),
            'b_queen': seguisy80.render('\u265B', True, self.black),
            'w_pawn': seguisy80.render('\u2659', True, self.white),
            'w_rook': seguisy80.render('\u2656', True, self.white),
            'w_knight': seguisy80.render('\u2658', True, self.white),
            'w_bishop': seguisy80.render('\u2657', True, self.white),
            'w_king': seguisy80.render('\u2658', True, self.white),
            'w_queen': seguisy80.render('\u2655', True, self.white),
        }

    def main(self):
        clock = pygame.time.Clock()
        run = True
        self.draw_board()

        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def draw_board(self):
        self.win.fill(self.fill)

        size_sqr = self.size/8
        for i in range(8):
            for j in range(8):
                if i%2 == j%2:
                    pygame.draw.rect(
                        self.win,
                        self.board[0],
                        (i*size_sqr, j*size_sqr, size_sqr, size_sqr))
                else:
                    pygame.draw.rect(
                        self.win,
                        self.board[1],
                        (i*size_sqr, j*size_sqr, size_sqr, size_sqr))
        pygame.display.update()


if __name__ == "__main__":
    chess_obj = Chess()
    chess_obj.main()
