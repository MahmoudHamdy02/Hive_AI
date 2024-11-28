import pygame
from constants import *

class InsectWidget:
    def __init__(self, name: str, color: int, count: int, position: tuple):
        self.insectName = name
        self.insectColor = color  # 0: white, 1: black
        self.insectCount = count
        self.insectPosition = position
        self.image = None  # Default image initialization

        if self.insectColor == 1 and self.insectCount > 0:
            if self.insectName == "Ant":
                self.image = pygame.image.load("GUI/images/b_insects/b-ant.png")
                print(self.insectCount)
            elif self.insectName == "bee":
                self.image = pygame.image.load("GUI/images/b_insects/b-bee.png")
            elif self.insectName == "beetle":
                self.image = pygame.image.load("GUI/images/b_insects/b-beetle.png")
            elif self.insectName == "hopper":
                self.image = pygame.image.load("GUI/images/b_insects/b-hopper.png")
            elif self.insectName == "spider":
                self.image = pygame.image.load("GUI/images/b_insects/b-spider.png")

        elif self.insectColor == 0 and self.insectCount > 0:
            if self.insectName == "Ant":
                self.image = pygame.image.load("GUI/images/w_insects/W-ant.png")
            elif self.insectName == "bee":
                self.image = pygame.image.load("GUI/images/w_insects/w-bee.png")
            elif self.insectName == "beetle":
                self.image = pygame.image.load("GUI/images/w_insects/w-beetle.png")
            elif self.insectName == "hopper":
                self.image = pygame.image.load("GUI/images/w_insects/w-hopper.png")
            elif self.insectName == "spider":
                self.image = pygame.image.load("GUI/images/w_insects/w-spider.png")

        if self.image:  # Ensure image is not None
            self.image = pygame.transform.scale(self.image, (20, 20))

    # Add function to re-render the count of insects
    def render(self, screen):
        # Draw the background rectangle
        pygame.draw.rect(screen, (255, 255, 255), (self.insectPosition[0], self.insectPosition[1], INSECT_BOX_X, INSECT_BOX_Y))
        # Draw the image if available
        if self.image:
            screen.blit(self.image, (self.insectPosition[0] + 10, self.insectPosition[1] + 10))
