"""
Target Shooting (Lab Starter)

Run with:  python3 main.py

Click on targets to hit them.
When the round is over, click anywhere to start a new round.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Target Shooting")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    engine = GameEngine()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if engine.is_over():
                    engine.reset()          # click to restart after the round ends
                else:
                    engine.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                engine.reset()

        engine.update()

        screen.fill((26, 27, 34))   # clear the previous frame
        engine.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()