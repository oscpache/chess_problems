import pygame
import sys


WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 47, 79, 79
YELLOW = 249, 186, 55
GREEN = 0, 128, 0

WIDTH, HEIGHT = 560, 560
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()


class BoxObject:
    def __init__(self, x: int, y: int, boxlen: int) -> None:
        self.x = x
        self.y = y
        self.boxlen = boxlen  # box lenght

    @property
    def box_center(self) -> tuple:
        # center of square and piece
        lc_y, lc_x = self.box_left_corner
        return lc_y + self.boxlen//2, lc_x + self.boxlen//2

    @property
    def box_left_corner(self) -> tuple:
        # upper left corner of square
        return self.y * self.boxlen, self.x * self.boxlen


class Square(BoxObject):
    def __init__(self, x: int, y: int, boxlen: int) -> None:
        super().__init__(x, y, boxlen)
        self.surf = pygame.Surface((self.boxlen, self.boxlen))
        self.surf.fill(self.color)
        screen.blit(self.surf, self.box_left_corner)
        pygame.display.flip()

    @property
    def color(self) -> tuple:
        return BLACK if (self.x % 2 == 0) ^ (self.y % 2 == 0) else WHITE


def draw_board(dim: int = 8) -> list:
    # returns grid: List[List[Square]]
    if WIDTH % dim != 0:
        print("BoardError: screen size and board size are incompatible!")
        sys.exit()
    return [[Square(x=i, y=j, boxlen=WIDTH//dim) for j in range(dim)] for i in range(dim)]
