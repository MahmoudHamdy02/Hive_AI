import pygame
import pygame_menu
pygame.init()
surface = pygame.display.set_mode((600, 400))
def set_difficulty(value, difficulty):
    # Do the job here !
    pass
global selected_mode  # Declare a global variable
selected_mode = 1  # Initialize it

def set_mode(value, mode):
    global selected_mode
    selected_mode = mode
    print(f"Selected Mode: {value[0]}, Mode Value: {mode}")
def set_difficulty1(value, difficulty):
    # Do the job here !
    pass
def set_difficulty2(value, difficulty):
    # Do the job here !
    pass
def get_main_menu():
    menu.mainloop(surface)
# Now you can use `selected_mode` later in your code after the user interacts with the menu.
def create_menu2():
    menu2 = pygame_menu.Menu('Welcome', 600, 400,
                       theme=pygame_menu.themes.THEME_BLUE)
    if selected_mode == 1:
        menu2.add.selector('Difficulty for Computer 1:', [('Hard', 1), ('Medium', 2),('Easy', 3)], onchange=set_difficulty1)
        menu2.add.selector('Difficulty for Computer 2:', [('Hard', 1), ('Medium', 2),('Easy', 3)], onchange=set_difficulty2)
    elif selected_mode == 2:
        menu2.add.text_input('Player 1 :', default='John Doe')
        menu2.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2),('Easy', 3)], onchange=set_difficulty)
    elif selected_mode == 3:
        menu2.add.text_input('Player 1 :', default='John Doe')
        menu2.add.text_input('Player 2 :', default='John Doe')

    menu2.add.button('Play', start_the_game)
    menu2.add.button('Back', get_main_menu)
    menu2.mainloop(surface)
def start_the_game():
    # Do the job here !
    pass
# menu.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2),('Easy', 3)], onchange=set_difficulty)

menu = pygame_menu.Menu('Welcome', 600, 400,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.selection=menu.add.selector('Mode :', [('Computer vs Computer', 1), ('Human vs Computer', 2),('Human vs Human', 3)], onchange=set_mode)

menu.add.button('next', create_menu2)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)