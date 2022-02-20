import pygame, sys
from base import core
from base.warnsdorff_heuristic import WarnsdorffHeuristic
from queens_animation import Queen
import random


class Knight(Queen):
    def __init__(self, x: int, y: int, objlen: int, boxlen: int) -> None:
        super().__init__(x, y, objlen, boxlen, image_name="wKnight.png")
        self.mx = [1, 1, 2, 2, -1, -1, -2, -2]  # movement in x-axis
        self.my = [2, -2, 1, -1, 2, -2, 1, -1]  # movement in y-axis
    
    def move_to(self, grid: list, dest: tuple) -> None:
        nx, ny = dest  # new x, new y
        velx, vely = 1 if nx - self.x >= 0 else -1, 1 if ny - self.y >= 0 else -1
        ox, oy = self.x, self.y
        # move on x-axis
        while self.x != nx:
            pygame.time.delay(500)  # 100
            self.x += velx
            core.screen.blit(self.surf, self.obj_left_corner)
            core.screen.blit(grid[self.x - velx][self.y].surf, grid[self.x - velx][self.y].box_left_corner)
            pygame.display.flip()

        # move on y-axis
        while self.y != ny:
            pygame.time.delay(500)  # 100
            self.y += vely
            core.screen.blit(self.surf, self.obj_left_corner)
            core.screen.blit(grid[self.x][self.y - vely].surf, grid[self.x][self.y - vely].box_left_corner)
            pygame.display.flip()

        grid[ox][oy].surf.fill(core.GREEN)
        grid[ox][oy].surf.fill(core.GRAY, rect=grid[ox][oy].surf.get_rect().inflate(-25, -25))
        core.screen.blit(grid[ox][oy].surf, grid[ox][oy].box_left_corner)
        pygame.display.flip()
        
    def perform_next_move(self, grid: list, sol: list, origin: tuple, move_id: int) -> tuple:
        x, y = origin
        nx, ny = x, y
        # choose the first movement to try out (randomly)
        start = random.randint(0, len(self.mx) - 1)
        # try out all possible movements
        for k in range(0, len(self.mx)):
            # i can take any values in [0,1,2,...,7]
            i = (start + k) % len(self.mx)
            nx = x + self.mx[i]  # new x coordenate
            ny = y + self.my[i]  # new y coordenate
            if 0 <= nx < 8 and 0 <= ny < 8 and sol[nx][ny] == move_id:
                self.move_to(grid, (nx, ny))
                break
        return nx, ny


def draw_knight(grid: list, origin: tuple, objroom: int = 0.59) -> Knight:
    # returns queens: List[Queen]
    boxlen = grid[0][0].boxlen
    objlen = int(boxlen * min(objroom, 0.70))
    return Knight(x=origin[0], y=origin[1], objlen=objlen, boxlen=boxlen)


def main() -> None:
    # set caption
    pygame.display.set_caption("Knight's Tour")

    # draw grid and queens 
    grid = core.draw_board()

    # set max frames per second
    clock = pygame.time.Clock()
    run = True
    FPS = 60

    # solution 
    board_size = 8
    tour = WarnsdorffHeuristic(board_size=board_size)
    sol = tour.build()  # solution is a N x N matrix representing the tour
    
    # draw knight
    orig = tour.xo, tour.yo
    move_id = sol[orig[0]][orig[1]] + 1
    wKnight = draw_knight(grid, orig)

    # start animation 
    while run:
        clock.tick(FPS)
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            # close window to kill the program
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # use [esc] or [q] keys to kill the program
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                sys.exit()
            # use [return] key to drive the animation
            elif event.key == pygame.K_RETURN:
                orig = wKnight.perform_next_move(grid, sol, orig, move_id)
                move_id = (move_id + 1) % (board_size * board_size)
                if move_id == 1:
                    grid = core.draw_board()
                    wKnight = draw_knight(grid, orig)
                pygame.event.clear()


if __name__ == "__main__":
    main()
