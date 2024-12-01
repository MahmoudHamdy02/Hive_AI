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

player1 = PlayerWidget("Player 1",(255, 0, 0) , get_player_dict(), Color.Black)
player2 = PlayerWidget("salma waleed",(0, 0, 255) , get_player_dict(), Color.White)
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

    current_state: State = State.Nothing_selected
    selected_tile = None

    new_insect = None  # To track the selected insect
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

                # This currently force the turn order
                # TODO: A turn must be skipped if there are no available moves
                # Create end_turn() function to handle logic

                # TODO: Create a visual effect to indicate a piece is selected

                if current_state == State.Nothing_selected:
                    # Check if player area 1 or 2 was clicked in the correct turn
                    # If yes, get the clicked insect
                    if current_player == player1 and pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos) or current_player == player2 and pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):
                        new_insect = current_player.handle_click(mouse_pos)
                        current_state = State.New_piece_selected
                        print(current_state)
                        continue

                    # Select existing tile from board
                    for tile in hex_manager.hexagons:
                        if tile.contains_point(mouse_pos) and tile.color == current_player.color:
                            selected_tile = tile
                            current_state = State.Existing_piece_selected
                            print(current_state, selected_tile.insect)
                            break

                elif current_state == State.New_piece_selected:
                    # If another new piece is clicked, select it instead
                    if current_player == player1 and pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos) or current_player == player2 and pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):
                        new_insect = current_player.handle_click(mouse_pos)
                        print(current_state)
                        continue

                    # Place new piece
                    for outline in hex_manager.outlines:
                        if outline.contains_point(mouse_pos):
                            q, r = outline.axial_coordinates
                            hex_manager.removeOutline(q, r)
                            hex_manager.createHexagonTile(q, r, new_insect, current_player.color)
                            current_player.insects[new_insect] -= 1  # Decrement insect count
                            current_player = player2 if current_player == player1 else player1
                            new_insect = None
                            current_state = State.Nothing_selected
                    print(current_state)
                elif current_state == State.Existing_piece_selected:
                    # If another tile is clicked, select it instead
                    tile_clicked = False
                    for tile in hex_manager.hexagons:
                        if tile.contains_point(mouse_pos) and tile.color == current_player.color:
                            tile_clicked = True
                            selected_tile = tile
                            current_state = State.Existing_piece_selected
                            print(current_state, selected_tile.insect)
                            break

                    # Move selected tile to clicked outline
                    outline_clicked = False
                    for outline in hex_manager.outlines:
                        if outline.contains_point(mouse_pos):
                            outline_clicked = True
                            q, r = outline.axial_coordinates
                            hex_manager.removeOutline(q, r)
                            tile_q, tile_r = selected_tile.axial_coordinates
                            hex_manager.removeHexagonTile(tile_q, tile_r)
                            hex_manager.createHexagonTile(q, r, selected_tile.insect, current_player.color)
                            selected_tile = None
                            current_player = player2 if current_player == player1 else player1
                            current_state = State.Nothing_selected

                    # If neither tile nor outline is clicked, remove selection
                    if tile_clicked == False and outline_clicked == False:
                        selected_tile = None
                        current_state = State.Nothing_selected
                    print(current_state)                                


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