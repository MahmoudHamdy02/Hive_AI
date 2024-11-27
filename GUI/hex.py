from __future__ import annotations

import math
from typing import List, Tuple

import pygame

from constants import MINIMAL_RADIUS, RADIUS


class HexagonTile:

    def __init__(self, axial_coordinates: Tuple[int,int], position: Tuple[float, float]):
        self.axial_coordinates = axial_coordinates
        self.position = position
        self.vertices = self.compute_vertices()

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position
        return (x, y + RADIUS)

    def compute_vertices(self) -> List[Tuple[float, float]]:
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

    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        # could cache results for performance
        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]
    
    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * MINIMAL_RADIUS, rel_tol=0.05)
    
    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < MINIMAL_RADIUS
    
    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, (150,150,150), self.vertices)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)