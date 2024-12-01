import pygame
from hex_manager import HexManager
from constants import *
from Player_widget import PlayerWidget

# Get a copy of the dict to avoid pass-by-sharing
def get_player_dict():
    return {
        "ant": 2,
        "bee": 2,
        "spider": 3,
        "hopper": 7, 
        "beetle": 1
    }

player1 = PlayerWidget("Player 1",(255, 0, 0) , get_player_dict())
player2 = PlayerWidget("salma waleed",(0, 0, 255) , get_player_dict())
hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
#hex_manager.createHexagonTile(0,0)
#hex_manager.createHexagonTile(-1,0)
#hex_manager.createHexagonTile(0,-1)
hex_manager.createHexagonTile(-1,-1)
hex_manager.createHexagonTile(0,1)

#hex_manager.createHexagonTile(2,2)
#hex_manager.removeHexagonTile(2,2)
#hex_manager.drawOutline(1,1)
hex_manager.drawOutline(2,2)
hex_manager.drawOutline(2,1)
hex_manager.drawOutline(0,2)


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
    current_player = player1
    board_flag = False
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # TODO: Place first piece automatically at (0, 0)

                # TODO: Detect clicking the placed board pieces

                # This currently force the turn order
                # TODO: A turn must be skipped if there are no available moves

                # Check if player area 1 or 2 was clicked in the correct turn
                # If yes, get the clicked insect
                if current_player == player1 and pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos) or current_player == player2 and pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):
                    selected_insect = current_player.handle_click(mouse_pos)
                    board_flag = False
                    continue

                # Check if clicking a board position to move the insect
                if selected_insect:
                    for outline in hex_manager.outlines:  # Assuming `vAntMoves` contains hexagonal tiles
                        if outline.contains_point(mouse_pos):
                            # Move the insect to this valid tile
                            q, r = outline.axial_coordinates
                            filled_tile = hex_manager.getTile(q, r)
                            if  filled_tile:
                                hex_manager.removeOutline(q, r)
                                filled_tile.insect2 = selected_insect
                                filled_tile.color2 = current_player.flag
                                selected_insect = None  # Reset selected insect
                                current_player = player2 if current_player == player1 else player1  # Reset selected player
                                break

                            else:
                                hex_manager.removeOutline(q, r)
                                hex_manager.createHexagonTile(q, r, selected_insect, current_player.flag)  # Add insect to tile
                                if not board_flag:
                                    current_player.insects[selected_insect] -= 1  # Decrement insect count
                                selected_insect = None  # Reset selected insect
                                current_player = player2 if current_player == player1 else player1  # Reset selected player
                                break

                # detect if the board was clicked
                else:
                    for tile in hex_manager.hexagons:
                        if tile.contains_point(mouse_pos):
                            if tile.insect and tile.color == current_player.flag:
                                selected_insect = tile.insect
                                tile.insect = None
                                tile.color = None
                                board_flag = True

                    if selected_insect:
                        print("current player "+current_player.name)
                        print("from the board  "+selected_insect)
 

                                


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