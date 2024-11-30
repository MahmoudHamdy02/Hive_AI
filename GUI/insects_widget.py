import pygame
from constants import *

class InsectWidget:
    def __init__(self, name: str, color: int, count: int, position: tuple):
        self.insectName = name
        self.insectColor = color  # 0: white, 1: black
        self.insectCount = count
        self.insectPosition = position
        self.image = None  # Default image initialization

        if self.insectColor == 1 and self.insectCount:
            if self.insectName == "ant":
                self.image = pygame.image.load(IMAGES_PATH_2+"/b_insects/b-ant.png")
            elif self.insectName == "bee":
                self.image = pygame.image.load(IMAGES_PATH_2+"/b_insects/b-bee.png")
            elif self.insectName == "beetle":
                self.image = pygame.image.load(IMAGES_PATH_2+"/b_insects/b-beetle.png")
            elif self.insectName == "hopper":
                self.image = pygame.image.load(IMAGES_PATH_2+"/b_insects/b-hopper.png")
            elif self.insectName == "spider":
                self.image = pygame.image.load(IMAGES_PATH_2+"/b_insects/b-spider.png")

        elif self.insectColor == 0 and self.insectCount:
            if self.insectName == "ant":
                self.image = pygame.image.load(IMAGES_PATH_2+"/w_insects/w-ant.png")
            elif self.insectName == "bee":
                self.image = pygame.image.load(IMAGES_PATH_2+"/w_insects/w-bee.png")
            elif self.insectName == "beetle":
                self.image = pygame.image.load(IMAGES_PATH_2+"/w_insects/w-beetle.png")
            elif self.insectName == "hopper":
                self.image = pygame.image.load(IMAGES_PATH_2+"/w_insects/w-hopper.png")
            elif self.insectName == "spider":
                self.image = pygame.image.load(IMAGES_PATH_2+"/w_insects/w-spider.png")

        if self.image:  # Ensure image is not None
            self.image = pygame.transform.scale(self.image, (110, 110))

    # Add function to re-render the count of insects
    def render(self, screen) -> None:
        
        # Draw the background rectangle
        pygame.draw.rect(screen, (255, 255, 255), (self.insectPosition[0], self.insectPosition[1], INSECT_BOX_X, INSECT_BOX_Y))
        # Draw the image if available
        
        if self.image:
            # Center the image within the rectangle
            img_x = self.insectPosition[0] + (INSECT_BOX_X - self.image.get_width()) // 2
            img_y = self.insectPosition[1] + (INSECT_BOX_Y - self.image.get_height()) // 2
            text_x = self.insectPosition[0] + (INSECT_BOX_X-30 )
            text_y = self.insectPosition[1] + (INSECT_BOX_Y-30)
            screen.blit(self.image, (img_x-55, img_y))
            count_text = pygame.font.SysFont("Arial", 24).render(f"x{self.insectCount}", True, (0, 0, 0))  
            screen.blit(count_text, (text_x , text_y))
            # it is displayed in the first box only
