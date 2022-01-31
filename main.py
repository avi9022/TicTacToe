import pygame
from Modules import Game

pygame.init()
WIDTH = 450
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((230, 230, 255))
clock = pygame.time.Clock()
click = False
game = Game(screen, WIDTH, HEIGHT)

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.is_active:
                if game.against_computer:
                    if game.x_turn:
                        pos = pygame.mouse.get_pos()
                        game.check_cell_collision(pos)
                    else:
                        pass
                else:
                    pos = pygame.mouse.get_pos()
                    game.check_cell_collision(pos)
            click = True
        if keys[pygame.K_SPACE] and not game.is_first_game and not game.is_active:
            game.is_active = True
            screen.fill((230, 230, 255))
            game.cells = game.init_grid()
            game.x_turn = True

    if game.is_first_game:
        game.main_menu(click)
    elif game.is_active:
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
