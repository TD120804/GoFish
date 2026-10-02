import pygame
from game import GoFishGame
from ui import GoFishUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((1100, 720))
    pygame.display.set_caption("Go Fish — Rule-Based Expert System")
    clock = pygame.time.Clock()

    game = GoFishGame()
    ui = GoFishUI(screen, game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                ui.handle_event(event)

        ui.update()
        ui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
