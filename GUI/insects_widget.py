import pygame
from constants import *

class InsectWidget:
    def __init__(self, name: str, color: int, count: int, position: tuple):
        self.name = name
        self.color = color
        self.count = count
        self.position = position
        self.image = None  # Default image initialization

        if self.color == Color.Black and self.count:
            self.image = pygame.image.load(IMAGES_PATH_2+f"/b_insects/b-{self.name}.png")

        elif self.color == Color.White and self.count:
            self.image = pygame.image.load(IMAGES_PATH_2+f"/w_insects/w-{self.name}.png")

        if self.image:  # Ensure image is not None
            self.image = pygame.transform.scale(self.image, (110, 110))

    # Add function to re-render the count of insects
    def render(self, screen) -> None:
        
        # Draw the background rectangle
        pygame.draw.rect(screen, (255, 255, 255), (self.position[0], self.position[1], INSECT_BOX_X, INSECT_BOX_Y))

        # Draw the image if available
        if self.image:
            # Center the image within the rectangle
            img_x = self.position[0] + (INSECT_BOX_X - self.image.get_width()) // 2
            img_y = self.position[1] + (INSECT_BOX_Y - self.image.get_height()) // 2
            text_x = self.position[0] + (INSECT_BOX_X-30 )
            text_y = self.position[1] + (INSECT_BOX_Y-30)
            screen.blit(self.image, (img_x-55, img_y))
            count_text = pygame.font.SysFont("Arial", 24).render(f"x{self.count}", True, (0, 0, 0))  
            screen.blit(count_text, (text_x , text_y))
            # it is displayed in the first box only
