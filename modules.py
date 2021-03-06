import pygame
import random
import asyncio


class Game(object):
    def __init__(self, screen, width, height):
        self.GAME_FONT = pygame.font.Font('graphics/_pixeltype.ttf', 50)
        self.clock = pygame.time.Clock()
        self.pudding = 30
        self.cell_size = (width - self.pudding) / 3
        self.cell_number = 3
        self.width = width
        self.height = height
        self.surface = screen
        self.is_active = False
        self.x_img = pygame.transform.scale(pygame.image.load('graphics/_xs.png').convert_alpha(), (100, 100))
        self.o_img = pygame.transform.scale(pygame.image.load('graphics/_o.png').convert_alpha(), (100, 100))
        self.comp_player = ComputerPlayer()
        self.x_turn = True
        self.winner = None
        self.against_computer = False
        self.filled_cells = 0
        self.is_first_game = True
        # a 2D list that holds all game cells and their content(None = empty, True = X, False = O)
        self.cells = []

    async def start(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    exit()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_active:
                        if self.against_computer:
                            if self.x_turn:
                                pos = pygame.mouse.get_pos()
                                await self.check_cell_collision(pos)
                            else:
                                pass
                        else:
                            pos = pygame.mouse.get_pos()
                            await self.check_cell_collision(pos)
                    click = True
                if keys[pygame.K_SPACE] and not self.is_first_game and not self.is_active:
                    self.is_active = True
                    self.restart_game()

            if self.is_first_game:
                self.main_menu(click)
            elif self.is_active:
                self.update()
            else:
                self.surface.fill((230, 230, 255))
                self.game_over(self.winner)
            pygame.display.update()
            self.clock.tick(60)

    def init_grid(self) -> list:
        new_grid = []
        for column in range(0, 3):
            for row in range(0, 3):
                cell_rect = pygame.Rect(self.cell_size * row + self.pudding + 5,
                                        self.cell_size * column + self.pudding + 5, self.cell_size, self.cell_size)
                new_grid.append([cell_rect, None])
        return new_grid

    def restart_game(self):
        self.surface.fill((230, 230, 255))
        self.is_active = True
        self.comp_player = ComputerPlayer()
        self.x_turn = True
        self.winner = None
        self.filled_cells = 0
        self.cells = self.init_grid()

    def draw_table(self) -> None:
        pygame.draw.line(self.surface, 'Black', ((self.width / 3), self.pudding),
                         ((self.width / 3), self.height - self.pudding), 10)
        pygame.draw.line(self.surface, 'Black', ((self.width / 3) * 2, self.pudding),
                         ((self.width / 3) * 2, self.height - self.pudding), 10)
        pygame.draw.line(self.surface, 'Black', (30, (self.height / 3)), (self.width - self.pudding, (self.height / 3)),
                         10)
        pygame.draw.line(self.surface, 'Black', (30, (self.height / 3) * 2),
                         (self.width - self.pudding, (self.height / 3) * 2), 10)

    async def draw_symbol(self, symbol):
        if len(symbol) == 2:
            if symbol[1]:
                self.surface.blit(self.x_img, symbol[0])
            else:
                self.surface.blit(self.o_img, symbol[0])
        await asyncio.sleep(1)

    async def check_cell_collision(self, mouse_pos):
        for rect in self.cells:
            if rect[0].collidepoint(mouse_pos) and rect[1] is None:
                await self.update_game_move(rect)
            else:
                continue

    async def update_game_move(self, rect_to_update):
        rect_to_update[1] = self.x_turn
        self.x_turn = not self.x_turn
        self.filled_cells += 1
        await self.draw_symbol(rect_to_update)
        self.check_winner(rect_to_update)
        if self.against_computer and self.filled_cells < 8 and self.is_active:
            new_grid_state = await self.comp_player.next_turn(self.cells, rect_to_update)
            self.cells = new_grid_state[0]
            await self.draw_symbol(self.cells[new_grid_state[1]])
            self.filled_cells += 1
            self.x_turn = True
            self.check_winner(self.cells[new_grid_state[1]])

    @staticmethod
    def get_row_column_collection(grid, current_move) -> tuple:
        row_collection = 0
        column_collection = 0
        for rect in grid:
            if rect[1] is not None and rect[1] == current_move[1]:
                if rect[0].y == current_move[0].y:
                    row_collection += 1
                if rect[0].x == current_move[0].x:
                    column_collection += 1

        return row_collection, column_collection, current_move

    def check_winner(self, current_move):
        # 2 variables that hold how many of the same symbol we  have in a given row or column
        (row_collection, column_collection, current_move) = self.get_row_column_collection(self.cells, current_move)

        if row_collection == 3 or column_collection == 3:
            self.is_active = False
            self.winner = current_move[1]
        if self.cells[0][1] is not None and \
                self.cells[0][1] == self.cells[4][1] and \
                self.cells[0][1] == self.cells[8][1]:
            self.is_active = False
            self.winner = self.cells[0][1]
        elif self.cells[2][1] is not None and self.cells[2][1] == self.cells[4][1] and self.cells[2][1] == \
                self.cells[6][1]:
            self.is_active = False
            self.winner = self.cells[2][1]

        if self.filled_cells == 9:
            self.is_active = False

    def game_over(self, winner):
        if winner is not None:
            if winner:
                winner_surface = self.GAME_FONT.render("X's Won!", False, 'Black')
            else:
                winner_surface = self.GAME_FONT.render("O's Won!", False, 'Black')
            winner_rect = winner_surface.get_rect(center=(self.surface.get_width() / 2, 50))
            self.surface.blit(winner_surface, winner_rect)
        elif not self.is_first_game:
            winner_surface = self.GAME_FONT.render("Its a Draw!", False, 'Black')
            winner_rect = winner_surface.get_rect(center=(self.surface.get_width() / 2, 50))
            self.surface.blit(winner_surface, winner_rect)
        instructions_surface = self.GAME_FONT.render("Press SPACE to Restart", False, 'Black')
        instructions_rect = instructions_surface.get_rect(center=(self.surface.get_width() / 2, 300))
        self.surface.blit(instructions_surface, instructions_rect)

    def update(self):
        self.draw_table()

    def main_menu(self, is_pressed):
        mx, my = pygame.mouse.get_pos()

        title_text = self.GAME_FONT.render('Pixel Tic Tac Toe', True, 'Black')
        comp_play_text = self.GAME_FONT.render('Challenge the COMPUTER!', True, 'Black')
        single_play_text = self.GAME_FONT.render('Play with a friend', True, 'Black')

        title_rect = title_text.get_rect(midtop=(self.width / 2, 50))
        comp_play_text_rect = comp_play_text.get_rect(midtop=(self.width / 2, title_rect.y + 200))
        comp_play_button = pygame.Rect(comp_play_text_rect.x - 20, comp_play_text_rect.y - 10, 400, 50)
        single_play_text_rect = single_play_text.get_rect(midtop=(self.width / 2, comp_play_button.bottom + 30))
        single_play_button = pygame.Rect(comp_play_button.x, comp_play_button.bottom + 17, 400, 50)

        self.surface.blit(title_text, title_rect)
        pygame.draw.rect(self.surface, (210, 224, 191), comp_play_button)
        self.surface.blit(comp_play_text, comp_play_text_rect)
        pygame.draw.rect(self.surface, (210, 224, 191), single_play_button)
        self.surface.blit(single_play_text, single_play_text_rect)

        if comp_play_button.collidepoint(mx, my) and is_pressed:
            self.against_computer = True
            self.is_active = True
            self.is_first_game = False
            self.cells = self.init_grid()
            self.surface.fill((230, 230, 255))
        elif single_play_button.collidepoint(mx, my) and is_pressed:
            self.against_computer = False
            self.is_active = True
            self.is_first_game = False
            self.cells = self.init_grid()
            self.surface.fill((230, 230, 255))


class ComputerPlayer(object):
    def __init__(self):
        self.is_first_turn = True

    async def next_turn(self, current_grid, opponent_last_move) -> tuple:
        if self.is_first_turn:
            self.is_first_turn = False
            return self.randomize_turn(current_grid)
        else:
            possible_win = self.check_possible_win(current_grid)
            if possible_win is not None:
                return possible_win
            else:
                return self.check_if_about_to_lose(current_grid, opponent_last_move)

    def randomize_turn(self, current_grid) -> tuple:
        new_grid = current_grid
        turn = random.randint(0, 8)
        while new_grid[turn][1] is not None:
            turn = random.randint(0, 8)
        new_grid[turn][1] = False
        return new_grid, turn

    def check_possible_win(self, current_grid) -> tuple:
        new_grid = current_grid
        for current_rect in current_grid:
            if not current_rect[1]:
                (row_collection, column_collection, current_move) = Game.get_row_column_collection(new_grid,
                                                                                                   current_rect)
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
        (row_collection, column_collection, current_move) = Game.get_row_column_collection(new_grid, opponent_last_move)
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

    def get_diagnol_collection(self, grid, symbol) -> tuple:
        first_diagonal_collection = 0
        second_diagonal_collection = 0

        for cell in grid[0::4]:
            if cell[1] == symbol:
                first_diagonal_collection += 1

        for cell in grid[2:7:2]:
            if cell[1] == symbol:
                second_diagonal_collection += 1

        return first_diagonal_collection, second_diagonal_collection
