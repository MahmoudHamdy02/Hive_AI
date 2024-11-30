import pygame
from hex_manager import HexManager
from constants import *
from Player_widget import PlayerWidget
player_dict = {
    "ant": 2,
    "bee": 2,
    "spider": 3,
    "hopper": 7, 
    "beetle": 1
}
player1 = PlayerWidget("Player 1",(255, 0, 0) , player_dict)
player2 = PlayerWidget("salma waleed",(0, 0, 255) , player_dict)
hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
#hex_manager.createHexagonTile(0,0)
#hex_manager.createHexagonTile(-1,0)
#hex_manager.createHexagonTile(0,-1)
hex_manager.createHexagonTile(-1,-1)
hex_manager.createHexagonTile(0,1)

#hex_manager.createHexagonTile(2,2)
#hex_manager.removeHexagonTile(2,2)
#hex_manager.drawOutline(1,1)
#hex_manager.drawOutline(1,0)
hex_manager.createHexagonTile(2,2)

vAntMoves=[(0,0),(-1,0),(2,0)]
for i in vAntMoves:
    hex_manager.drawOutline(i[0],i[1])
def start_game():
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    bg_image = pygame.image.load("GUI/images/bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (640, 1280))

    selected_insect = None  # To track the selected insect
    selected_player = None  # To track the selected player

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check if a player widget was clicked
                if pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos):  # Player 1 area
                    selected_player = player1
                elif pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):  # Player 2 area
                    selected_player = player2

                # Check if clicking an insect box
                if selected_player and not selected_insect:
                    selected_insect = selected_player.handle_click(mouse_pos)
                 # Check if clicking a board position to move the insect
                elif selected_insect:
                    for tile in hex_manager.outlines:  # Assuming `vAntMoves` contains hexagonal tiles
                        if tile.contains_point(mouse_pos):
                        # Move the insect to this valid tile
                            position=tile.axial_coordinates
                            hex_manager.removeOutline(position[0],position[1])
                            hex_manager.createHexagonTile(position[0], position[1], selected_insect, selected_player.player_color)  # Add insect to tile
                            selected_player.player_insects[selected_insect] -= 1  # Decrement insect count
                            selected_insect = None  # Reset selected insect
                            selected_player = None  # Reset selected player
                            break


        # RENDER GAME HERE
        screen.fill((0,0,0))

        # HACK: render bg twice side by side to avoid low resolution
        screen.blit(bg_image, (0,0))
        screen.blit(bg_image, (640,0))

        hex_manager.render(screen)
        player1.render(screen)
        player2.render(screen)

        # Render the changes on the screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
start_game()