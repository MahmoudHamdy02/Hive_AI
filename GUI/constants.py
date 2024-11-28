import math


WIDTH = 1280
HEIGHT = 720
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
RADIUS = 50 # Outer circle: from center to vertex
MINIMAL_RADIUS = RADIUS * math.cos(math.radians(30)) # Inner circle: from center to edge
ORIGIN = (CENTER_X, CENTER_Y - RADIUS) # Subtract radius to align origin to center of hexagon

INSECT_BOX_X=230
INSECT_BOX_Y=100
