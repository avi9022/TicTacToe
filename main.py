import pygame


class Game:
    def __init__(self):
        self.x_img = pygame.transform.scale(pygame.image.load('graphics/Xs.png').convert_alpha(), (100, 100))
        self.o_img = pygame.transform.scale(pygame.image.load('graphics/Os.png').convert_alpha(), (100, 100))
        pygame.transform.scale(self.o_img, (50, 50))
        self.X_turn = True
        self.filled_cells = 0
        self.is_first_game = True
        # a 2D list that holds all game cells and their content(None = empty, True = X, False = O)
        self.cells = []
        for column in range(0, 3):
            for row in range(0, 3):
                cell_rect = pygame.Rect(cell_size * row + 30, cell_size * column + 30, cell_size, cell_size)
                self.cells.append([cell_rect, None])

    def draw_table(self):
        pygame.draw.line(screen, 'Black', ((WIDTH / 3), 30), ((WIDTH / 3), HEIGHT - 30), 10)
        pygame.draw.line(screen, 'Black', ((WIDTH / 3) * 2, 30), ((WIDTH / 3) * 2, HEIGHT - 30), 10)
        pygame.draw.line(screen, 'Black', (30, (HEIGHT / 3)), (WIDTH - 30, (HEIGHT / 3)), 10)
        pygame.draw.line(screen, 'Black', (30, (HEIGHT / 3) * 2), (WIDTH - 30, (HEIGHT / 3) * 2), 10)

    def draw_symbol(self, symbol):
        if symbol[1]:
            screen.blit(self.x_img, symbol[0])
        else:
            screen.blit(self.o_img, symbol[0])

    def check_cell_collision(self, mouse_pos):
        for rect in self.cells:
            if rect[0].collidepoint(mouse_pos) and rect[1] is None:
                rect[1] = self.X_turn
                self.X_turn = not self.X_turn
                self.filled_cells += 1
                self.draw_symbol(rect)
                self.check_winner(rect)
                break

    def check_winner(self, current_move):
        global is_active
        global winner
        # 2 variables that hold how many of the same symbol we  have in a given row or column
        row_collection = 0
        column_collection = 0
        for rect in self.cells:
            if rect[1] is not None and rect[1] == current_move[1]:
                if rect[0].y == current_move[0].y:
                    row_collection += 1
                if rect[0].x == current_move[0].x:
                    column_collection += 1
        if row_collection == 3 or column_collection == 3:
            is_active = False
            winner = current_move[1]
        if self.cells[0][1] is not None and self.cells[0][1] == self.cells[4][1] and self.cells[0][1] == self.cells[8][
            1]:
            is_active = False
            winner = self.cells[0][1]
        elif self.cells[2][1] is not None and self.cells[2][1] == self.cells[4][1] and self.cells[2][1] == \
                self.cells[6][1]:
            is_active = False
            winner = self.cells[2][1]

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


pygame.init()
game_font = pygame.font.Font('graphics/Pixeltype.ttf', 50)
cell_size = 130
cell_number = 3
WIDTH = cell_size * cell_number + 30
HEIGHT = cell_size * cell_number + 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((230, 230, 255))
game = Game()
winner = None
is_active = False

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and is_active:
            pos = pygame.mouse.get_pos()
            game.check_cell_collision(pos)
        if not is_active and keys[pygame.K_SPACE]:
            screen.fill((230, 230, 255))
            is_active = True
            game.__init__()

    if is_active:
        game.update()

    else:
        screen.fill((230, 230, 255))
        game.game_over(winner)
    pygame.display.update()
