import pygame
from Modules import Game

pygame.init()
WIDTH = 450
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((230, 230, 255))
clock = pygame.time.Clock()
game = Game(screen, WIDTH, HEIGHT)

while True:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game.is_active:
            if game.against_computer:
                if game.x_turn:
                    pos = pygame.mouse.get_pos()
                    game.check_cell_collision(pos)
                else:
                    pass
            else:
                pos = pygame.mouse.get_pos()
                game.check_cell_collision(pos)
        if not game.is_active and keys[pygame.K_SPACE]:
            screen.fill((230, 230, 255))
            game.__init__(screen, WIDTH, HEIGHT)
            game.is_active = True
            game.is_first_game = False

    if game.is_active:
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
