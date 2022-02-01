import pygame
from modules import Game
import asyncio


async def main():
    pygame.init()
    WIDTH = 450
    HEIGHT = 450
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((230, 230, 255))
    game = Game(screen, WIDTH, HEIGHT)
    await game.start()


if __name__ == "__main__":
    asyncio.run(main())
