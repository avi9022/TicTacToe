import random
import pygame


# TODO :: Gme class should have its own file
# TODO :: Must inherit from something
class Game:
    GAME_FONT = None

    # TODO :: Private variables start with double underscore
    # TODO  :: cell_size should come in init
    def __init__(self):
        self.x_img = pygame.transform.scale(pygame.image.load('graphics/Xs.png').convert_alpha(), (100, 100))
        self.o_img = pygame.transform.scale(pygame.image.load('graphics/Os.png').convert_alpha(), (100, 100))
        self.comp_player = ComputerPlayer()
        pygame.transform.scale(self.o_img, (50, 50))

        # TODO :: variable do  not start with  upper case
        self.X_turn = True
        self.winner = None
        self.against_computer = True
        self.filled_cells = 0
        self.is_first_game = True
        # a 2D list that holds all game cells and their content(None = empty, True = X, False = O)
        self.cells = []
        for column in range(0, 3):
            for row in range(0, 3):
                cell_rect = pygame.Rect(cell_size * row + 30, cell_size * column + 30, cell_size, cell_size)
                # TODO :: dict
                self.cells.append([cell_rect, None])

    def draw_table(self) -> None:
        pygame.draw.line(screen, 'Black', ((WIDTH / 3), 30), ((WIDTH / 3), HEIGHT - 30), 10)
        pygame.draw.line(screen, 'Black', ((WIDTH / 3) * 2, 30), ((WIDTH / 3) * 2, HEIGHT - 30), 10)
        pygame.draw.line(screen, 'Black', (30, (HEIGHT / 3)), (WIDTH - 30, (HEIGHT / 3)), 10)
        pygame.draw.line(screen, 'Black', (30, (HEIGHT / 3) * 2), (WIDTH - 30, (HEIGHT / 3) * 2), 10)

    def draw_symbol(self, symbol):
        # TODO :: what if symbol is smaller len then 2
        if symbol[1]:
            screen.blit(self.x_img, symbol[0])
        else:
            screen.blit(self.o_img, symbol[0])

    def check_cell_collision(self, mouse_pos):
        for rect in self.cells:
            if rect[0].collidepoint(mouse_pos) and rect[1] is None:
                self.update_grid(rect)
            else:
                continue

    def update_grid(self, rect_to_update):
        rect_to_update[1] = self.X_turn
        self.X_turn = not self.X_turn
        self.filled_cells += 1
        self.draw_symbol(rect_to_update)
        self.check_winner(rect_to_update)
        if self.against_computer and self.filled_cells < 8 and is_active:
            new_grid_state = self.comp_player.next_turn(self.cells, rect_to_update)
            self.cells = new_grid_state[0]
            self.draw_symbol(self.cells[new_grid_state[1]])
            self.filled_cells += 1
            self.X_turn = True
            self.check_winner(self.cells[new_grid_state[1]])

    def get_row_column_collection(self, current_move) -> tuple:
        row_collection = 0
        column_collection = 0
        for rect in self.cells:
            if rect[1] is not None and rect[1] == current_move[1]:
                if rect[0].y == current_move[0].y:
                    row_collection += 1
                if rect[0].x == current_move[0].x:
                    column_collection += 1

        return row_collection, column_collection, current_move

    def check_winner(self, current_move):
        global is_active
        # 2 variables that hold how many of the same symbol we  have in a given row or column
        (row_collection, column_collection, current_move) = self.get_row_column_collection(current_move)

        if row_collection == 3 or column_collection == 3:
            is_active = False
            self.winner = current_move[1]
        if self.cells[0][1] is not None and \
                self.cells[0][1] == self.cells[4][1] and \
                self.cells[0][1] == self.cells[8][1]:
            is_active = False
            self.winner = self.cells[0][1]
        elif self.cells[2][1] is not None and self.cells[2][1] == self.cells[4][1] and self.cells[2][1] == \
                self.cells[6][1]:
            is_active = False
            self.winner = self.cells[2][1]

        if self.filled_cells == 9:
            is_active = False

    def game_over(self, winner):
        if winner is not None:
            if winner:
                winner_surface = game_font.render("X's Won!", False, 'Black')
            else:
                winner_surface = game_font.render("O's Won!", False, 'Black')
            winner_rect = winner_surface.get_rect(center=(screen.get_width() / 2, 50))
            screen.blit(winner_surface, winner_rect)
        elif not self.is_first_game:
            winner_surface = game_font.render("Its a Draw!", False, 'Black')
            winner_rect = winner_surface.get_rect(center=(screen.get_width() / 2, 50))
            screen.blit(winner_surface, winner_rect)
        instructions_surface = game_font.render("Press SPACE to Restart", False, 'Black')
        instructions_rect = instructions_surface.get_rect(center=(screen.get_width() / 2, 300))
        screen.blit(instructions_surface, instructions_rect)

    def update(self):
        self.draw_table()


class ComputerPlayer:
    def __init__(self):
        self.is_first_turn = True

    def next_turn(self, current_grid, opponent_last_move) -> tuple:
        if self.is_first_turn:
            return self.randomize_turn(current_grid)
        else:
            possible_win = self.check_possible_win(current_grid)
            if possible_win is not None:
                return possible_win
            else:
                return self.check_if_about_to_lose(current_grid, opponent_last_move)

    def randomize_turn(self, current_grid) -> tuple:
        self.is_first_turn = False
        new_grid = current_grid
        turn = random.randint(0, 8)
        while new_grid[turn][1] is not None:
            turn = random.randint(0, 8)
        new_grid[turn][1] = False
        return new_grid, turn

    def check_possible_win(self, current_grid):
        new_grid = current_grid
        for current_rect in current_grid:
            if not current_rect[1]:
                (row_collection, column_collection, current_move) = game.get_row_column_collection(current_rect)
                if row_collection == 2:
                    for cell in new_grid:
                        if cell[0].y == current_rect[0].y and cell[1] is None:
                            cell[1] = False
                            return new_grid, new_grid.index(cell)
                if column_collection == 2:
                    for cell in new_grid:
                        if cell[0].x == current_rect[0].x and cell[1] is None:
                            cell[1] = False
                            return new_grid, new_grid.index(cell)
        first_diagonal_collection, second_diagonal_collection = self.get_diagnol_collection(new_grid, False)
        print(first_diagonal_collection, second_diagonal_collection)
        if first_diagonal_collection == 2:
            for cell in new_grid[0::4]:
                if cell[1] is None:
                    cell[1] = False
                    return new_grid, new_grid.index(cell)
        if second_diagonal_collection == 2:
            for cell in new_grid[2:7:2]:
                if cell[1] is None:
                    cell[1] = False
                    return new_grid, new_grid.index(cell)
        return None

    def check_if_about_to_lose(self, current_grid, opponent_last_move) -> tuple:
        new_grid = current_grid
        (row_collection, column_collection, current_move) = game.get_row_column_collection(opponent_last_move)
        first_diagonal_collection, second_diagonal_collection = self.get_diagnol_collection(new_grid, True)
        if row_collection == 2:
            for cell in new_grid:
                if cell[0].y == opponent_last_move[0].y and cell[1] is None:
                    cell[1] = False
                    return new_grid, new_grid.index(cell)
        if column_collection == 2:
            for cell in new_grid:
                if cell[0].x == opponent_last_move[0].x and cell[1] is None:
                    cell[1] = False
                    return new_grid, new_grid.index(cell)
        if first_diagonal_collection == 2:
            for cell in new_grid[0::4]:
                if cell[1] is None:
                    cell[1] = False
                    return new_grid, new_grid.index(cell)
        if second_diagonal_collection == 2:
            for cell in new_grid[2:7:2]:
                if cell[1] is None:
                    cell[1] = False
                    return new_grid, new_grid.index(cell)

        return self.randomize_turn(new_grid)

    def get_diagnol_collection(self, grid, symbol):
        first_diagonal_collection = 0
        second_diagonal_collection = 0

        for cell in grid[0::4]:
            if cell[1] == symbol:
                first_diagonal_collection += 1

        for cell in grid[2:7:2]:
            if cell[1] == symbol:
                second_diagonal_collection += 1

        return first_diagonal_collection, second_diagonal_collection


pygame.init()
game_font = pygame.font.Font('graphics/Pixeltype.ttf', 50)
cell_size = 130
cell_number = 3
WIDTH = cell_size * cell_number + 30
HEIGHT = cell_size * cell_number + 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((230, 230, 255))
clock = pygame.time.Clock()
game = Game()

is_active = False

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and is_active:
            if game.against_computer:
                if game.X_turn:
                    pos = pygame.mouse.get_pos()
                    game.check_cell_collision(pos)
                else:
                    pass
            else:
                pos = pygame.mouse.get_pos()
                game.check_cell_collision(pos)
        if not is_active and keys[pygame.K_SPACE]:
            screen.fill((230, 230, 255))
            is_active = True
            game.__init__()
            game.is_first_game = False

    if is_active:
        game.update()

    else:
        screen.fill((230, 230, 255))
        game.game_over(game.winner)
    pygame.display.update()
    clock.tick(60)


def main():
    pass


if __name__ == "__main__":
    main()
