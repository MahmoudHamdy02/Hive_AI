import pygame
from hex_manager import HexManager
from constants import *
from Player_widget import PlayerWidget
player1 = PlayerWidget("Player 1",(255, 0, 0) , 4)
player2 = PlayerWidget("salma waleed",(0, 0, 255) , 4)
hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
hex_manager.createHexagonTile(0,0)
hex_manager.createHexagonTile(-1,0)
hex_manager.createHexagonTile(0,-1)
hex_manager.createHexagonTile(-1,-1)
hex_manager.createHexagonTile(0,1)
hex_manager.createHexagonTile(2,2)
hex_manager.removeHexagonTile(2,2)
hex_manager.drawOutline(1,1)
hex_manager.drawOutline(1,0)
hex_manager.drawOutline(2,2)
hex_manager.removeOutline(2,2)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

bg_image = pygame.image.load("GUI/images/bg.jpg")
bg_image = pygame.transform.scale(bg_image, (640, 1280))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER GAME HERE
    screen.fill((0,0,0))

    # HACK: render bg twice side by side to avoid low resolution
    screen.blit(bg_image, (0,0))
    screen.blit(bg_image, (640,0))
    
    hex_manager.render(screen)
    player1.render(screen)
    player2.render(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
