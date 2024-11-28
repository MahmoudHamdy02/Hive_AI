import pygame
from constants import *
class PlayerWidget:
    def __init__(self,name: str, color: tuple,insects: int):
        self.player_name = name
        self.player_color = color
        #self.player_score = self.player.score
        self.player_insects = insects
        self.player_insect_count = 5
        self.postion = (10, 10)
        
    def render(self, screen):
        """
        Render the player widget on the screen.

        :param screen: The pygame screen object.
        """
        # Determine the position and size based on player color
        if self.player_color == (255, 0, 0):  # Red color
            rect_width = 250
            rect_x = 0  # Align to the left side of the screen
        else:
            rect_width = 250
            rect_x = WIDTH-250

        rect_y = 0
        rect_height = HEIGHT

        # Draw the background for the widget
        pygame.draw.rect(screen, (50, 50, 50), (rect_x, rect_y, rect_width, rect_height))  # A gray background
        pygame.draw.rect(screen, self.player_color, (rect_x, rect_y, rect_width, rect_height), 3)  # Border with player color

        # Render the player's name
        name_text = pygame.font.SysFont("Arial", 20).render(f"Name: {self.player_name}", True, (255, 255, 255))
        screen.blit(name_text, (rect_x + 10, rect_y + 10))

    
    
            