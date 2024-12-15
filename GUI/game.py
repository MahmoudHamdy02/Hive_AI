import sys
import os

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



import pygame
from hex_manager import HexManager
from constants import *
from Player_widget import PlayerWidget
from GameParameters import GameParameters

from Game_Logic.Game.GameController import GameController

# Get a copy of the dict to avoid pass-by-sharing
def get_player_dict():
    return {
        "ant": 3,
        "bee": 1,
        "spider": 2,
        "grasshopper": 3, 
        "beetle": 2
    }

hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
#hex_manager.createHexagonTile(0,0)
#hex_manager.createHexagonTile(-1,0)
#hex_manager.createHexagonTile(0,-1)
#hex_manager.createHexagonTile(-1,-1)
#hex_manager.createHexagonTile(0,1)

#hex_manager.createHexagonTile(2,2)
#hex_manager.removeHexagonTile(2,2)
#hex_manager.drawOutline(1,1)
#hex_manager.drawOutline(2,2)
#hex_manager.drawOutline(2,1)
#hex_manager.drawOutline(0,2)

controller=GameController()
vAntMoves=[(0,0),(-1,0),(2,0)]
#for i in vAntMoves:
    #hex_manager.drawOutline(i[0],i[1])

# def endTurn(current_turn, current_player):
#         # check no available moves

#         current_turn += 1
#         current_player = player2 if current_player == player1 else player1

def start_game(game_parameters: GameParameters):
    name1 = name2 = "Computer"
    if game_parameters.selected_mode == Gamemode.PvP or game_parameters.selected_mode == Gamemode.PvC:
        name1 = game_parameters.name1
    if game_parameters.selected_mode == Gamemode.PvP:
        name2 = game_parameters.name2
    
    player1 = PlayerWidget(name1, (255, 0, 0) , get_player_dict(), Color.Black)
    player2 = PlayerWidget(name2, (0, 0, 255) , get_player_dict(), Color.White)  
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    bg_image = pygame.image.load(f"{GUI_PATH}/images/bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (640, 1280))

    current_state: State = State.Nothing_selected
    selected_tile = None
    current_turn = 0

    new_insect = None  # To track the selected insect
    current_player = player1
    player1_bee_played = False
    player2_bee_played = False

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # This currently force the turn order
                # TODO: A turn must be skipped if there are no available moves
                # Create end_turn() function to handle logic

                if current_state == State.Nothing_selected:
                    # Check if player area 1 or 2 was clicked in the correct turn
                    # If yes, get the clicked insect
                    if current_player == player1 and pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos) or current_player == player2 and pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):
                        new_insect = current_player.handle_click(mouse_pos)
                        if new_insect is None:
                            continue
                        for tile in hex_manager.hexagons:
                            if tile.color == Color.Black and tile.insect == "bee":
                                player1_bee_played = True
                            if tile.color == Color.White and tile.insect == "bee":
                                player2_bee_played = True
                        if new_insect != "bee" and ((current_turn == 6 and current_player == player1 and not player1_bee_played) or (current_turn == 7 and current_player == player2 and not player2_bee_played)):
                            continue
                        print(hex_manager.outlines)
                        moveOutlines=controller.get_valid_adds(new_insect)
                        print(moveOutlines)
                        if len(moveOutlines) >0:
                            current_state = State.New_piece_selected
                            for i in moveOutlines:
                                hex_manager.drawOutline(i[0],i[1])

                        print(current_state)
                        continue

                    # Select existing tile from board
                    for tile in hex_manager.hexagons:
                        if tile.contains_point(mouse_pos) and tile.color == current_player.color:
                            selected_tile = tile
                            moveOutlines=controller.get_valid_moves(tile.axial_coordinates)
                            print("current outlines: ", moveOutlines)
                            if len(moveOutlines) >0:
                                tile.selected = True
                                current_state = State.Existing_piece_selected
                                for i in moveOutlines:
                                    hex_manager.drawOutline(i[0],i[1])
                            print(current_state, selected_tile.insect)
                            break

                elif current_state == State.New_piece_selected:
                    # If another new piece is clicked, select it instead
                    # Skip if another piece is selected in mandatory bee's turn
                    if current_player == player1 and pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos) or current_player == player2 and pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):
                        new_insect = current_player.handle_click(mouse_pos)
                        for tile in hex_manager.hexagons:
                            if tile.color == Color.Black and tile.insect == "bee":
                                player1_bee_played = True
                            if tile.color == Color.White and tile.insect == "bee":
                                player2_bee_played = True
                        if new_insect != "bee" and ((current_turn == 6 and current_player == player1 and not player1_bee_played) or (current_turn == 7 and current_player == player2 and not player2_bee_played)):
                            new_insect = "bee"
                        print(current_state)
                        continue

                    for tile in hex_manager.hexagons:
                        if tile.contains_point(mouse_pos):
                            hex_manager.removeAllOutlines()
                            current_state = State.Nothing_selected
                            continue

                    # Place new piece
                    for outline in hex_manager.outlines:
                        if outline.contains_point(mouse_pos):
                            q, r = outline.axial_coordinates
                            hex_manager.removeAllOutlines()
                            
                            hex_manager.createHexagonTile(q, r, new_insect, current_player.color)
                            controller.add_piece(new_insect, (q, r))
                            current_player.insects[new_insect] -= 1  # Decrement insect count
                            #if not controller.hasPlay():
                            current_turn += 1
                            current_player = player2 if current_player == player1 else player1
                            # endTurn()
                            new_insect = None
                            current_state = State.Nothing_selected
                    print(current_state)
                elif current_state == State.Existing_piece_selected:
                    # If another tile is clicked, select it instead
                    tile_clicked = False
                    for tile in hex_manager.hexagons:
                        if tile.contains_point(mouse_pos) and tile.color == current_player.color:
                            tile_clicked = True
                            selected_tile.selected = False
                            selected_tile = tile
                            hex_manager.removeAllOutlines()
                            moveOutlines=controller.get_valid_moves(tile.axial_coordinates)
                            if len(moveOutlines) >0:
                                tile.selected = True
                                for i in moveOutlines:
                                    hex_manager.drawOutline(i[0],i[1])
                            current_state = State.Existing_piece_selected
                            print(current_state, selected_tile.insect)
                            break

                    # Move selected tile to clicked outline
                    outline_clicked = False
                    for outline in hex_manager.outlines:
                        if outline.contains_point(mouse_pos):
                            outline_clicked = True
                            q, r = outline.axial_coordinates
                            controller.move_piece(selected_tile.axial_coordinates, (q, r))
                            hex_manager.removeAllOutlines()
                            tile_q, tile_r = selected_tile.axial_coordinates
                            hex_manager.removeHexagonTile(tile_q, tile_r)
                            hex_manager.createHexagonTile(q, r, selected_tile.insect, current_player.color)
                            selected_tile = None
                            current_player = player2 if current_player == player1 else player1
                            current_turn += 1
                            # endTurn()
                            current_state = State.Nothing_selected

                    # If neither tile nor outline is clicked, remove selection
                    if tile_clicked == False and outline_clicked == False:
                        selected_tile.selected = False
                        selected_tile = None
                        hex_manager.removeAllOutlines()
                        current_state = State.Nothing_selected
                    print(current_state)                                


        # RENDER GAME HERE
        screen.fill((0,0,0))

        # HACK: render bg twice side by side to avoid low resolution
        screen.blit(bg_image, (0,0))
        screen.blit(bg_image, (640,0))
        screen.blit(bg_image, (640*2,0))
        screen.blit(bg_image, (640*3,0))

        hex_manager.render(screen)
        player1.render(screen)
        player2.render(screen)

        # Render the changes on the screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
start_game(GameParameters())