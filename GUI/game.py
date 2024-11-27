import pygame
from hex import HexagonTile
from hex_manager import HexManager
from constants import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
hex_manager.createHexagonTile(0,0)
hex_manager.createHexagonTile(0,1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER GAME HERE
    screen.fill((0,0,0))
    
    hex_manager.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
