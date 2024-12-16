import math
from enum import Enum
import os

import pygame


GUI_PATH = os.path.dirname(__file__) # Path to inside the GUI folder, doesn't include trailing "/"
pygame.display.init()
WIDTH=pygame.display.Info().current_w-300
HEIGHT=pygame.display.Info().current_h-300
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
RADIUS = 50 # Outer circle: from center to vertex
MINIMAL_RADIUS = RADIUS * math.cos(math.radians(30)) # Inner circle: from center to edge
ORIGIN = (CENTER_X, CENTER_Y - RADIUS) # Subtract radius to align origin to center of hexagon
INSECT_BOX_X=230
INSECT_BOX_Y=100

Color = Enum("Color", [("Black", 0), ("White", 1)])
State = Enum("State", [("Nothing_selected", 0),("New_piece_selected", 1),("Existing_piece_selected", 2)])
Gamemode = Enum("Gamemode", [("CvC", 0),("PvC", 1),("PvP", 2)])