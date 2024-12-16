import queue
import sys
import os
import threading
from typing import List
from hex import HexagonTile

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pygame
from hex_manager import HexManager
from constants import *
from Player_widget import PlayerWidget
from GameParameters import GameParameters
from Game_Logic.AI.Agent import Agent
from Game_Logic.AI.AlphaBetaAgent import AlphaBetaAgent
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
winner = None

hex_manager = HexManager(ORIGIN, RADIUS, MINIMAL_RADIUS)
controller=GameController()
ai_queue = queue.Queue()

def start_game(game_parameters: GameParameters):
    name1 = "Computer1"
    name2 = "Computer2"
    agent1 = agent2 = None
    if game_parameters.selected_mode == Gamemode.PvP:
        name1 = game_parameters.name1
        name2 = game_parameters.name2
    elif game_parameters.selected_mode == Gamemode.PvC:
        name1 = game_parameters.name1
        agent2 = AlphaBetaAgent(controller,Color.Black , 2, 1)
    elif game_parameters.selected_mode == Gamemode.CvC:
        agent1 = AlphaBetaAgent(controller,Color.White , 2, 1)
        agent2 = AlphaBetaAgent(controller,Color.Black , 2, 1)
    
    player1 = PlayerWidget(name1, (255, 0, 0) , get_player_dict(), Color.White, agent1)
    player2 = PlayerWidget(name2, (0, 0, 255) , get_player_dict(), Color.Black, agent2)

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

    ai_move = None
    ai_thread = None
    def check_victory():
        global winner
        loser = controller.get_loser()
        print("loser: ", loser)
        if loser == 2:
            winner = "white"
            print("winner: ", winner)
            display_winner(screen, f"{player1.name} (White) wins!")
            return "white"
        elif loser == 1:
            winner = "black"
            print("winner: ", winner)
            display_winner(screen, f"{player2.name} (Black) wins!")
            return "black"
            
    def endTurn():
        # End turn and set current player
        # If current player has no moves, swap back to previous player
        nonlocal current_turn, current_player
        current_turn += 1
        current_player = player2 if current_player == player1 else player1
        if not controller.hasPlay():
            current_player = player2 if current_player == player1 else player1

        check_victory()
        # loser = controller.get_loser()
        # print("loser: ", loser)
        # if loser == Color.Black:
        #     winner = "white"
        # elif loser == Color.White:
        #     winner = "black"

        # winner = controller.get_winner()
        # print("winner: ", winner)
        # if winner == Color.White:
        #     display_winner(screen, f"{player1.name} (White) wins!")
        # elif winner == Color.Black:
        #     display_winner(screen, f"{player2.name} (Black) wins!")

        
    # Display winner on screen
    def display_winner(screen, message):
        font = pygame.font.Font(None, 50)
        text = font.render(message, True, (0, 255, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2-HEIGHT/4))
        screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(3000)


    # Run in separate thread, send result back to main thread
    def get_best_move(agent: Agent):
        move = agent.getBestMove()
        ai_queue.put(move)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if winner is not None:
            pass
        elif current_player.name == "Computer1" or current_player.name == "Computer2":
            try:
                ai_move = ai_queue.get_nowait()
                print("Move received: ", ai_move)
                if ai_move:
                    if ai_move[1] is not None:
                        # Apply the ai_move using the game controller
                        controller.move_piece(ai_move[1], ai_move[2])

                        # Update the HexManager to reflect the ai_move visually
                        hex_manager.removeHexagonTile(ai_move[1][0], ai_move[1][1])
                        hex_manager.createHexagonTile(ai_move[2][0], ai_move[2][1], ai_move[0], current_player.agent.agentColor)

                        print(f"Computer moved {ai_move[0]} from {ai_move[1]} to {ai_move[2]}")
                    # There is no available ai_move and computer will add new piece 
                    else:
                        controller.add_piece(ai_move[0], ai_move[2])
                        hex_manager.createHexagonTile(ai_move[2][0], ai_move[2][1], ai_move[0], current_player.agent.agentColor)
                        current_player.insects[ai_move[0]] -= 1
                    ai_move = None
                    endTurn()
                    print("Turn ended, next player: ", current_player.name)
                    continue
            except queue.Empty:
                pass

            if ai_thread is None or not ai_thread.is_alive():
                if ai_move is None:  # Only start if no pending AI move
                    ai_thread = threading.Thread(target=get_best_move, args=(current_player.agent,))
                    ai_thread.start()
                    print("Thread started")
        else:
            # Disable clicking when AI is playing
            for event in events:
                
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if current_state == State.Nothing_selected:
                        # Check if player area 1 or 2 was clicked in the correct turn
                        # If yes, get the clicked insect
                        if current_player == player1 and pygame.Rect(0, 0, 250, HEIGHT).collidepoint(mouse_pos) or current_player == player2 and pygame.Rect(WIDTH - 250, 0, 250, HEIGHT).collidepoint(mouse_pos):
                            new_insect = current_player.handle_click(mouse_pos)
                            if new_insect is None:
                                continue
                            for tile in hex_manager.hexagons:
                                if tile.color == player1.color and tile.insect == "bee":
                                    player1_bee_played = True
                                if tile.color == player2.color and tile.insect == "bee":
                                    player2_bee_played = True
                            if new_insect != "bee" and ((current_turn == 6 and current_player == player1 and not player1_bee_played) or (current_turn == 7 and current_player == player2 and not player2_bee_played)):
                                continue
                            # print(hex_manager.outlines)
                            moveOutlines=controller.get_valid_adds(new_insect)
                            # print(moveOutlines)
                            if len(moveOutlines) >0:
                                current_state = State.New_piece_selected
                                for i in moveOutlines:
                                    hex_manager.drawOutline(i[0],i[1])

                            print(current_state)
                            continue

                        # Select existing tile from board
                        clicked_tiles: List[HexagonTile] = []
                        for tile in hex_manager.hexagons:
                            if tile.contains_point(mouse_pos):
                                clicked_tiles.append(tile)
                                print("clicked tile z: ", tile.insect,tile.z)
                        if len(clicked_tiles) > 0:
                            selected_tile = clicked_tiles[0]
                            for clicked_tile in clicked_tiles:
                                if clicked_tile.z > selected_tile.z:
                                    selected_tile = clicked_tile
                            print("selected tile: ",selected_tile.insect)

                            if selected_tile.color == current_player.color:
                                moveOutlines=controller.get_valid_moves(selected_tile.axial_coordinates)
                                print("current outlines: ", moveOutlines)
                                if len(moveOutlines) >0:
                                    selected_tile.selected = True
                                    current_state = State.Existing_piece_selected
                                    for i in moveOutlines:
                                        hex_manager.drawOutline(i[0],i[1])
                                print(current_state, selected_tile.insect)

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
                                # current_turn += 1
                                # current_player = player2 if current_player == player1 else player1
                                new_insect = None
                                
                                current_state = State.Nothing_selected
                                endTurn()
                        print(current_state)
                    elif current_state == State.Existing_piece_selected:
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
                                # current_player = player2 if current_player == player1 else player1
                                # current_turn += 1
                                current_state = State.Nothing_selected
                                endTurn()
                                break
                        if outline_clicked: continue

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

                        # If neither tile nor outline is clicked, remove selection
                        if tile_clicked == False and outline_clicked == False:
                            selected_tile.selected = False
                            selected_tile = None
                            hex_manager.removeAllOutlines()
                            current_state = State.Nothing_selected
                        print(current_state)                                


        # RENDER GAME HERE
        screen.fill((0,0,0))

        # HACK: render bg multiple times to avoid low resolution
        screen.blit(bg_image, (0,0))
        screen.blit(bg_image, (640,0))
        screen.blit(bg_image, (640*2,0))
        screen.blit(bg_image, (640*3,0))

        hex_manager.render(screen)
        player1.render(screen)
        player2.render(screen)
        if winner is  None: # needs fixing
            # Render the current player's turn
            font = pygame.font.Font(None, 50)
            text = font.render(f"{current_player.name}'s turn", True, (50, 50, 50))
            text_rect = text.get_rect(center=(WIDTH // 2, 50))
            screen.blit(text, text_rect)

        # Render the changes on the screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
start_game(GameParameters())
