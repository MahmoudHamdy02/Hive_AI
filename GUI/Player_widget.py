from typing import Tuple
import pygame
from constants import *
import insects_widget


class PlayerWidget:

    def __init__(self,name: str, color: Tuple[float, float, float],insects: dict):
        
        self.name = name
        self.color = color
        #self.player_score = self.player.score
        self.insects = insects
        self.insect_count = 5
        self.postion = (10, 10)
        self.insectsBoxes={}
        if self.color == (255, 0, 0):  # Red color

            self.flag = Color.Black
        else:

            self.flag = Color.White
        
    def render(self, screen) -> None:
        """
        Render the player widget on the screen.

        :param screen: The pygame screen object.
        """
        self.insectsBoxes={}
        # Determine the position and size based on player color
        if self.color == (255, 0, 0):  # Red color
            rect_width = 250
            rect_x = 0  # Align to the left side of the screen
        else:
            rect_width = 250
            rect_x = WIDTH-250

        rect_y = 0
        rect_height = HEIGHT

        # Draw the background for the widget
        pygame.draw.rect(screen, (50, 50, 50), (rect_x, rect_y, rect_width, rect_height))  # A gray background
        pygame.draw.rect(screen, self.color, (rect_x, rect_y, rect_width, rect_height), 3)  # Border with player color

        # Render the player's name
        name_text = pygame.font.SysFont("Arial", 20).render(f"Name: {self.name}", True, (255, 255, 255))
        screen.blit(name_text, (rect_x + 10, rect_y + 10))
        i=1
        for insect_name, count in self.insects.items():

            box_x = rect_x + 10
            box_y = rect_y + 40 * i + (i - 1) * INSECT_BOX_Y
            insect_box = pygame.Rect(box_x, box_y, INSECT_BOX_X, INSECT_BOX_Y)

            insect = insects_widget.InsectWidget(insect_name,self.flag,count,(box_x,box_y))
            insect.render(screen)
            # count_text = pygame.font.SysFont("Arial", 24).render(f"x{1}", True, (0, 0, 0))  
            # screen.blit(count_text, (rect_x+10 + INSECT_BOX_X-30, INSECT_BOX_Y+5))

            # Store the box in the dictionary
            self.insectsBoxes[insect_name] = insect_box
            i+=1

    def handle_click(self, position) -> str | None:
        """
        Check if the click is within any insect box.
        
        :param position: (x, y) position of the mouse click.
        :return: The name of the clicked insect, or None if no box was clicked.
        """
        for insect_name, rect in self.insectsBoxes.items():
            if rect.collidepoint(position):
                print(insect_name)
                return insect_name
        return None
       


    
    
            