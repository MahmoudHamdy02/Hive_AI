from __future__ import annotations
from abc import ABC, abstractmethod
import math
from typing import List, Tuple

import pygame

from constants import MINIMAL_RADIUS, RADIUS

# Abstract class
class Hexagon(ABC):
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
    
    def __collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < MINIMAL_RADIUS
    def point_in_polygon(self, point: Tuple[float, float]) -> bool:
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

    def __init__(self, axial_coordinates: Tuple[int,int], position: Tuple[float, float], insect = None):
        super().__init__(axial_coordinates, position)
        self.insect=insect

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        if self.insect:
           pygame.draw.polygon(screen, (255,0,0), self.vertices)
           pygame.draw.aalines(screen, (255, 0, 0), closed=True, points=self.vertices)
        else:
           pygame.draw.polygon(screen, (150,150,150), self.vertices)
           pygame.draw.aalines(screen, (25, 25, 25), closed=True, points=self.vertices)



class HexagonOutline(Hexagon):

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