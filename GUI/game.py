import pygame
from hex_manager import HexManager
from constants import *

hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
hex_manager.createHexagonTile(0,0)
hex_manager.createHexagonTile(0,1)
hex_manager.drawOutline(1,1)
hex_manager.drawOutline(1,0)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

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
