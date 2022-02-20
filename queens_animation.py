import pygame, sys
from base.queens_solver import n_queens_solver
from base import core


class Queen(core.BoxObject):
    def __init__(self, x: int, y: int, objlen: int, boxlen: int, image_name: str = "wQueen.png") -> None:
        super().__init__(x, y, boxlen)
        self.objlen = objlen  # size of piece 
        self.surf = pygame.transform.scale(pygame.image.load(f"images/{image_name}"), (self.objlen, self.objlen))
        core.screen.blit(self.surf, self.obj_left_corner)
        pygame.display.flip()

    @property
    def obj_left_corner(self) -> tuple:
        # upper left corner of piece
        c_y, c_x = self.box_center
        return c_y - self.objlen//2, c_x - self.objlen//2 

    def move_to(self, grid: list, dest: tuple) -> None:
        new_x, _ = dest
        vel = 1 if new_x >= self.x else -1
        while new_x != self.x:
            pygame.time.delay(50) # 100
            self.x += vel
            core.screen.blit(self.surf, self.obj_left_corner)
            core.screen.blit(grid[self.x - vel][self.y].surf, grid[self.x - vel][self.y].box_left_corner)
            pygame.display.flip()


def draw_queens(grid: list, config: list, objroom: int = 0.59) -> list:
    # returns queens: List[Queen]
    boxlen = grid[0][0].boxlen
    objlen = int(boxlen * min(objroom, 0.70))
    return [Queen(x=row, y=col, objlen=objlen, boxlen=boxlen) for col, row in enumerate(config)]


def set_text(message :str) -> None:
    font = pygame.font.Font('freesansbold.ttf', 28)
    text = font.render(message, True, core.YELLOW, core.BLACK)
    t1, t2 = text.get_size()
    core.screen.blit(text, (core.WIDTH//2 - t1//2, core.HEIGHT//2 - t2//2))
    pygame.display.flip()


def main() -> None:
    # set caption
    pygame.display.set_caption("8 Queens Problem")

    # draw grid and queens 
    grid = core.draw_board()
    Q = draw_queens(grid, config=[0]*8)

    # set max frames per second
    clock = pygame.time.Clock()
    run = True
    FPS = 60

    # get solutions with a light representation
    solver = n_queens_solver(board_size=8)
    # each configuration is a list where index -> colum and config[index] -> row.   
    configs = [[0]*8] # "stand by" configuration 
    configs.extend(solver.get_solutions())

    # start animation 
    set_text(message="Stand  by!!!")
    frame_id = 1
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
                # change configuration
                message = f"Solution {frame_id}" if frame_id else "Stand  by!!!"
                for j, queen in enumerate(Q):
                    i = configs[frame_id][j]
                    queen.move_to(grid, dest=(i, j))
                frame_id = (frame_id + 1) % len(configs)
                set_text(message=message)
                pygame.time.delay(100)
                pygame.event.clear()


if __name__ == "__main__":
    main()
