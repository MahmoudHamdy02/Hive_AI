from __future__ import annotations
from abc import ABC, abstractmethod
import math
from typing import List, Tuple
from constants import *
import pygame

from constants import MINIMAL_RADIUS, RADIUS


class Hexagon(ABC):
    """Abstract parent class for hexagon tiles and outlines"""

    def __init__(self, axial_coordinates: Tuple[int,int], position: Tuple[float, float]):
        self.axial_coordinates = axial_coordinates
        self.position = position
        self.vertices = self.__compute_vertices()

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position
        return (x, y + RADIUS)

    def __compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        x, y = self.position
        half_radius = RADIUS / 2
        # Vertices in counter-clockwise order
        return [
            (x, y),
            (x - MINIMAL_RADIUS, y + half_radius),
            (x - MINIMAL_RADIUS, y + 3 * half_radius),
            (x, y + 2 * RADIUS),
            (x + MINIMAL_RADIUS, y + 3 * half_radius),
            (x + MINIMAL_RADIUS, y + half_radius),
        ]

    def contains_point(self, point: Tuple[float, float]) -> bool:
        """Check if a point (x, y) is inside the hexagon polygon"""
        x, y = point
        vertices = self.vertices
        n = len(vertices)
        inside = False

        p1x, p1y = vertices[0]
        for i in range(n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    @abstractmethod
    def render(self):
        pass


class HexagonTile(Hexagon):
    """ Hexagon tile that represents an insect piece """

    def __init__(self, axial_coordinates: Tuple[int,int], position: Tuple[float, float], insect: str = None, color: int = None, z: int = 0):
        super().__init__(axial_coordinates, position)
        self.selected = False
        self.color = color
        self.insect = insect
        self.image = None
        self.z = z
        if self.insect:
            c = "b" if self.color == Color.Black else "w"
            self.image = pygame.image.load(f"{GUI_PATH}/images/{c}_insects/{c}-{self.insect}.png")
            self.image = pygame.transform.scale(self.image, (105, 105))
            self.image = pygame.transform.rotate(self.image, 90)
    
    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""

        pygame.draw.polygon(screen, (150,150,150), self.vertices)
        pygame.draw.aalines(screen, (25, 25, 25), closed=True, points=self.vertices)
        
        if self.selected:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, (self.position[0]-53 , self.position[1]))
                



class HexagonOutline(Hexagon):
    """ Hexagon outline that represents a legal move for a piece"""

    def __init__(self, axial_coordinates: Tuple[int,int], position: Tuple[float, float]):
        super().__init__(axial_coordinates, position)
        self.inner_vertices = self.__compute_inner_vertices()
    
    def __compute_inner_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's inner vertices as x, y tuples"""
        # Draw the same outline again using a smaller radius,
        # then move it down to the center
        x, y = self.position
        r = RADIUS * 0.85
        half_radius = r / 2
        min_r = r * math.cos(math.radians(30))

        offset = abs(self.vertices[3][1] - (y + 2 * r)) // 2
        # Vertices in counter-clockwise order
        return [
            (x, y + offset),
            (x - min_r, y + half_radius + offset),
            (x - min_r, y + 3 * half_radius + offset),
            (x, y + 2 * r + offset),
            (x + min_r, y + 3 * half_radius + offset),
            (x + min_r, y + half_radius + offset),
        ]

    def render(self, screen) -> None:
        pygame.draw.aalines(screen, (25, 160, 255), closed=True, points=self.vertices)
        pygame.draw.aalines(screen, (25, 160, 255), closed=True, points=self.inner_vertices)