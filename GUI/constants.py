import math


WIDTH = 1280
HEIGHT = 720
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
ORIGIN = (CENTER_X, CENTER_Y)
RADIUS = 50 # Outer circle: from center to vertex
MINIMAL_RADIUS = RADIUS * math.cos(math.radians(30)) # Inner circle: from center to edge
