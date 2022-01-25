import pygame


class Game:
    def __init__(self):
        self.x_img = pygame.transform.scale(pygame.image.load('graphics/Xs.png').convert_alpha(), (100, 100))
        self.o_img = pygame.transform.scale(pygame.image.load('graphics/Os.png').convert_alpha(), (100, 100))
        pygame.transform.scale(self.o_img, (50, 50))
        self.X_turn = True
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

    def draw_symbol(self):
        for rect in self.cells:
            if rect[1] is not None:
                if rect[1]:
                    screen.blit(self.x_img, rect[0])
                else:
                    screen.blit(self.o_img, rect[0])

    def check_cell_collision(self, mouse_pos):
        for rect in self.cells:
            if rect[0].collidepoint(mouse_pos) and rect[1] is None:
                rect[1] = self.X_turn
                self.X_turn = not self.X_turn

    def update(self):
        self.draw_table()
        self.draw_symbol()

class Player:
    def __init__(self, x):
        self.is_first = x


pygame.init()
cell_size = 130
cell_number = 3
WIDTH = cell_size * cell_number + 30
HEIGHT = cell_size * cell_number + 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((230, 230, 255))
game = Game()
is_active = True

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and is_active:
            pos = pygame.mouse.get_pos()
            game.check_cell_collision(pos)

    if is_active:
        game.update()
    pygame.display.update()
