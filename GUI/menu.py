import pygame
import pygame_menu
from constants import *
from game import start_game
from GameParameters import GameParameters
import sys


pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

game_parameters = GameParameters()

def set_name1(value):
    game_parameters.name1 = value

def set_name2(value):
    game_parameters.name2 = value

def set_mode(value, mode):
    game_parameters.selected_mode = mode
    print(f"Selected Mode: {value[0]}, Mode Value: {mode}")

def set_difficulty1(value, difficulty):
    game_parameters.difficulty1 = difficulty

def set_difficulty2(value, difficulty):
    game_parameters.difficulty2 = difficulty

def get_main_menu():
    menu.mainloop(surface)

# Now you can use `selected_mode` later in your code after the user interacts with the menu.
def create_menu2():
    menu2 = pygame_menu.Menu('Welcome', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
    if game_parameters.selected_mode == Gamemode.CvC:
        menu2.add.selector('Difficulty for Computer 1:', [('Hard', 3), ('Medium', 2),('Easy', 1)], default = game_parameters.difficulty1, onchange=set_difficulty1)
        menu2.add.selector('Difficulty for Computer 2:', [('Hard', 3), ('Medium', 2),('Easy', 1)], default = game_parameters.difficulty2, onchange=set_difficulty2)
    elif game_parameters.selected_mode == Gamemode.PvC:
        menu2.add.text_input('Player 1 :', default=game_parameters.name1, onchange=set_name1)
        menu2.add.selector('Difficulty :', [('Hard', 3), ('Medium', 2),('Easy', 1)], default = game_parameters.difficulty2, onchange=set_difficulty2)
    elif game_parameters.selected_mode == Gamemode.PvP:
        menu2.add.text_input('Player 1 :', default=game_parameters.name1, onchange=set_name1)
        menu2.add.text_input('Player 2 :', default=game_parameters.name2, onchange=set_name2)

    menu2.add.button('Play', start_the_game)
    menu2.add.button('Back', get_main_menu)
    menu2.mainloop(surface)

def start_the_game():

    start_game(game_parameters)
    sys.exit()

menu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)

menu.add.selector('Mode :', [('Player vs Player', Gamemode.PvP), ('Player vs Computer', Gamemode.PvC), ('Computer vs Computer', Gamemode.CvC)], onchange=set_mode)

menu.add.button('Next', create_menu2)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)
